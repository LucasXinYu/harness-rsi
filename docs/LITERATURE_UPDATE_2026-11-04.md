# Literature and evidence update — November 4, 2026

Search window: October 25–November 4. This is targeted primary-source review, not an exhaustive census. Human adjudication and experimental reproduction are not claimed.

The bibliography grows from 305 to 318 papers (11 resources remain separate). Dataset v0.4.0 contains 145 records from 113 works, 60 primary-checked records and 45 scoped observations. The frozen 95-record October 1 atlas remains unchanged.

## What changes the synthesis

1. **Retain the right object.** Meta2 retains evolution guidance while resetting online edits; Skill++ shows why a growing skill library can lose routing coverage. Accumulating more artifacts alone does not establish learning.
2. **Separate warm starts from a better optimizer.** Continual AutoResearch finds faster initialization without a general post-initialization optimization advantage. SelfImprove-Bench separates replay, new instances, difficulty and capability transfer.
3. **Name all trained components.** OMCE learns a controller around a fixed LLM. Harness-S and RSI-Dojo train models; CARE also relies on external diagnosis and human promotion.
4. **Separate a valid successor from a beneficial one.** RSI-Env admits executable successors independently of capability gain. ParetoSaddler separates intermediate promotion from final development-set selection.
5. **Recheck behavior and costs.** Artifact-to-Capability exposes composition failures; Memory Tax reports task-dependent memory costs and model-swap sensitivity. EvoGroup distinguishes its own holdout evaluations from projected baseline scores.

## Source-level decisions

### Meta2

