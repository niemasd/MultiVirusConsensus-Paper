#!/usr/bin/env bash
if (( $# < 2 )) ; then
    echo "USAGE: $0 <ref.fas> <reads1.fq> [reads2.fq] [...]" ; exit 1
fi
ref=$(basename "$1" | rev | cut -d'.' -f2- | rev)
minimap2 -a -t 8 -x sr "$@" | tee >(samtools view -@ 8 -b -o "$2.$ref.bam") | viral_consensus -i - -r "$1" -o "$2.$ref.consensus.fas" -oi "$2.$ref.inscount.json" -op "$2.$ref.poscount.tsv"
