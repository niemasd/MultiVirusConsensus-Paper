# Commands

All of the following commands assume that they will be run from the `MultiVirusConsensus-Paper/benchmark/results` folder.

## Generate Datasets

```bash
for x in 1 10 100 1000 ; do for r in $(seq -w 1 10) ; do art_illumina -na -ss HS25 -i ../data/references.fas -p -l 150 -f $x -m 200 -s 10 -o simulated.x$x.r$r. ; sleep 2 ; done ; done
```

## Run MultiVirusConsensus

```bash
for s in $(ls *.fq.gz | cut -d'.' -f1-3 | sort | uniq) ; do /usr/bin/time -v -o $s.time.mvc.txt ~/MultiVirusConsensus/MultiVirusConsensus.py --keep_multimapped all -r ../../data/references.fas -i $s* -o out.$s ; done
```

## Run ViralConsensus

```bash
for s in $(ls *.fq.gz | cut -d'.' -f1-3 | sort | uniq) ; do for ref in ../references/*.fas ; do /usr/bin/time -v -o $s.time.viral_consensus.$(echo $ref | rev | cut -d'/' -f1 | rev | cut -d'.' -f1).txt ../scripts/run_viral_consensus.sh "$ref" $s.*.fq.gz ; done ; done
```

## Run iVar

```bash
for s in $(ls *.fq.gz | cut -d'.' -f1-3 | sort | uniq) ; do for ref in ../references/*.fas ; do /usr/bin/time -v -o $s.time.ivar.$(echo $ref | rev | cut -d'/' -f1 | rev | cut -d'.' -f1).txt ../scripts/run_ivar.sh "$ref" $s.*.fq.gz ; done ; done
```

## All Together

This is what should actually be run to avoid creating a bunch of FASTQ files, which can get quite large.

```bash
for x in 1 10 100 1000 ; do for r in $(seq -w 1 10) ; do art_illumina -na -ss HS25 -i ../data/references.fas -p -l 150 -f $x -m 200 -s 10 -o "x$x.r$r." ; /usr/bin/time -v -o "x$x.r$r.time.mvc.txt" ~/MultiVirusConsensus/MultiVirusConsensus.py -r ../data/references.fas --keep_multimapped all -i x$x.r$r.*.fq -o "x$x.r$r.out.mvc" && for c in x$x.r$r.out.mvc/*.consensus.fas ; do mv "$c" x$x.r$r.consensus.$(basename "$c" | rev | cut -d'.' -f2- | rev).mvc.fas ; done ; echo "RUN IVAR" ; echo "RUN VIRALCONSENSUS" ; rm -f *.fq *.bam */*.bam; done ; done
```
