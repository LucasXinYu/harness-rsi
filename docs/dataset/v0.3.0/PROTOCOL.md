# Harness RSI evidence curation protocol

Protocol version 0.3, documented November 1, 2026. This documents a retrospective curation process; it was not preregistered.

## Research questions and units

For each reported agent-system change ask: what is editable, what feedback selects it, what persists, what is trained, and what comparison supports the result? One record is a source in a task subcategory. One signal is a scoped reported observation within that record. Neither unit is an independent experiment. Repeated citation keys must be grouped when analyzing studies.

The broader bibliography includes methods, surveys, benchmarks and adjacent training work. Evidence membership requires an identifiable mechanism and an inspectable evaluation or failure case. A larger bibliography does not imply a larger evidence corpus.

## Discovery and eligibility

Use primary arXiv papers, proceedings, OpenReview and author-released artifacts. Search with overlap from the previous completed horizon, including harness/workflow evolution, memory/skill revision, continual adaptation, evaluation and model/data transfer. This is targeted discovery and reference following, not an exhaustive systematic review. Preserve actual queries, dates, failures and decisions. Do not report a PRISMA flow or recall estimate without the required search records and denominator.

Include reusable changes to instructions, tools, context, memory or execution control; include evaluation studies of those changes. Coupled weight-training studies may be included only with an explicit training boundary. Exclude task outputs alone from claims of retained harness change. Environment wrappers that reshape training signals while leaving the task agent harness unchanged are adjacent work. Conceptual surveys remain in the bibliography and screening ledger, not empirical outcome counts.

Deduplicate by canonical DOI/arXiv identity, then title and author inspection. Versions of one paper remain one source. If primary metadata and the manuscript disagree, retain the discrepancy and document the resolution. The Trinity's Atom author list concatenates Wangbo Zhao and Kaipeng Zhang; the separate names in manuscript Section 8 are used.

## Extraction and scientific distinctions

Record a pinned primary URL and section/table/figure locator. Keep first-release date, inspected-version date, metadata-check date and claim-review date separate. Unknown dates remain null or retain their original precision. A search-through date is not an assertion that every record was re-audited on that date.

For each new signal record its setting, comparison, outcome, retention, attribution, relevant components, applicable benchmarks, and limits. Extract selection rules and controlled variables only when inspected; a null means not assessed, not absent. Do not label an item not reported unless the relevant reporting scope was checked.

- Fixed executor weights do not imply that a router, memory policy or auxiliary model is untrained.
- Unchanged cross-model transfer, independently re-evolved harnesses, trained-policy transfer and target-domain adaptation are different regimes.
- Stream-level improvement does not establish retention or absence of forgetting; inspect delayed probes and backward effects.
- Accepted in one round does not imply retained in the final artifact.
- Full-system comparisons, component ablations, proposal tests, illustrative cases and edit-outcome statistics support different claims.
- A tool-use count is not an effectiveness measure. HarnessX's affected-task hit-rate is not invocation frequency.
- Costs and times measured on common solved tasks have a different denominator from solve rates.
- Preserve unsuccessful proposals, regression, fallback routes, compute changes and unavailable artifacts.

## Review states

`legacy_curated` means narrative evidence inherited from v0.1.0 without a new primary-text audit in this release. `primary_source_checked` means targeted AI-assisted inspection of the stated claim, protocol and limitations against the pinned source. It does not certify every sentence in the paper or reproduce an experiment. `human_review_status: pending` is explicit: no independent human adjudication or inter-annotator agreement is claimed.

Six source-version migrations are review events, not six invented outcome signals. A mechanism/protocol review can have no coded outcome; absence of a signal is not evidence of no gain. Short support excerpts are exact normalized-text anchors; their automatic match is a traceability check, not proof of the interpretation.

For a human audit, sample by domain, attribution, training boundary and outcome, then have two researchers independently label blinded copies. Adjudicate disagreements with a source locator, retain both original labels, and report denominators and per-field agreement. Do not calculate agreement from two runs of the same assistant or assign human review retroactively.

## New category boundary

The dataset adds `cross_domain / multi-domain-agent-evaluation` for aggregate claims spanning incompatible task categories: e.g. MaD-RSI's joint executor evaluation, HERD's sequential stream and Trinity's multi-benchmark comparison. A single-domain result such as the Selm SpreadsheetBench ablation remains in its task category. Do not duplicate the same aggregate into several domains. The historical four-domain survey atlas remains a distinct frozen artifact.

v0.3.0 adds three task categories without reclassifying old records:

- `reasoning / multi-objective-combinatorial-optimization`: search procedures for combinatorial solution quality/runtime trade-offs, such as HEMO. Excludes ordinary mathematical question answering and weight-only solvers.
- `interactive / embodied-navigation`: agent movement and place/route memory, such as EvoLife. Excludes object manipulation and single-image perception.
- `visual / compositional-3d-reconstruction`: executable scene construction from visual evidence, such as SceneEvolve. Excludes 2D image generation and merely describing a scene.

These are dataset task distinctions, not claims of new RSI mechanisms or a revision of the manuscript taxonomy. Method categories in the bibliography remain unchanged. MolRSI and RecRSI fit machine-learning engineering because they search scientific/recommender training workflows; RSIV fits program generation because it produces executable visualization programs.

## Analysis and reuse

Use the normalized tables and join by `record_id`, `signal_id` and citation `key`. Signals can share sources, cases and observations. Do not pool raw improvements, treat missing signals as failures/absence, estimate global success rates or rank incompatible benchmarks. This is an evidence resource, not a training/evaluation benchmark; there is no fabricated train/test split. The HF split is named `data`.

Primary papers are linked, not redistributed. The release includes project-authored curation, minimal support anchors and metadata. Its rights notice distinguishes project contributions from third-party material. The maintainer authorized CC BY 4.0 on October 31, 2026 for project-owned annotations and compilation only; see LICENSE-DATA.md.

## Reproducibility and corrections

Source JSON is authoritative; build exports deterministically, validate JSON Schema and relational constraints, verify frozen-release hashes and compute a complete manifest. Archive corrections with old and new IDs, reason, version and locator. Keep all published versions immutable, including its superseded interpretation, with a visible correction notice in the current release. Publish a versioned release and check the actual downloaded HF/GitHub payload before marking synchronization complete.

Documentation follows the questions in [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) and the [Hugging Face Dataset Card guidance](https://huggingface.co/docs/hub/datasets-cards); this is not certification by either organization.
