# Persistent experience, specialization and evaluator validity

Targeted literature update: **27 October 2026**. The search overlaps the previous completed horizon by seven days (17–27 October) and revisits pending candidates. Six newly collected papers were first posted on 18–22 October; the update date is not their publication date. The living collection now contains **282 papers and 11 official resources**. No new category is needed.

This release also publishes the revised author manuscript, incorporating the October 24 draft and today's changes. The [October 27 reading PDF](paper/Harness_RSI_Preprint_2026-10-27.pdf) and [paper/citation page](paper/) describe that version. [Preprints.org v1](https://doi.org/10.20944/preprints202610.2293.v1) remains a separate submitted version. The October 1 domain snapshot, 95 category–source records and dataset v0.1.0 are unchanged.

## What changes in the synthesis

**Transfer must name what remains fixed.** RiseHarness adapts separately for each executor before cross-benchmark evaluation; its cross-model swap is weaker than using each model's own adapted harness. OO-Harness freezes a hierarchy before testing and chooses the base harness throughout its disjoint-application-family test. Reusing a successful specialization, falling back safely, and adapting a new specialization are different outcomes.

**Memory can change several learned objects.** BEAM fixes the task executor but trains a memory-value estimator. HERD distills skill-conditioned behavior into model weights while retaining a fixed skill writer. MCCL proposes a framework separating memory substrate, asset and management policy. These studies help specify whether improvement resides in stored experience, a selector, the task model, or the mechanism proposing future edits; their evidence does not make these objects interchangeable.

**An evolving evaluator still needs a reference.** VeriEvolve repairs executable evaluators between search rounds and preserves regression cases, while an external verifier supplies calibration and admission outcomes. Generated-challenge agreement is not held-out validity, and an internally improving score cannot by itself establish that task quality improved.

The resulting evaluation question is concrete: does persistent improvement evidence produce better subsequent edits under the same total proposal/evaluation budget, after a model or task shift, while retaining earlier gains? Checkpoints, reset-memory controls, independent reference evaluation, and separate reporting of fallback and active-edit effects would help answer it. This is our synthesis and proposed test contract, not a newly reproduced empirical result.

## Verified additions and source locations

### RiseHarness: Harness Self-Evolution for Long-Horizon Terminal Agents

**First posted:** 2026-10-20. **Category:** Harness Optimization and Search Workflows.

Revises prompts and executable interaction logic around a fixed terminal-agent model, task protocol and verifier. Contrasting successful and failed runs of the same task exposes agent and internal harness traces; a handbook maps symptoms to editable responsibilities. Acceptance uses repeated development runs; independent behavior checks are optional, not universal. Each model is adapted separately before cross-benchmark testing. Swapping final harnesses between models underperforms their own adapted versions, so cross-benchmark reuse does not establish cross-model portability. Noisy selection and combined edits limit component attribution.

