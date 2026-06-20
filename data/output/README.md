# Summary Statistics

All benchmarks were run with MultiVirusConsensus v0.1.0 on a 2.8 GHz Intel i7-1165G7 CPU with 16 GB of memory.

## Simulated

| Folder                   | # Reads |     # Bases | Reads Mapped Correct | Reads Mapped Incorrect | Time (s) | Peak Memory (KB) |
| :----------------------- | ------: | ----------: | -------------------: | ---------------------: | -------: | ---------------: |
| [`simulated`](simulated) | 797,000 | 119,550,000 |              796,965 |                  7,998 |    21.28 |          456,732 |

## Real

| Folder                                             | SRA ID                                                                |   # Reads |       # Bases | Reads Mapped Correct | Reads Mapped Incorrect | Time (s) | Peak Memory (KB) |
| :------------------------------------------------- | :-------------------------------------------------------------------- | --------: | ------------: | -------------------: | ---------------------: | -------: | ---------------: |
| [`HMPV.SRR8776440`](HMPV.SRR8776440)               | [SRR8776440](https://trace.ncbi.nlm.nih.gov/Traces/?run=SRR8776440)   |   962,668 |   264,627,355 |              481,943 |                  3,582 |    36.37 |          427,128 |
| [`InfluenzaA.SRR37308007`](InfluenzaA.SRR37308007) | [SRR37308007](https://trace.ncbi.nlm.nih.gov/Traces/?run=SRR37308007) | 1,364,614 |   193,590,311 |              123,430 |                    128 |    28.57 |          437,104 |
| [`RSV.SRR37377179`](RSV.SRR37377179)               | [SRR37377179](https://trace.ncbi.nlm.nih.gov/Traces/?run=SRR37377179) | 1,297,542 |   248,078,890 |              271,163 |                  1,196 |    50.88 |          433,452 |
| [`SC2.SRR36479629`](SC2.SRR36479629)               | [SRR36479629](https://trace.ncbi.nlm.nih.gov/Traces/?run=SRR36479629) | 2,631,924 |   359,258,128 |            2,629,527 |                      0 |    87.54 |          651,380 |
| [`mixed`](mixed)                                   | All the above                                                         | 6,256,748 | 1,065,554,684 |            3,506,063 |                  4,906 |   228.02 |          649,108 |
