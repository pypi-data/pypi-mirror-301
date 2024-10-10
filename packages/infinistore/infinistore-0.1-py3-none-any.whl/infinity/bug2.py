from infinity.lib import InfinityConnection, DisableTorchCaching
import torch
import time

conn = InfinityConnection()
conn.connect("127.0.0.1")

dst_tensor = torch.zeros(4096, device="cuda:2", dtype=torch.float32)
t1=time.time()
for i in range(20):
    conn.read_cache(dst_tensor, [("key1", 0), ("key2", 1024), ("key3", 2048), ("key1", 2048+1024)], 1024)
print("Time:", time.time()-t1)

conn.sync()
print(dst_tensor[2048+1024:])
