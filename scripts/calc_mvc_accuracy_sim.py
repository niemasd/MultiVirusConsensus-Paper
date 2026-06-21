#! /usr/bin/env python3
'''
Calculate MultiVirusConsensus consensus sequence accuracy on a simulated output folder
'''

# imports
from pathlib import Path
from sys import argv

# run tool
if __name__ == "__main__":
    # check args
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h','help'}:
        print(f"USAGE: {argv[0]} <mvc_sim_out>"); exit(1)
    mvc_out_path = Path(argv[1])
    if not mvc_out_path.is_dir():
        raise ValueError(f"Directory not found: {mvc_out_path}")

    # load reference sequences
    refs_path = mvc_out_path / 'references.fas'
    if not refs_path.is_file():
        raise ValueError(f"Invalid MVC output folder (missing references.fas): {mvc_out_path}")
    with open(refs_path, mode='rt') as f:
        lines = f.readlines()
    refs = {lines[i][1:].strip().split()[0].strip() : lines[i+1].strip() for i in range(0, len(lines), 2)}

    # load consensus sequences
    seqs = dict()
    for k in refs:
        fas_path = mvc_out_path / f'{k}.consensus.fas'
        if not fas_path.is_file():
            raise ValueError(f"Consensus sequence not found: {fas_path}")
        with open(fas_path, mode='rt') as f:
            seqs[k] = f.readlines()[1].strip()
        if len(seqs[k]) != len(refs[k]):
            raise ValueError(f"Reference vs. Consensus length mismatch: {k}")

    # calculate evaluation metrics
    print("ID\tlength\tnum_ambig\tprop_ambig\tnum_unambig\tprop_unambig\tnum_correct\tprop_correct")
    for ID, ref in sorted(refs.items()):
        ref_len = len(ref)
        seq = seqs[ID]
        num_ambig = seq.count('N')
        num_unambig = ref_len - num_ambig
        num_correct = sum(1 for i in range(ref_len) if ref[i] == seq[i])
        print(f"{ID}\t{ref_len}\t{num_ambig}\t{num_ambig/ref_len}\t{num_unambig}\t{num_unambig/ref_len}\t{num_correct}\t{num_correct/ref_len}")
