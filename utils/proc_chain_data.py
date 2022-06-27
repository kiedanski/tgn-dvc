# %%
import pandas as pd


# %%
DATA_DIR = "~/workspace/data/"
# %%
df_users = pd.read_csv(DATA_DIR + "/chain-nodes.csv")
df_contracts = pd.read_csv(DATA_DIR + "/chain-edges.csv")
# %%
df_contracts["is_contract"] = True
df_users["is_contract"] = False

df_nodes = pd.concat([df_users, df_contracts], axis=0)
df_nodes = df_nodes.drop_duplicates(subset="address", keep="last")


# %%

df_trans = pd.read_csv(DATA_DIR + "/transactions.csv")
df_trans = df_trans.dropna(axis=0)
# %%

# Keep only nodes - transactions that are presnet in both

addr_trans = set(df_trans["from_address"].values)
addr_trans |= set(df_trans["to_address"].values)

addr_node = set(df_nodes["address"].values)

addr_common = addr_trans.intersection(addr_node)
# %%

# Filter by shard address
df_nodes = df_nodes[df_nodes["address"].isin(addr_common)]
df_trans = df_trans[
    (df_trans["from_address"].isin(addr_common))
    | (df_trans["to_address"].isin(addr_common))
]  # <- This should not be empty
# %%
# %%
