import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from union_find import QuickUnion, UnionWeight, UnionRank, PathCompressionType

# Enum and Union-Find classes are as provided in the initial code

def generate_random_pairs(n):
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    random.shuffle(pairs)
    return pairs

def pad_arrays(arrays, length):
    return [np.pad(array, (0, length - len(array)), 'constant') for array in arrays]

def run_experiment(n, union_strategy, compression_strategy, delta, T):
    all_tpl_records = []
    all_tpu_records = []
    results_data = []
    
    if n > 1000 and union_strategy == QuickUnion and compression_strategy == PathCompressionType.NC:
        return 0, 0, results_data

    for i in range(T):
        print(f"Running experiment {round((i + 1)/T*100,0)}% for n={n} with {union_strategy.__name__} and {compression_strategy.name} (T={T}, delta={delta})")
        uf = union_strategy(n, compression_strategy)
        pairs = generate_random_pairs(n)

        tpl_records = []
        tpu_records = []

        start_time = time.time()

        for k, (i, j) in enumerate(pairs):
            uf.merge(i, j)

            if (k + 1) % delta == 0 or uf.nr_blocks() == 1:
                tpl_records.append(uf.tpl())
                tpu_records.append(uf.tpu())
                elapsed_time = time.time() - start_time
                results_data.append({
                    'n': n,
                    'k': k,
                    'depth': uf.depth(0),
                    'Time (s)': elapsed_time,
                    'TPU': uf.tpu(),
                    'TPL': uf.tpl(),
                    'Normalized Depth': uf.depth(0) / n if n != 0 else 0,
                    'Normalized TPU': uf.tpu() / n if n != 0 else 0,
                    'Normalized TPL': uf.tpl() / n if n != 0 else 0,
                    'Union-Find Class': union_strategy.__name__,
                    'Path Compression': compression_strategy.name
                })
                if uf.nr_blocks() == 1:
                    break

        if len(tpl_records) >= 5:
            all_tpl_records.append(np.array(tpl_records))
            all_tpu_records.append(np.array(tpu_records))

    if not all_tpl_records or not all_tpu_records:
        return np.array([]), np.array([]), results_data

    max_length = max(len(record) for record in all_tpl_records)
    all_tpl_records = pad_arrays(all_tpl_records, max_length)
    all_tpu_records = pad_arrays(all_tpu_records, max_length)

    avg_tpl = np.mean(all_tpl_records, axis=0)
    avg_tpu = np.mean(all_tpu_records, axis=0)

    return avg_tpl, avg_tpu, results_data

# Main experiment execution
n_values = [1000, 5000, 10000]
T = 20
delta = {
    1000: 10,
    5000: 50,
    10000: 100
}

strategies = {
    "QU-NC": (QuickUnion, PathCompressionType.NC),
    "QU-FC": (QuickUnion, PathCompressionType.FC),
    "QU-PS": (QuickUnion, PathCompressionType.PS),
    "QU-PH": (QuickUnion, PathCompressionType.PH),
    "UW-NC": (UnionWeight, PathCompressionType.NC),
    "UW-FC": (UnionWeight, PathCompressionType.FC),
    "UW-PS": (UnionWeight, PathCompressionType.PS),
    "UW-PH": (UnionWeight, PathCompressionType.PH),
    "UR-NC": (UnionRank, PathCompressionType.NC),
    "UR-FC": (UnionRank, PathCompressionType.FC),
    "UR-PS": (UnionRank, PathCompressionType.PS),
    "UR-PH": (UnionRank, PathCompressionType.PH),
}


for n in n_values:
    all_results_data = []
    for strategy_name, (union_strategy, compression_strategy) in strategies.items():
        print(f"Running experiment for n={n} with {strategy_name}")
        tpl, tpu, results_data = run_experiment(n, union_strategy, compression_strategy, delta[n], T)
        all_results_data.extend(results_data)
    df = pd.DataFrame(all_results_data)
    df.to_csv(f'union_find_experiments_results_{n}.csv', index=False)
    

# Convert the results data to a pandas DataFrame
df = pd.DataFrame(all_results_data)

df.to_csv('union_find_experiments_results.csv', index=False)
