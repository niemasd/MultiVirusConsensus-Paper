# Commands

## Generate Datasets

```bash
for x in 1 10 100 1000 ; do for r in $(seq -w 1 10) ; do art_illumina -ss HS25 -i references.fas -p -l 150 -f $x -m 200 -s 10 -o simulated.x$x.r$r. ; sleep 2 ; done ; done
```

## Run MultiVirusConsensus

```bash
for s in $(ls *.fq.gz | cut -d'.' -f1-3 | sort | uniq) ; do /usr/bin/time -v -o $s.time.mvc.txt ~/MultiVirusConsensus/MultiVirusConsensus.py -r ../../data/references.fas -i $s* -o out.$s ; done
```

## Run ViralConsensus

```bash
for s in $(ls *.fq.gz | cut -d'.' -f1-3 | sort | uniq) ; do for ref in ../references/*.fas ; do /usr/bin/time -v -o $s.time.viral_consensus.$(echo $ref | rev | cut -d'/' -f1 | rev | cut -d'.' -f1).txt ../scripts/run_viral_consensus.sh "$ref" $s.*.fq.gz ; done ; done
```

## Run iVar

```bash
for s in $(ls *.fq.gz | cut -d'.' -f1-3 | sort | uniq) ; do for ref in ../references/*.fas ; do /usr/bin/time -v -o $s.time.ivar.$(echo $ref | rev | cut -d'/' -f1 | rev | cut -d'.' -f1).txt ../scripts/run_ivar.sh "$ref" $s.*.fq.gz ; done ; done
```
