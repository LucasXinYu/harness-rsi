# Continual adaptation, transfer and attribution — October 24, 2026

The living collection now contains **276 papers and 11 official resources**. This targeted search adds seven records, including an October 15 study recovered through overlapping searches. It is not an exhaustive census. The **95 category–source records through October 1 and dataset v0.1.0 are unchanged**. The public reading PDF remains the October 20 edition; a new working manuscript is being prepared separately.

## Seven additions, four existing categories

| Study | Primary category | Inspected source and locator |
| :-- | :-- | :-- |
| MaD-RSI | Harness optimization and search | [2610.28201v1](https://arxiv.org/html/2610.28201v1), §§3–4, 7 |
| Harness-Delta Attribution | Generalization, evaluation and safety | [2610.22466v1](https://arxiv.org/html/2610.22466v1), §§3–5; Appendix C |
| Harness Scaling | Model and policy training | [2610.29458v1](https://arxiv.org/html/2610.29458v1), §§3–4 |
| HarnessAdapt-RL / Training the Whole Agent | Model and policy training | [2610.28069v1](https://arxiv.org/html/2610.28069v1), §§3, 4.4–4.6; Appendices 9.4, 9.8 |
| Are Self-Evolving Agents Continual Learners? | Generalization, evaluation and safety | [2610.25858v1](https://arxiv.org/html/2610.25858v1), §§3–4; Appendices B–D |
| Recoverability and Verifier Strength | Generalization, evaluation and safety | [2610.27465v1](https://arxiv.org/html/2610.27465v1), §§2–5; Appendix E |
| SERA / From VLM Planners to Robotic Agents | Task-domain harness evolution | [2610.29560v1](https://arxiv.org/html/2610.29560v1), §§3–4; Appendices A.1, B.3 |

Bibliographic identity, first-release provenance and individual mechanism summaries are in the [catalog](catalog.json). Existing categories accommodate these mechanisms; an additional application does not by itself require a new taxonomy branch.

## What the comparison changes

**Transfer has a direction.** MaD-RSI uses several fixed models to improve a shared harness. Harness Scaling trains a policy across supplied harness variation. HarnessAdapt-RL changes policy and runtime support together. These interventions answer different questions: a reusable harness, a model robust to harness changes, and a compatible model–harness pair are distinct outputs.

**A better endpoint is insufficient for continual improvement.** The continual-learning study tests drift and earlier-task retention. HDA asks what explains a gain after accounting for compute and detectable shortcuts. Together they motivate a sequence-level comparison: which gain survives the next change, at what cost, and with what interference? Neither a residual attribution term nor a single final score establishes sustained transfer.

**Persistence must be specified.** In SERA, the selected planner harness is fixed before testing while episode context still changes. In the recoverability study, saved versions support rollback, but rollback cannot erase effects that already occurred. A mutable context, a versioned harness, and a changed improvement procedure should therefore have separate records.

## A reporting contract for future releases

For each intervention, identify the editable artifact, its later consumer, the model and task distribution, and what remained fixed. Record proposal, acceptance, activation and task effect separately. Evaluate intermediate checkpoints on both new and earlier tasks. Compare unchanged reuse with re-optimization and include search, validation and deployment costs. When possible, retain rejected candidates and regressions; absence of a report is not evidence of absence.

This is our synthesis and proposed reporting practice, not a claim that all collected studies satisfy these controls or that we reproduced their experiments.

## Scope correction

[EnvHarness](https://arxiv.org/abs/2608.19880) scales environment-side training signals while leaving the task agent's own harness unchanged. Its catalog description now makes this distinction explicit, consistent with the author's clarification. It remains adjacent training infrastructure; no frozen domain record was relabeled or added.

The survey's posted [Preprints.org v1](https://www.preprints.org/manuscript/202610.2293) is available separately from the author-hosted reading revision. Neither is peer-reviewed.
