# %%
import json
import time
import threading
import datetime
import queue
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
with open(MAP_FILE, "r") as fh:
    addr2num = json.load(fh)
# %%

q = queue.Queue()


def write2disk():

    with open(OUTDIR / "edge.csv", "w") as f:
        while True:
            line = q.get()
            f.write(line)


# %%

threading.Thread(target=write2disk, daemon=True).start()


address = []
total = 0
used = 0
start = time.perf_counter()

with open(OUTDIR / "edge.csv", "w") as f:
    with open(EDGE_FILE, "r") as fh:
        for i, line in enumerate(fh):
            if i == 0:
                q.put(line)
                continue

            total += 1
            if i % 10000:
                elapsed = (time.perf_counter() - start) / 3600
                tot = 1000000
                perc = i / tot
                remaining = (tot - i) / i * elapsed
                print(
                    f"Edges: {perc:4%}, Elapsed: {elapsed:.3f}h, Remaining: {remaining:.3f}h",
                    flush=True,
                    end="\r",
                )

            if i % 100000 == 0:
                break

            parts = line.strip().split(",")

            from_addr = addr2num.get(parts[0], None)
            to_addr = addr2num.get(parts[1], None)
            if from_addr is None or to_addr is None:
                continue

            used += 1

            date_obj = datetime.datetime.fromisoformat(parts[3][:-6])
            time_str = date_obj - FIRST_ETH_DATE
            time_str = time_str.total_seconds() / 1000000

            new_line = [from_addr, to_addr, time_str, 0, parts[2]]

            new_line = ",".join(map(str, new_line)) + "\n"
            f.write(new_line)


print(f"Percentage of edges with valid node data {used / total:.2%}")
