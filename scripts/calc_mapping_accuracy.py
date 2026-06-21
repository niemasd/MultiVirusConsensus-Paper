#! /usr/bin/env python3
'''
Count the number of fragments that mapped to the correct reference genome
'''

# imports
from pathlib import Path
from pysam import AlignmentFile
from sys import argv

# constants
SAMPLE_TO_REF_PREFIX = {
    'SRR8776440':  'NC_039199', # HMPV
    'SRR37308007': 'NC_0073',   # Influenza A
    'SRR37377179': 'OP890336',  # RSV
    'SRR36479629': 'NC_045512', # SARS-CoV-2
    'CY040449':    'CY040449',
    'CY040450':    'CY040450',
    'CY040451':    'CY040451',
    'CY040452':    'CY040452',
    'CY040453':    'CY040453',
    'CY040454':    'CY040454',
    'CY040455':    'CY040455',
    'CY040456':    'CY040456',
    'NC_007366':   'NC_007366',
    'NC_007367':   'NC_007367',
    'NC_007368':   'NC_007368',
    'NC_007369':   'NC_007369',
    'NC_007370':   'NC_007370',
    'NC_007371':   'NC_007371',
    'NC_007372':   'NC_007372',
    'NC_007373':   'NC_007373',
    'NC_026431':   'NC_026431',
    'NC_026432':   'NC_026432',
    'NC_026433':   'NC_026433',
    'NC_026434':   'NC_026434',
    'NC_026435':   'NC_026435',
    'NC_026436':   'NC_026436',
    'NC_026437':   'NC_026437',
    'NC_026438':   'NC_026438',
    'NC_045512':   'NC_045512',
    'OP890336':    'OP890336',
    'OP965707':    'OP965707',
    'NC_039199':   'NC_039199',
    'NC_023891':   'NC_023891',
}

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
    correct = 0; incorrect = 0
    for reference, frag_IDs in fragments.items():
        for frag_ID in frag_IDs:
            if reference.startswith(SAMPLE_TO_REF_PREFIX[frag_ID.split('.')[0].strip()]):
                correct += 1
            else:
                incorrect += 1
    print(f"Correct:\t{correct}")
    print(f"Incorrect:\t{incorrect}")
