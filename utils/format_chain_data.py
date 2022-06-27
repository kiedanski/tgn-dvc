# %%
import json
import time
import datetime
from pathlib import Path

# %%
DIR = Path("/home/worker/workspace/data/")
OUTDIR = Path("/home/worker/workspace/assets/formatted")
OUTDIR.mkdir(parents=True, exist_ok=True)

NODE_FILE = DIR / "chain-nodes.csv"
EDGE_FILE = DIR / "chain-edges.csv"
MAP_FILE = OUTDIR / "map.json"
# %%
FIRST_ETH_DATE = datetime.datetime(2015, 7, 28)
DATE_FORMAT = "%Y-%m-%d %H:%M%S+00:00"

# %%

# %%
addr2num = {}
cnt = 0
# %%

start = time.perf_counter()
with open(OUTDIR / "node.csv", "w") as f:
    with open(NODE_FILE, "r") as fh:
        for i, line in enumerate(fh):

            if i == 0:
                f.write(line)
                continue

            if i % 10000:
                elapsed = (time.perf_counter() - start) / 3600
                tot = 219997030
                perc = i / tot
                remaining = (tot - i) / i * elapsed
                print(
                    f"Nodes: {perc:4%}, Elapsed: {elapsed:.3f}h, Remaining: {remaining:.3f}h",
                    flush=True,
                    end="\r",
                )

            parts = line.strip().split(",")
            addr = parts[0]
            if addr in addr2num:
                new_line = [str(addr2num[addr])]
            else:
                addr2num[addr] = cnt
                new_line = [str(cnt)]
                cnt += 1

            for p in parts[1:]:
                p_ = p
                if p == "True":
                    p_ = 1
                elif p == "False":
                    p_ = 0
                elif p == "" or p == None:
                    p_ = 0
                new_line.append(str(p_))

            f.write(",".join(new_line) + "\n")

print("\n", flush=True)
# %%
with open(MAP_FILE, "w") as fh:
    json.dump(addr2num, fh, indent=2)
# %%

# %%
# address = []
# total = 0
# used = 0
# start = time.perf_counter()
# with open(OUTDIR / "edge.csv", "w") as f:
#     with open(EDGE_FILE, "r") as fh:
#         for i, line in enumerate(fh):
#                 if i == 0:
#                     f.write(line)
#                     continue

#                 total += 1
#                 if i % 10000:
#                     elapsed = (time.perf_counter() - start) / 3600
#                     tot = 1598534865
#                     perc = i / tot
#                     remaining = (tot - i) / i * elapsed
#                     print(f"Edges: {perc:4%}, Elapsed: {elapsed:.3f}h, Remaining: {remaining:.3f}h", flush=True, end="\r")

#                 parts = line.strip().split(",")

#                 from_addr = addr2num.get(parts[0], None)
#                 to_addr = addr2num.get(parts[1], None)
#                 if from_addr is None or to_addr is None:
#                     continue

#                 used += 1

#                 date_obj = datetime.datetime.fromisoformat(parts[3][:-6])
#                 time_str = date_obj - FIRST_ETH_DATE
#                 time_str = time_str.total_seconds()

#                 new_line = [from_addr, to_addr, parts[2], time_str]

#                 f.write(",".join(map(str, new_line)) + "\n")


# print(f"Percentage of edges with valid node data {used / total:.2%}")
