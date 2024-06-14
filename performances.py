import os
import random
import time
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from union_find import QuickUnion, UnionWeight, UnionRank, PathCompressionType

# Define the range for n and the step
n_values = list(range(1, 1000, 10)) + [1000 + i * 10 for i in range(100)]

# List of path compression types and union-find classes
path_compressions = ["NC", "FC", "PS", "PH"]
union_find_classes = [UnionWeight, UnionRank]

def random_operations(uf, size: int, num_operations: int):
    """Perform a series of random merges and finds."""
    for _ in range(num_operations):
        a, b = random.randint(0, size - 1), random.randint(0, size - 1)
        uf.merge(a, b)
        uf.find(a)

data = []

# Enhanced tests
for path_compression in path_compressions:
    print(f"Path compression: {path_compression}")
    for union_find_class in union_find_classes:
        print(f"Union find class: {union_find_class.__name__}")
        for n in n_values:
            print(f"\t n: {n}")
            uf = union_find_class(n, PathCompressionType[path_compression])
            start_time = time.time()

            # Perform random operations
            random_operations(uf, n, n * 10)

            elapsed_time = time.time() - start_time

            # Merge first and last element to check stats
            uf.merge(0, n - 1)

            # Print stats
            data.append({
                'n': n,
                'depth': uf.depth(0),
                'Time (s)': elapsed_time,
                'TPU': uf.tpu(),
                'TPL': uf.tpl(),
                'Normalized Depth': uf.depth(0) / n if n != 0 else 0,
                'Normalized TPU': uf.tpu() / n if n != 0 else 0,
                'Normalized TPL': uf.tpl() / n if n != 0 else 0,
                'Union-Find Class': union_find_class.__name__,
                'Path Compression': path_compression
            })

df = pd.DataFrame(data)


df.to_csv('data.csv', index=False)