#! /usr/bin/env python3
'''
Build a FASTA file with 1 sequence per SARS-CoV-2 lineage
'''

# imports
from lzma import open as xzopen
from pathlib import Path

# constants
BENCHMARK_PATH = Path(__file__).parent
ASSEMBLIES_PATH = BENCHMARK_PATH / 'SC2.assemblies.fas.xz'
REFERENCE_PATH = BENCHMARK_PATH / 'reference.fas'
LINEAGES_PATH = BENCHMARK_PATH / 'lineages.fas.xz'

# run tool
if __name__ == "__main__":
    # load one assembly sequence from each lineage
    print("Loading assemblies...", end=' ')
    with xzopen(ASSEMBLIES_PATH, mode='rt') as f:
        lines = f.readlines()
    print(f"done: {len(lines)//2}")
    print("Selecting first assembly per lineage...", end=' ')
    assemblies = dict() # assemblies[lineage] = sequence
    for i in range(0, len(lines), 2):
        lineage = lines[i].split('|')[-1].strip()
        if lineage not in assemblies:
            assemblies[lineage] = lines[i+1].strip()
    print(f"done: {len(assemblies)}")

    # write one sequence per lineage
    print("Writing lineages FASTA...", end=' ')
    with xzopen(LINEAGES_PATH, mode='wt') as f:
        for k, v in assemblies.items():
            f.write(f">{k}\n{v}\n")
    print("done")