[Primary full text, v1](https://arxiv.org/html/2610.27435v1): Sections 3.1–3.5, 4.4; Appendices A.4, B, D.4 and E. [Identity and submission history](https://arxiv.org/abs/2610.27435v1).

### OO-Harness: Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design

**First posted:** 2026-10-20. **Category:** Harness Optimization and Search Workflows.

Builds a hierarchy of specialized harness subclasses by reusing and overriding parent behavior, retaining design and routing lessons from proposal outcomes. Acceptance targets a discovered task cluster; it is not an all-task regression guarantee. The hierarchy and lessons are frozen before held-out testing, while routing uses the task and observable base execution without the hidden grader. On the disjoint-application-family test the router chooses the base harness for every task: this supports fallback preservation, not transfer of the specialized subclasses. Single-run ablations limit causal isolation of inheritance and added search.

[Primary full text, v1](https://arxiv.org/html/2610.28380v1): Sections 3.1–3.5, 5.1 and 5.3; limitations. [Identity and submission history](https://arxiv.org/abs/2610.28380v1).

### HERD: HERD: Harness-Evolving Recursive Distillation for Continual Learning

**First posted:** 2026-10-22. **Category:** Model and Policy Training, Harness Co-Evolution, and Distillation.

Evolves external textual skills, distills a teacher with privileged skills and verified answers into a new LoRA adapter, and merges the adapter into the task model. Prior-checkpoint and original-model anchors constrain drift; bounded residual examples serve as probes rather than replay training targets. The skill writer remains a fixed base checkpoint, and deployment uses model weights without the skills. Evaluation uses one model with known task boundaries and verified training answers. This is continual parameter learning coupled to harness evolution, not weight-free memory RSI or a demonstrated self-evolving skill writer.

[Primary full text, v1](https://arxiv.org/html/2610.31401v1): Sections 2.2–2.4 and 3.1–3.3; limitations. [Identity and submission history](https://arxiv.org/abs/2610.31401v1).

### MCCL: Memory-Centric Continual Learning for AI Agents

**First posted:** 2026-10-21. **Category:** Surveys, Definitions, and Conceptual Frameworks.

Proposes a substrate–asset–policy taxonomy and distinguishes inner-loop memory-state updates from outer-loop changes to memory-management policy. Its evaluation framework separates retention, adaptation and transfer using stateful/reset comparisons, delayed re-probes, interference and explicit budgets. The scaling discussion and evaluation protocol are conceptual proposals, not new benchmark evidence that memory universally produces continual learning. It supplies a vocabulary and test design for assessing retained improvement guidance, rather than an additional demonstrated harness intervention.

[Primary full text, v1](https://arxiv.org/html/2610.29357v1): Sections 2, 3.5 and 4. [Identity and submission history](https://arxiv.org/abs/2610.29357v1).

### BEAM: Memory as Belief: Bayesian Evolution of Memory for Self-Evolving LLM Agents

**First posted:** 2026-10-18. **Category:** Memory, Context, Skills, and Experience Reuse.

Maintains reusable memories and trains a context-dependent Bayesian memory-value estimator with LoRA and a Beta head while holding the task-executing model fixed. Semantic retrieval and Thompson sampling select memories; post-task leave-one-out counterfactual feedback updates their predicted value for future tasks. Thus fixed executor weights do not mean that every learned component is weight-free. Cross-task initialization from MATH500 to AIME includes further target adaptation, not unchanged zero-shot transfer. Consecutive-stream gains alone do not establish retention against forgetting, and counterfactual evaluation has a separate compute cost.

[Primary full text, v1](https://arxiv.org/html/2610.25119v1): Methodology (memory formation, belief representation and update); Experiments (cross-task transfer); Appendix A. [Identity and submission history](https://arxiv.org/abs/2610.25119v1).

### VeriEvolve: VeriEvolve: Evaluator-First Evolution for Tool-Using Agents

**First posted:** 2026-10-21. **Category:** Generalization, Evaluation Methodology, and Safety.

Builds executable evaluators from instruction-grounded positive, negative and adversarial end states, freezes an evaluator during workflow search, and revises it between searches using counterfactual pairs and cumulative regression cases. The external MCPMark verifier is hidden from model roles but used for admission, calibration and reference outcomes; the process is not verifier-free. The controlled study concerns filesystem tasks, and agreement on generated challenges is distinct from held-out agreement. A single search campaign without a fixed-budget search control limits attribution of gains specifically to evaluator evolution.

[Primary full text, v1](https://arxiv.org/html/2610.29005v1): Sections 3, 4.1–4.3 and 5–7; limitations. [Identity and submission history](https://arxiv.org/abs/2610.29005v1).

## Screening and limits

World2HOSI, a previously pending application candidate, was inspected in Sections 3.1–3.4. Its state management, orchestration and motion refinement did not establish a retained harness or improver revision in the inspected method, so it was not added as direct harness-evolution evidence. Selm (arXiv:2610.24630) remains pending full mechanism/evaluation screening. This is a targeted update, not an exhaustive search or independent reproduction. Preprint interpretations may change with revisions or clarifications.
