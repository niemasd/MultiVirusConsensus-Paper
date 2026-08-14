# Commands

All of the following commands assume that they will be run from the `MultiVirusConsensus-Paper/benchmark/results` folder.

## Generate Dataset

```bash
art_illumina -na -ss HS25 -i ../data/references.fas -p -l 150 -f $x -m 200 -s 10 -o OUT_PREFIX
```

## Run MultiVirusConsensus

```bash
~/MultiVirusConsensus/MultiVirusConsensus.py --quiet --keep_multimapped all -r ../../data/references.fas -i FASTQS -o OUT_FOLDER
```

## Run ViralConsensus

```bash
../scripts/run_viral_consensus.sh ../references/REFERENCE.fas FASTQS
```

## Run iVar

```bash
../scripts/run_ivar.sh ../references/REFERENCE.fas FASTQS
```

## All Together

The `sleep 2` is because `art_illumina` uses the system time as a RNG seed, so this ensures it'll be different each run.

```bash
for x in 10 20 30 ; do
    echo "- Coverage: $x"
    for r in $(seq -w 1 5) ; do
        echo "  - Replicate: $r"
        echo "    - Simulating Reads"
        art_illumina -na -ss HS25 -i ../data/references.fas -p -l 150 -f $x -m 200 -s 10 -o "x$x.r$r." > /dev/null 2>&1 && sleep 2
        echo "    - Running MVC"
        /usr/bin/time -v -o "x$x.r$r.time.mvc.txt" ~/MultiVirusConsensus/MultiVirusConsensus.py --quiet --keep_multimapped all -r ../data/references.fas -i x$x.r$r.*.fq -o "x$x.r$r.out.mvc" && \
        for c in x$x.r$r.out.mvc/*.consensus.fas ; do
            mv "$c" x$x.r$r.consensus.$(basename "$c" | rev | cut -d'.' -f3- | rev).mvc.fas
        done
        echo "    - Running ViralConsensus and iVar"
        for fas in ../references/*.fas ; do
            echo "      - Reference: $fas"
            ref=$(basename $fas | rev | cut -d'.' -f2- | rev)
            /usr/bin/time -v -o "x$x.r$r.time.$ref.viral_consensus.txt" ../scripts/run_viral_consensus.sh "$fas" x$x.r$r.*.fq > /dev/null 2>&1
            /usr/bin/time -v -o "x$x.r$r.time.$ref.ivar.txt" ../scripts/run_ivar.sh "$fas" x$x.r$r.*.fq > /dev/null 2>&1
            mv "x$x.r$r.consensus.$ref.ivar.fa" "x$x.r$r.consensus.$ref.ivar.fas"
            rm -rf *.bam */*.bam
        done
        rm -f *.fq ../references/*.fai
    done
    echo ""
done
```
