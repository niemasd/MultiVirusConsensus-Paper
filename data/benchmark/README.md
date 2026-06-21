# Command

```bash
for x in 1 10 100 ; do for r in $(seq -w 1 10) ; do art_illumina -ss HS25 -i references.fas -p -l 150 -f $x -m 200 -s 10 -o simulated.x$x.r$r. ; sleep 2 ; done ; done
```
