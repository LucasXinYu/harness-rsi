# Harness RSI Evidence Dataset

## Release and scope

- Version: **0.1.0**, released **2026-10-18**.
- Evidence cutoff: **2026-10-01**; original evidence export: **2026-10-10**.
- Unit: **one source within one task subcategory**, not one edit, trial, or independent effect.
- Coverage: **95 records**, **63 distinct sources** (62 research papers and one benchmark resource), four domains and 20 task subcategories.
- Structured outcome/retention screening: **4 of 95 records**, containing **6 scoped signals**. The other **91 records are not reviewed for these labels**.

This is a curated dataset of **reported** harness changes and outcomes, not a new benchmark, an exhaustive experiment log, or an independently reproduced collection of causal effects. The living bibliography is a separate, broader collection that includes surveys, adjacent methods, and benchmarks; new literature entries do not automatically enter this dataset.

## Files and stable versions

The website publishes `dataset/v0.1.0/dataset.json`, `records.jsonl`, `records.csv`, `schema.json`, `checksums.json`, `citation.bib`, and this card. `dataset/latest.json` is a convenience pointer, not a reproducibility pin. Cite and download a versioned path and retain its checksums. The repository also retains the unchanged original `docs/evidence.json`.

Each JSON/JSONL row contains the original record and additive annotations. CSV has the same 95 record units; nested arrays are JSON-encoded within cells, and null is written as `null`. Parse nested cells with `json.loads`; a CSV row is not an individual signal.

## Fields and interpretation

| Field | Meaning |
| :-- | :-- |
| `id`, `key` | Stable category-source identifier and bibliography citation key. Repeated keys are related contexts, not independent replications. |
| `domain`, `category`, `category_id` | Task organization, not a claim that domains are disjoint. |
| `sections` | Curated starting configuration, reported evolution, outcomes, and limitations. |
| `sources` | Versioned primary-source URLs and section/table/appendix locators. |
| `benchmarks` | Original memberships and study/transfer/evaluation/case roles. Membership does not assign every claim to every benchmark. |
| `annotation_status` | `record_screened` or `not_reviewed`; screening is a new pass over curated record text, not a new primary-source audit. |
| `signals` | Zero or more scoped observations. Empty means not screened, not “no regressions.” |
| `signals[].outcome` | `improvement`, `regression`, `no_gain`, `mixed`, or `not_assessed`. Usage alone does not establish a performance effect. |
| `signals[].retention` | `retained`, `rejected`, `rolled_back`, `not_reported`, or `not_assessed`. Use `not_reported` only after explicitly checking the relevant reporting scope. |
| `signals[].attribution` | Case, full-system comparison, reported proposal test, usage observation, component ablation, or not assessed. These are different evidential designs, not an ordinal quality score. |
| `signals[].components` | Instructions, tools, context, memory, and/or control implicated by the observation; these tags do not establish separate causal effects. |
| `signals[].benchmark_ids` | Explicit applicability. An empty list means the annotation is not assigned to a benchmark; it does not mean all benchmark memberships. |
| `signals[].scope` | Particular comparison, case, metric direction, or restriction necessary to interpret the label. |
| `signals[].section`, `evidence_quote` | Exact supporting excerpt of the **curated record**, not necessarily a verbatim quotation from the original paper. |
| `signals[].source_index`, `primary_source` | Link back to an existing source and its locator. Source identity is inherited, not invented. |
| `selection_protocol`, `controlled_variables` | Reserved for systematic extraction. Currently null for every record: **not assessed in this pass**, not absent in the paper. |

## Collection and annotation process

The base records were extracted for a literature survey using targeted discovery and reference following, with inclusion based on concrete reusable harness changes and related evaluation contracts. Bibliographic curation, benchmark membership, and comparative observations are maintained separately. See `CONTRIBUTING.md` for source verification and correction procedures.

For this initial structured-label release, an AI assistant manually screened four existing records containing explicit outcomes or useful boundary cases. Each signal has an exact supporting record excerpt, scope, attribution label, retention label, and inherited primary-source locator. This is a deliberately selected pilot, **not a random sample**. It does not constitute a fresh reading of every primary source. No independent dual annotation, inter-annotator agreement study, or full 95-record outcome audit has been performed for this layer. Human maintainers remain responsible for editorial acceptance.

Validators check record IDs, vocabularies, exact excerpt matches, benchmark restrictions, source indices, frozen-source hash, and cross-format consistency. Passing validation establishes structural consistency, not scientific truth.

## Negative results and missingness

Preserve reported regressions, failed proposals, rollbacks, and null results rather than keeping only final winners. Keep outcome, retention, and usage separate: a tool with zero measured use is not automatically a harmful tool. Do not turn a full-system result into a component ablation, or move a case into a different benchmark.

`not_reviewed` and null differ from a verified “not reported.” The pilot cannot estimate the prevalence of failures. The literature may omit unsuccessful searches, and we do not observe the full denominator of attempted edits. This dataset therefore cannot remove publication bias or support a global intervention success rate. Fixed tasks alone also do not control model changes, compute budgets, selection leakage, or simultaneous interventions.

## Intended use and limits

Use the dataset for tracing source-backed design changes, comparing evaluation practices, investigating reported trade-offs, and identifying missing evidence. Filter by scope and attribution before analyzing signals. Do not use raw record or signal counts as independent effect counts, rank methods as a common leaderboard, or claim causal component benefits without the appropriate experimental evidence. Retention is not the same as effectiveness.

## Rights and citation

**No dataset-specific reuse license has been granted.** Public download does not imply permission for unrestricted redistribution or commercial use. Source papers, code, fonts, and other materials retain their respective rights. A license choice requires maintainer approval; this release does not silently apply CC BY, CC0, or a software license to the collection.

Use the versioned `citation.bib` for a dataset citation. There is currently no dataset DOI; do not invent one or imply that the survey is accepted or published. Dataset authorship is credited to the Harness RSI project team; AI assistance is documented separately, not listed as a scholarly author.

## Corrections and future releases

Submit a source-backed evidence correction through the repository issue template, giving record ID, source version, locator, proposed label, scope, and rationale. Change labels only after reviewing their support and downstream comparisons. Preserve the original survey snapshot; expand this annotation pilot in a new dataset version with updated coverage, card, checksums, and release notes. New papers must undergo evidence extraction before they can expand the frozen-record dataset.

Run `python3 examples/inspect_dataset.py --outcome regression` to inspect scoped regressions locally. This example summarizes disclosed observations; it does not calculate a success rate.
