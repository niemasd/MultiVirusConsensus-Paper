#!/usr/bin/env bash
if (( $# < 2 )) ; then
    echo "USAGE: $0 <ref.fas> <reads1.fq> [reads2.fq] [...]" ; exit 1
fi
ref=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
minimap2 -a -t 8 -x sr "$@" | samtools sort -@ 8 -o "$2.$ref.bam" && \
samtools mpileup -A -aa -d 0 -Q 0 --reference "$1" "$2.$ref.bam" | ivar consensus -p "$2.$ref.consensus.fas"
