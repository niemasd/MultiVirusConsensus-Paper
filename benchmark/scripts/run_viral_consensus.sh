#!/usr/bin/env bash
if (( $# < 2 )) ; then
    echo "USAGE: $0 <ref.fas> <reads1.fq> [reads2.fq] [...]" ; exit 1
fi
ref=$(basename "$1" | rev | cut -d'.' -f2- | rev)
prefix=$(basename "$2" | cut -d'.' -f1-2)
minimap2 -a -t 8 -x sr "$@" | viral_consensus -i - -r "$1" -o "$prefix.consensus.$ref.viral_consensus.fas"
