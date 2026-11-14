# Literature synthesis — November 14, 2026

Seventeen new bibliography papers and three revised existing works were inspected. The evidence dataset adds 14 records (159 total); four new contextual papers do not create empirical outcome records. This targeted update is not exhaustive.

## Comparisons that changed

- **Acceptance and validity:** sequential error control, falsification/regression probes and verifier construction address different failure sources; their assumptions are not interchangeable.
- **Continual behavior and cost:** backward losses, pre-feedback scoring, bounded memory baselines and full token accounting prevent endpoint gains from standing in for sustained improvement.
- **Transfer and training:** independently reoptimized models, student-specific frozen libraries, hardware-conditioned warm starts and learned policies are recorded as distinct regimes.

## Inspected evidence

### HarnessFlow

Uses MCTS over executable harness variants; a coding agent edits prompts, tools and control code using archived validation scores and trajectories. Combining exploration and exploitation improves reported validation-guided search results over either extreme; the comparison matches candidate attempts, not every source of computation.

Five executions per candidate are not five independent search runs. Search is rerun for the second model, so this is not unchanged cross-model transfer; reported inference costs exclude one-time search costs. [Primary source](https://arxiv.org/html/2611.06254v1), Sections 2–4.3; Tables 3–4; Appendices C–D.

### TRUST

Places an online statistical gate around fixed-proposer harness updates, using e-values, adaptive error-budget allocation and a correction for validation reuse. Reported acceptance error is lower than greedy acceptance across the tested settings; the conditional statistical guarantee and empirical test results must remain distinct.

The error-control result depends on a conditional mean bound and overlap-bias specification; tolerated loss is not a guarantee that each accepted edit improves. Empirical zero-tolerance error differs from the theoretical tolerance-adjusted quantity. [Primary source](https://arxiv.org/html/2611.10787v1), Sections 3–7; Table 1; Section 6.2.

### MULTILOOP

Optimizes executable multi-agent search loops and keeps an archive of code and training performance; improvements include prompts, tools and coordination code. The evolved loop improves fully correct answers over reported single-agent baselines, but persistent coordination failures and unequal inference cost limit attribution to multi-agent orchestration.

The single-agent/multi-agent comparison is not compute matched. Evaluation uses one benchmark; orchestration failures largely persist despite gains from prompt formatting and tool changes. [Primary source](https://arxiv.org/html/2611.15754v1), Sections 2–4; Appendix B.

### JoMoHa

Jointly trains an Engineer that generates harness programs and a Solver that executes them, using shared rewards, collaboration-aware critics and asymmetric policy updates. Frozen-policy and fixed-harness swaps support contributions from co-adaptation; gains cannot be attributed to harness edits with unchanged executor weights.

Both policies change weights. Most external baseline scores are taken from Harness-R1; only JoMoHa and WHALE are evaluated locally. Freezing the Engineer parameters still permits fresh program sampling. [Primary source](https://arxiv.org/html/2611.11499v1), Sections 4–6; Section 6.2.

### RSI Tax

Evaluates continual harness methods prequentially and accounts for proposer, execution and verification tokens; a bounded periodic-note baseline tests low-cost persistent adaptation. A small periodic-note baseline matches or leads reported accuracy while using substantially fewer tokens than heavier methods; verification dominates much of the measured improvement overhead.

The evaluation uses fixed task orders and few repeated runs. An artifact not used later is not proof its generation was causally wasted; token totals are not monetary cost. Terminal task order is not measured environmental drift. [Primary source](https://arxiv.org/html/2611.13524v1), Sections 2–6; Tables 2–3.

### Flex-RSI

Alternates an executor that improves a task solution with an improver that edits executor and improver harness code and prompts under protected validation and hidden-test evaluation. Editing the harness beats a frozen harness in six of seven reported paired settings, with one tie; this limited ablation does not establish uniform gains across the full benchmark.

Agent backbone weights remain fixed, but some task solutions train helper models. Most model/task configurations have one run; the frozen-harness comparison covers seven pairs, not all benchmark settings. [Primary source](https://arxiv.org/html/2611.08946v1), Sections 3.2–4.1 and 5.4; Tables 8–9; Section 6.

### FGSE

Represents lessons as scoped, verifier-aware hypotheses and tests temporary updates with transfer, falsification and regression probes before commit, refinement or rejection. Removing falsification probes raises reported harmful-update rates, and removing the regression archive increases regression damage; probe type matters beyond simply adding verification calls.

Reliability depends on executable verifiers and probe coverage. The theoretical bound requires fresh final probes and a finite conditionally fixed candidate set; it is not unconditional safety for arbitrary updates. [Primary source](https://arxiv.org/html/2611.14326v1), Sections 3–6; Tables 2 and 6; Appendices C–D.

### Failure traces and portable skills

Compares teacher-written portable skill notes derived from target-agent failure traces with a same-budget-ceiling teacher that sees no episode-specific trace. Trace-conditioned notes improve generated sealed-decision accuracy over the no-episode control, but the official retail task estimate is negative with an interval spanning zero; no interactive success gain is established.

Actual searches are not identical despite common ceilings. Improvements on generated sealed decisions do not carry to official interactive-task success; other tested domains have null results or data defects. [Primary source](https://arxiv.org/html/2611.11342v2), Sections 2–4; Table 1.

### Student-Aware Teaching

Maintains a student profile, diagnoses failures with probes and writes validated executable skills for a frozen student; the teacher is absent at deployment. Student-aware teaching improves reported held-out performance over student-agnostic teaching; library swaps show that the same skill collection is not equally effective for every student.

Primary evidence uses one teacher/student pair and custom task suites. Control runs are separate jobs rather than perfectly paired experiments; transfer depends on the receiving student and selector. [Primary source](https://arxiv.org/html/2611.13144v1), Sections 3–6; Tables 2–3 and 5–6.

### Veritas

Generates task-grounded verifier programs using evidence contracts, domain rules and authoring principles; candidates are revised by a model or researchers and selected on validation agreement. Authoring-principle ablations support better reported verifier agreement, while model transfer is positive in most but not all settings; neither result establishes universally reliable verification.

Some main results use tasks involved in mechanism development. Terminal evaluations are the closest held-out results. Pairwise judging sees candidates, unlike execution-verifier generation; oracle agreement is not task-solving improvement. [Primary source](https://arxiv.org/html/2611.13336v1), Sections 3.1–4.5; Tables 3–4; Limitations.

### InfraRSI

Co-optimizes training launch configurations and code under fixed workload contracts, fits time/memory surrogates from trials and stores verified, hardware-conditioned experience for later searches. Filtered cross-hardware experience improves final speedup and convergence on the reported target workload relative to cold start and unfiltered eligible packs; the transfer evaluation covers one target workload.

Auxiliary surrogates are fitted; the optimized workload itself trains models. Predeclared loss tolerances vary by task and do not prove unchanged final model quality. Cross-hardware reuse warm-starts further search rather than directly deploying an unchanged configuration. [Primary source](https://arxiv.org/html/2611.11558v1), Sections 3–6; Tables 5–6; Appendix A.

### Continual harness forgetting

Sequentially evolves coding harnesses on two task types, then replays earlier tasks to measure forgetting and inspect verification, workflow and budget conflicts. Second-stage evolution can sharply reduce success on earlier sampled tasks; inspected conflicts show why current-task gains alone do not establish continual retention.

Experiments sample 50 SWE-Bench Verified, 50 SWT and 30 FeatureBench tasks with one backbone. Replayed evolution tasks are not a separate held-out generalization test; SWT prompts are paraphrased to remove lexical shortcuts. [Primary source](https://arxiv.org/html/2611.03219v1), Sections 3–4; Appendices A–B.

### Teacher-free skill and policy co-evolution

Alternates validation-gated external skill-rule edits with GRPO LoRA policy training; the base model remains the editor even when the executing policy is adapted. The final rule/weight swap comparison supports complementary contributions from external skills and adapted policy weights; it does not show that the editor itself improves across generations.

Teacher-free does not mean fixed executor weights or a learned successor editor. The empirical edit gate is not a calibrated statistical test, and the two-round study does not establish long-run stability. [Primary source](https://arxiv.org/html/2611.15268v1), Sections 4–6; Tables 2–3.

### Multi-Task Self-Evolving Harnesses

Runs the same frozen model and current harness as solver and proposer; edits code and evolution notes after mixed-domain batches, then continues on Claw-Eval with replayed success anchors. Two stronger backbones improve mean in-domain scores, one has uncertain gains and another regresses; out-of-domain improvement is uneven. Success-anchor replay is a design choice, not a guarantee against forgetting.

Acceptance checks executability rather than performance. Gains depend on backbone and task; the out-of-distribution mean is driven largely by BrowseComp-Plus. Only one model has three independent first-stage search runs. [Primary source](https://arxiv.org/html/2609.38372v2), Sections 3–6; Tables 3–5; Appendix D.

## Contextual bibliography additions

- **EvoX:** A Rust runtime organizes action realization, execution continuity and outcome grounding. The controlled runtime comparison disables memory, evolution and extensions, so it is architectural evidence rather than a demonstrated recursive-improvement loop. Sections 3–5.6. [Primary source](https://arxiv.org/html/2611.15006v1).
- **Third Eye:** Tests whether a first-update winner remains a good choice after another update using separate selection/final tests. The intervention is small-model LoRA training, not harness revision; harm is model-dependent and the no-update control is not compute matched. Sections 3–5. [Primary source](https://arxiv.org/html/2611.12988v1).
- **Competition and RSI:** Analyzes competitive incentives for self-improvement using a stochastic two-actor game. This is a conceptual safety model, not an empirical demonstration of harness optimization or observed recursive gains. Section 4. [Primary source](https://arxiv.org/html/2611.10261v1).
- **AgentTorrent:** Collects public repository artifacts associated with coding agents. Configuration and planning files offer a resource for studying harness practice; detection and co-occurrence do not establish causal performance gains or autonomous evolution. Artifact detection and repository classification have distinct validation procedures. Sections IV–V. [Primary source](https://arxiv.org/html/2611.15436v1).

## Version and review boundaries

MemSkill v3 and RSI-Dojo v2 retain scoped outcome labels after rechecks. Multi-Task Self-Harness v2 receives a separate aggregate record; its v1 task records and historical atlas finding remain pinned. The broader bibliography has 335 papers and 11 resources. Dataset v0.5.0 has 126 works, 74 targeted AI-assisted checks and 59 observations; 85 inherited records and zero independent human adjudications remain explicit. See the dataset card and search log for all denominators.

The November 14 author reading PDF is separate from the posted Preprints.org v2. No platform resubmission or conference submission is implied.
