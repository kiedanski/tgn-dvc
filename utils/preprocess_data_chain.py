# %%
import json
import numpy as np
import pandas as pd
from pathlib import Path
import argparse

# %%


def preprocess(data_name):
    u_list, i_list, ts_list, label_list = [], [], [], []
    feat_l = []
    idx_list = []

    with open(data_name) as f:
        s = next(f)
        for idx, line in enumerate(f):
            e = line.strip().split(",")
            u = int(e[0])
            i = int(e[1])

            ts = float(e[2])
            label = float(e[3])  # int(e[3])

            feat = np.array([float(x) for x in e[4:]])

            u_list.append(u)
            i_list.append(i)
            ts_list.append(ts)
            label_list.append(label)
            idx_list.append(idx)

            feat_l.append(feat)
    return pd.DataFrame(
        {"u": u_list, "i": i_list, "ts": ts_list, "label": label_list, "idx": idx_list}
    ), np.array(feat_l)


def reindex(df, bipartite=True):
    new_df = df.copy()
    if bipartite:
        assert df.u.max() - df.u.min() + 1 == len(df.u.unique())
        assert df.i.max() - df.i.min() + 1 == len(df.i.unique())

        upper_u = df.u.max() + 1
        new_i = df.i + upper_u

        new_df.i = new_i
        new_df.u += 1
        new_df.i += 1
        new_df.idx += 1
    else:
        new_df.u += 1
        new_df.i += 1
        new_df.idx += 1

    return new_df


def node_features(filepath, node_dict):

    features = []
    count = 0
    with open(filepath, "r") as fh:
        for i, line in enumerate(fh):
            if i == 0:
                continue
            parts = line.strip().split(",")
            addr = int(parts[0])
            # import pdb; pdb.set_trace()
            if addr in node_dict:
                count += 1
                features.append([parts[1:]])

            print(count, flush=True, end="\r")
    features = np.vstack(features).astype(float)
    return features


def run(data_name="chain", bipartite=False):
    # path = Path("asset/").mkdir(parents=True, exist_ok=True)
    PATH_EDGES = "./assets/formatted/edge.csv".format(data_name)
    PATH_NODES = "./assets/formatted/node.csv".format(data_name)
    OUT_DF = "./data/ml_{}.csv".format(data_name)
    OUT_FEAT = "./data/ml_{}.npy".format(data_name)
    OUT_NODE_FEAT = "./data/ml_{}_node.npy".format(data_name)

    df, feat = preprocess(PATH_EDGES)
    new_df = reindex(df, bipartite)

    empty = np.zeros(feat.shape[1])[np.newaxis, :]
    feat = np.vstack([empty, feat])

    nodes = dict(
        (v, k) for k, v in enumerate(set(new_df.u.unique()).union(new_df.i.unique()))
    )
    new_df["u"] = new_df["u"].map(nodes)
    new_df["i"] = new_df["i"].map(nodes)
    new_df = new_df.sort_values("ts", ascending=True)

    feat_node = node_features(PATH_NODES, nodes)

    # max_idx = max(new_df.u.max(), new_df.i.max())
    # max_idx = len(nodes)
    # rand_feat = np.zeros((max_idx + 1, 172))

    new_df.to_csv(OUT_DF)
    np.save(OUT_FEAT, feat)
    np.save(OUT_NODE_FEAT, feat_node)


run()
