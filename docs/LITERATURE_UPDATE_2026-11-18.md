# Literature update · November 18, 2026

Four source-checked studies bring the living bibliography to 347 papers and 11 resources.

The comparisons sharpen three separate questions: how changes are accepted, whether they preserve other behavior, and which parts of the system learn. No new literature category is needed.

## Harnesses That Improve Themselves

Proposes changes to one harness module at a time and gates them using validation outcomes, executed-code checks and a runtime token cap. Reject updates that fail validation or exceed the cost limit. Freeze the chosen harness before held-out evaluation.

Modular gated evolution attained 40.0% held-out accuracy at 46.7k tokens per task, versus 42.5% at 451.6k for an unconstrained full rewrite. The modular harness permits 12 turns, while the unconstrained rewrite permits 28. This is a combined accuracy–cost comparison, not an equal-budget estimate of the gate alone. The test set mixes held-out tasks from the development repository and a new repository. [Primary text](https://arxiv.org/html/2611.22299v1), Section VII, Table IV.

## Synapse

Compiles recognized skill instructions into a source-linked partial program, repairs mapped spans, and screens structurally related tests including previously passing cases. Rank candidate patches using repair-test results, then accept only a validation improvement. Run three repair iterations and evaluate the selected skill on held-out questions.

On DocVQA with GPT-6 Sol, full Synapse scored 90.64% versus 87.97% for the variant without SkIR-based repair and broader screening. The ablation jointly changes repair representation and screening, so it does not isolate either effect. The method relies on self-reported coverage and an unmeasured locality assumption. Small validation suites and earlier development-time test scoring limit confidence in generalization. [Primary text](https://arxiv.org/html/2611.20856v1), Sections 3.6, 4.1 and 4.3, Table 2, Section 5.

## CRAFT

Routes adaptation between correction memory, inferred rules and an online learned model while a supervisor enforces the robot execution contract. Update the provider from scoped outcome feedback. Physical completion and task acceptability are scored separately. The pilot freezes the service and interaction budgets before evaluation.

The ladder completed 96/120 acceptable jobs versus 94/120 for a frontier agent with memory and rules. It asked 6 versus 11 optional questions, but dispatched 13 versus 9 wrong actions. Six streams support a descriptive comparison, not a superiority claim. Both methods use simulation and different adaptation providers. The frontier incurs seven decision timeouts. The project includes a separately trained perception probe and online adaptation learners. The integrated pilot uses a shared segmentation/depth frontend and a frozen robot skill. [Primary text](https://arxiv.org/html/2611.19952v1), Sections 4–6.5, Table 3 and Appendix G.

## When Agent Skills Go Stale

Replays previously recorded checks, verifies conflicts with retained skill state, and attempts local repair before rebuilding when necessary. Validate candidates on disjoint tasks or runs using performance and cost criteria. Retain the previous state if neither repair nor rebuilding is accepted.

For procedural AppWorld skills, selective maintenance scored 0.569 versus 0.627 without maintenance, with mean execution cost 24.8 versus 25.7. The paired performance difference was -5.9 percentage points, with a bootstrap interval from -21.6 to +9.8. The interval spans decline and improvement. The study evaluates one maintenance event after a controlled environment change, not successive continual updates. Lower execution cost does not establish preserved task performance. [Primary text](https://arxiv.org/html/2611.22525v1), Sections 4.1–4.2, Table 4 and Appendix E.1.

## Search and curation

The November 10–18 submission-date queries returned 135 distinct arXiv IDs. Additional screening used cs.AI, cs.CL and cs.LG announcement titles and the earlier queue. 423 candidates remain pending. The revision audit returned all 329 identified arXiv IDs from the bibliography and evidence registry, with no updates dated November 17 or later. These searches are targeted and do not establish exhaustive coverage.

Evidence v0.8.0 contains 170 category–source records from 137 works, 70 scoped observations and 85 targeted AI-assisted primary-source checks. The other 85 records retain their inherited review status. No independent human adjudication or experimental reproduction is claimed. [Dataset card](dataset/v0.8.0/DATASET_CARD.md).

This release corrects the README’s stale primary-check count. Previously published datasets, the original 95-record atlas, the November 14 reading PDF and the posted preprint retain their independent version dates.