[Pinned primary paper](https://arxiv.org/html/2611.05139v1). Sections 3.2–3.3, 4.1 and 4.5; Appendix F.

Learns a reusable Meta-Skill from contrasted training trajectories; a frozen deployment evolver uses it to decide when to keep or edit a task-local harness.

Task-local reset outperforms retaining online edits across tasks on both reported benchmarks; this supports the retained-guidance boundary, not continually improving the optimizer. The Meta-Skill stays frozen at deployment; task edits and outcomes do not update it. Each backbone learns its own Meta-Skill, so multi-model results are not unchanged cross-model transfer.

Selection: Disjoint training/test tasks; privileged verifier feedback is training-only; reset seed harness for every test task.

### Harness-S

[Pinned primary paper](https://arxiv.org/html/2611.04277v1). Sections 3, 4.1, 4.4 and 4.7; Appendices A–B and G.

Evolves a fixed pool of complementary harnesses, routes rescue rollouts for base-harness failures, and uses their reward contrasts to train a shared policy with GRPO.

On AppWorld 4B, refreshed routing profiles outperform fixed profiles under equal rescue allocation; improvements also persist when the trained policy is evaluated under the original harness. Executor weights change. Equal per-task rescue allocations do not equal total sampling because failure frequencies differ; external harness transfer still depends on the execution interface.

Selection: Train tasks drive edits and policy learning; validation selects parents and refreshes routing profiles; test tasks are reserved for final evaluation.

### EvoGroup

[Pinned primary paper](https://arxiv.org/html/2611.03868v1). Sections 2, 3.1, 3.3 and 3.6; Appendix A.

Uses confidence/correctness buckets and selective trajectory inspection to revise memory representations, tools, execution checks and selection policies for shared group contexts.

Evolved tools and prompts yield the largest component gains, while successive updates still lose previously passed tasks. Self-reflection has weaker evidence consistency than localization agreement. Main-table external baselines are projections from full-benchmark category scores, not reruns on held-out question IDs. Frozen cross-benchmark transfer is distinct from unchanged cross-model transfer.

Selection: Stratified 30/70 EverMemBench evolution/holdout split; freeze the evolved harness before GroupMemBench transfer.

### ParetoSaddler

[Pinned primary paper](https://arxiv.org/html/2611.02079v1). Sections 4 and 5.1–5.3; Appendices F, G and L.

Uses repeated executions and Bayesian-bootstrap quality/cost screening to promote intermediate harnesses, then applies deployment preferences to the development-evaluated candidate set.

Replacing mean-based promotion with Bayesian screening yields better reported ClawMark quality/cost endpoints. An additional GAIA2 search run supports limited run-to-run stability. Bootstrap uncertainty covers execution variation on fixed screening tasks, not task-sampling uncertainty. Repetition adds evaluation cost; test-repeat variability is not independent search-run variability.

Selection: Domain-disjoint train/development/test partitions; select final cost/quality endpoints on development data; three test repeats per frozen harness.

### Continual AutoResearch

[Pinned primary paper](https://arxiv.org/html/2611.05108v1). Sections 3, 5 and 6.

Compares native CLI agents that retain conversation, files and experiment artifacts across task streams with the same agents reset before each task.

Continual agents improve time-to-convergence AUC, but removing first-valid-submission reward removes the observed advantage; this does not establish a better subsequent optimizer. Gains mainly concern faster initialization; final rewards are mixed. Four of five agents have only one matched run pair; cross-agent differences combine model and harness effects.

Selection: Training/development feedback is visible; hidden test evaluates saved submissions after execution. First stream tasks are excluded from transfer summaries.

### SelfImprove-Bench

[Pinned primary paper](https://arxiv.org/html/2611.02797v1). Sections 3–4; Appendix A.

Separates replay on historical instances from new-instance, harder-task, new-game and cross-capability transfer, while tracing which artifacts self-improving agents modify.

Historical-instance replay regresses in 8/18 method-task pairs while new-instance transfer improves in 16/18; retained artifacts and trajectory scores need separate reevaluation. Six game environments bound the conclusions. Transfer is asymmetric; the main retained edits contain no meta-optimizer changes, unlike a separately prompted exploratory variant.

Selection: Build a disjoint held-out descriptor pool before training; select harnesses from training feedback and freeze them during replay/transfer evaluation.

### RSI-Env

[Pinned primary paper](https://arxiv.org/html/2611.01736v1). Sections 3–4; Appendix A.

A protected host controller manages a persistent model/harness/research-state successor loop; self-improvement and fixed external-teacher settings can edit harnesses and train models.

Open-General Self improves GPQA and AIME while lowering SimpleQA and Terminal-Bench performance; an executable successor is not a monotone improvement across capabilities. Successor registration checks validity and executability rather than capability gain. Some settings train weights; actual runtime differs substantially despite the same maximum allocation.

Selection: Register valid executable successors independently of capability scores; separately evaluate four capability benchmarks under three feedback regimes.

### OMCE

[Pinned primary paper](https://arxiv.org/html/2611.01747v1). Sections 3–4 and Limitations; Appendix G.

An online contextual-bandit controller chooses direct execution, episodic reuse, guidance reuse or distillation; task feedback updates both memory and routing statistics.

Continuing controller updates improves first-attempt success in all four freeze comparisons, but BigCodeBench four-attempt success is lower than with the frozen controller. The LLM is fixed but the auxiliary controller learns. Only the chosen route supplies feedback; results rely on timely rewards and differ between first-attempt and four-attempt success.

Selection: Sequential task feedback updates state; matched memory snapshots and midstream controller-freeze ablations separate routing adaptation from memory growth.

### Skill++

[Pinned primary paper](https://arxiv.org/html/2611.00544v1). Sections 3.2 and 4; Limitations.

Refines incoming skill names/descriptions with contrasts and scope exclusions while preserving skill bodies and earlier metadata, reducing routing interference in growing libraries.

Removing differentiation, scope exclusions or name clarification lowers SRA-Bench routing coverage. Reported gains across routers concern skill selection rather than solved-task accuracy. Full-coverage-at-five is skill selection, not end-to-end task completion. Evaluation is text-only; continual retriever-training baselines must not be confused with the metadata-only method.

Selection: Ten class-incremental sessions; synthetic body-derived queries guide refinement without evaluation queries or labels; evaluate nine library-growth checkpoints.

### Artifact-to-Capability

[Pinned primary paper](https://arxiv.org/html/2611.04952v1). Sections 3–5 and Limitations.

Replays frozen Reflexion, Voyager and DGM artifacts on controlled Gomoku states to test whether stored memories, skills and code actually produce intended behavior.

The Voyager case contains useful skills but their calling order overrides winning behavior; DGM versions show loss-only drift. Artifact validity and historical scores do not guarantee retained capability. One game, one executor and adapted implementations limit external validity. A diagnostic state set partly comes from DGM trajectories; findings do not estimate prevalence across all self-evolving agents.

Selection: Freeze evolved artifacts before fixed-state replay; compare artifact versions on common state obligations rather than historical trajectory scores alone.

### CARE

[Pinned primary paper](https://arxiv.org/html/2611.02839v1). Sections 3.3, 5.2, 7.2–7.4, 8.1–8.2 and 9.4–9.6.

Attributes production failures to model behavior or external components, trains verified model-behavior repairs by on-policy self-distillation, and gates promotion through frozen simulation, online comparison and human approval.

Combined offline scores increase, but simulation accuracy and bad-case rates trade off. Final online satisfaction differences from the incumbent are not statistically significant. Harnesses also change between versions, so trends cannot isolate model updates. Satisfaction parity is not statistically significant superiority; retrospective bad-case rates and selected ablations have calibration limits.

Selection: Evaluate all versions on 559 frozen current-SOP cases; compare candidate/incumbent concurrently online; accountable humans approve promotion.

### RSI-Dojo

[Pinned primary paper](https://arxiv.org/html/2611.03698v1). Sections 3–5 and 7.

Builds runnable post-training environments, improves collection guidance, filters execution trajectories, and fine-tunes agents to train target models.

Fine-tuned agents outperform their own starting models on PostTrainBench and Lite. This is evidence for learning post-training workflows, not autonomous recursive acceleration. This trains an improver but does not close a successor self-improvement loop. Official leaderboard hardware differs; hosted/self-hosted tool access also differs.

Selection: Filter trajectories for behavior and measured outcome; evaluate trained agents under the standard AutoTrainess harness without added collection guidance.

### Memory Tax

[Pinned primary paper](https://arxiv.org/html/2610.34073v1). Sections 3.1, 4.2–4.4, 5.1 and Limitations; Appendix A.4.

Compares transformed memory systems with raw-history retrieval and probes information preservation, retrieval accessibility and construction/answering backbone sensitivity.

Many memory systems underperform raw-history RAG and amplify backbone sensitivity, while distilled experience can help web tasks. The effect depends on task and system, not memory presence alone. Retrieval-scope alignment is not equal absolute token cost. Representative systems, sampled offline English benchmarks and model-dependent judging limit generalization.

Selection: Construct and evaluate memory separately; experiential-memory experiments freeze training-derived memory before test evaluation.

## Existing revision and pending work

KARMA v2 (November 2) preserves the inspected 23/30 positive cross-domain transfer result. Its offline action-agreement scope, validation gate and limits were rechecked; this is not evidence of production revenue or fairness improvements. Historical v1 extraction remains in dataset v0.3.0.

Four arXiv queries returned 220 unique works: 22 already collected, 13 included and 185 pending. Fourteen older pending candidates remain outside that result set. No new category was necessary. Existing 85 legacy records and all human adjudication tasks remain explicitly unfinished.

The November 4 reading manuscript and dataset are companion versions. Updating them does not replace the October 30 Preprints.org v2 or any submitted review-system manuscript.
