#! /usr/bin/env python3
'''
Count the number of fragments that mapped to each reference sequence
'''

# imports
from json import dump as jdump
from pathlib import Path
from pysam import AlignmentFile
from sys import argv, stdout

# run tool
if __name__ == "__main__":
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h','help'}:
        print(f"USAGE: {argv[0]} <bam_file>"); exit(1)
    p = Path(argv[1])
    if not p.is_file():
        raise ValueError(f"File not found: {p}")
    with AlignmentFile(p, 'r') as bam:
        fragments = {ref:set() for ref in bam.references}
        for read in bam.fetch(until_eof=True):
            if read.is_proper_pair and (not read.is_secondary) and (not read.is_supplementary):
                fragments[read.reference_name].add(read.query_name)
    jdump({k:len(v) for k,v in fragments.items()}, stdout, indent=4)
    stdout.write('\n')
