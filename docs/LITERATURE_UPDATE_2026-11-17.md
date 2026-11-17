# Literature update · November 17, 2026

Two November 16 preprints and two earlier studies bring the bibliography to 343 papers and 11 resources.

## ELITE

Develops alternative changes to a common agent scaffold and integrates compatible edits after inspecting their implementations. Structural checks and smoke tests gate updates. An invalid integrated agent leaves the parent in place. The evolution loop receives no downstream task scores.

With DeepSeek-V4-Flash, the authors report 73.3% on SWE-bench Verified after evolution versus 64.0% for the initial agent. This is a full-system transfer comparison on 50 tasks. Three evolution runs inform the mean. On the Pro subset ELITE scored below HGM (85.6% vs 88.3%). The zero task-evaluation count excludes final testing and does not imply zero evolution cost. [Primary text](https://arxiv.org/html/2611.21056v1), Sections 4–5.3, Tables 1–2 and Appendix A.4.

## Harness Leverage Across Model Size

Compares a fixed set of workflow harnesses and ablates the six executable completion checks within Mingbird. The study prespecifies harness variants and scores output artifacts on a frozen suite. The checks govern completion during a run.

At 4.7B, the full harness averaged 0.980 versus 0.984 with its six checks disabled. The paired difference was -0.004, with an interval from -0.052 to +0.044. The interval includes zero. This ablation cannot identify which individual check matters, and the paper reports saturation on higher-capacity runs. Results describe a fixed harness comparison. [Primary text](https://arxiv.org/html/2611.21407v1), Sections 3.4–3.8 and 4.4, Table 7.

## EasyFoam

Distills solver traces into edits to external skill files. Each proposal competes against the same parent on separate validation tasks. Each round uses disjoint proposal and validation tasks and penalizes regressions across task families. The final skill library is frozen for test.

On the 25 held-out ExtFoamBench tasks, 5 passed all acceptance checks with evolved skills versus 2 with the initial skills (20% vs 8%). Development and test share task families. The comparison measures transfer to new tasks within those families and the combined effect of the selected edits. Execution completion alone is insufficient for acceptance. [Primary text](https://arxiv.org/html/2611.14525v1), Sections 3.3 and 4.4, Table 3 and Appendix D.3.

## When Should LLM Agents Forget?

Selects whether to discard memories flagged as stale or pass the flat context to the generator according to performance at a matched resolver-error level. Within each simulated corruption level, choose hard deletion only when it beats flat retention on calibration data. Freeze that choice for test.

Pooled over 612 environment–query outcomes, the calibrated gate achieved 0.655 accuracy versus 0.641 for always discarding items labeled stale. The 612 outcomes reuse 102 distinct test queries. The study uses synthetic validity errors and a retrospective matched sweep. Transfer to a new error distribution and production costs were not established by this comparison. [Primary text](https://arxiv.org/html/2611.17338v1), Sections 4–6 and 12, deployment-matched validation gate in Section 6.

## Search and curation

The four November 8–17 submission-date queries returned 144 distinct arXiv IDs. We also screened announcement titles and revisited the pending queue. There are 397 candidates awaiting further review. The revision query covered 325 distinct arXiv IDs from the collection and evidence registry. It returned no updates dated November 15 or later. The results above come from the stated versions.

Evidence v0.7.0 contains 166 category–source records from 133 works, with 81 targeted AI-assisted primary checks and 66 scoped observations. Independent human adjudication is pending. [Dataset card](dataset/v0.7.0/DATASET_CARD.md).
