# Certificate Table — Primary and Redundant Proofs

Use this file as the single source of manuscript table values.

| Quantity | Primary certificate | Independent redundancy | Role |
|---|---:|---:|---|
| Cut \(T\) | 300 | 1000 | finite-history cut |
| Mesh cells \(N\) | 12000 | 20000 | CAP discretization |
| \(\rho(M)\) bracket | [0.0707, 0.0813] | [0.1213, 0.1376] | diagnostic linear bound operator |
| \(F(b)<b\) min relative slack | \(6.036\times10^{-4}\) | \(5.651\times10^{-4}\) | self-map certificate |
| Perron contraction \(\kappa\) | \(\le0.083612\) | \(\le0.187495\) | Banach contraction |
| adapted state tube | \(\le4.8661\times10^{-4}\) | \(\le4.3355\times10^{-3}\) | finite-history error |
| physical state tube | \(\le2.2193\times10^{-4}\) | \(\le1.9773\times10^{-3}\) | finite-history error |
| certified entry cells | 836 | 789 | threshold excursion |
| entry time span | [5.8576774143, 13.7275388580] | [5.8595227628, 13.7288892565] | cold-start extinction region |
| best threshold margin \(\eta\) | \(\ge0.0309411007\) | \(\ge0.0309340309\) | entry separation |
| \(K_J\) upper bound | 11.3499043 | 11.3457429 | M1 |
| \(M_T\) upper bound | 0.043232414 | 0.015478583 | M1 |
| M1 radius \(r\) | 2221/20000 | 2222/20000 | M1 |
| \(K_JC_rr\) | \(\le0.48857\) | \(\le0.48862\) | contraction tail |
| M1 margin | \(\ge0.0135626\) | \(\ge0.0413364\) | survival proof |

## Primary manuscript choice

Use \(T=300,N=12000\) in theorem statements and the main CAP exposition because:
- the state tube is substantially tighter;
- the computation is smaller;
- threshold entry is certified over a slightly wider interval;
- the M1 margin is already comfortably positive.

Use \(T=1000,N=20000\) only in a compact robustness paragraph/table row.

## Provenance

Primary manifests:
- \`computations/manifests/t6_stageD_adaptT300_N12000_manifest.json\`
- \`computations/manifests/t6_stageE_adaptT300_N12000_manifest.json\`
- \`computations/manifests/t6_summary_adaptT300_N12000_manifest.json\`

Redundant manifests:
- \`computations/manifests/t6_stageD_adaptT1000_N20000_manifest.json\`
- \`computations/manifests/t6_stageE_adaptT1000_N20000_manifest.json\`
- \`computations/manifests/t6_summary_adaptT1000_N20000_manifest.json\`

Certificate code:
\`c9bc2f80788e0834ecb74e69e89aab59e50c741d\`.
