# Harness RSI Evidence Dataset

## Status and purpose

**v0.6.0, November 16, 2026.** Maintained by the Harness RSI project team as a companion to *From Harness Optimization to Recursive Self-Improvement: A Survey of Language Model Agents*. Xin Yu leads the project. Codex assisted search, extraction and validation; it is not a scholarly author. No additional funding is asserted for this dataset release.

This resource documents what agent harnesses change, how changes are selected, what outcomes are reported, and what the evidence cannot establish. It is a curated evidence collection, not a new benchmark or a collection of reproduced experiments.

## Composition and coverage

| Quantity | v0.1.0 | v0.2.0 | v0.3.0 | v0.4.0 / v0.4.1 | v0.5.0 | v0.6.0 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Category-source records | 95 | 113 | 132 | 145 | 159 | 162 |
| Distinct works | 63 | 81 | 100 | 113 | 126 | 129 |
| Records with structured signals | 4 | 22 | 30 | 43 | 57 | 60 |
| Scoped signals | 6 | 24 | 32 | 45 | 59 | 62 |
| Documented primary-source checks | Not claimed | 28 | 47 | 60 | 74 | 77 |
| Inherited records without a new primary audit | 95 | 85 | 85 | 85 | 85 | 85 |
| Populated selection/control fields | 0 | 28 | 47 | 60 | 74 | 77 |
| Independently human-adjudicated records | Not claimed | 0 | 0 | 0 | 0 | 0 |

This release adds three works and three observations to v0.5.0. The observations measure a CodeSearch compression-schedule ablation, a FinMMR Easy memory ablation, and a SWE-Bench Pro performance–cost trade-off. Each applies to the model, benchmark and comparison named in the record. All six stable releases retain their original bytes.

The bibliography contains 339 papers and 11 resources. The frozen October 1 atlas contains 95 category–source records. The separately versioned evidence collection contains 129 works, including one benchmark resource.

## Collection and review

The last completed standard search was November 15. On November 16 the four date-bounded Atom queries returned HTTP 503 or 429. Three official arXiv announcement lists, primary proceedings, citation backtracking and the existing queue supplied targeted coverage. The updated search log gives the filters, dates, source URLs and queue size. The date on an announcement can differ from the submission date used for the bibliography timeline.

ModHarness-RL revises steering while training its policy and keeps its default compression program fixed. FinAcumen freezes its development memory bank during held-out evaluation. HarnessPro compares budget-specific harnesses using per-task execution cost. These studies support different claims about adaptation and cost. See the records for the pinned full texts and comparison conditions.

Evidence uses pinned papers and locators. First release, inspected revision, metadata check and claim review are distinct dates. Full third-party papers are not distributed. Short support anchors and hashes identify inspected HTML renderings; arXiv can regenerate HTML without changing the PDF version.

`primary_source_checked` means AI-assisted inspection of the specified claim, protocol and limitations. It is not experimental reproduction or independent dual annotation. The 85 inherited records remain `legacy_curated`. Human adjudication is pending; no agreement statistic is fabricated. Automatic excerpt matching checks traceability, not scientific truth.

## Files and loading

`dataset.json` and `records.jsonl` preserve the nested representation; `schema.json` specifies it. `primary-checked.records.jsonl` contains only the 77 targeted primary-checked records. Seventeen have no structured outcome; use `signals.csv` for the 62 scoped observations. This subset is not independently human-adjudicated.

`sources.json`, `screening.json`, `search-log.json`, `corrections.json`, `quality-report.json`, `citation.bib` and `checksums.json` accompany every version. The v0.6.0 search log preserves its query counts and pending identities; the historical logs remain separately archived.

Normalized tables avoid nested JSON strings inside CSV cells:

| Table | Unit and joins |
| --- | --- |
| `papers.csv` | One work, keyed by `key` |
| `records.csv` | One category-source record, keyed by `id`, linked by `key` |
| `signals.csv` | One observation, keyed by `signal_id`, linked by `record_id` |
| `record_sources.csv` | Source version and locator per record |
| `record_benchmarks.csv` | Record/benchmark membership and role |
| `record_controls.csv` | One inspected control condition per record |
| `signal_components.csv` | Signal/component relation |
| `signal_benchmarks.csv` | Explicit signal applicability |
| `reviews.csv` | Review provenance per record |
| `review-queue.csv` | 85 primary-source reviews and 77 human-adjudication tasks; reviewer fields are blank |

Flat JSONL files for papers, all records, the primary-checked subset and signals support separate HF configurations. The split is called `data`; no training/test partition is invented. Randomly splitting related literature rows would not produce a valid model benchmark.

```python
import json
from pathlib import Path
data = json.loads(Path("dataset.json").read_text())
for record in data["records"]:
    if record["review"]["status"] == "primary_source_checked":
        for signal in record["signals"]:
            if signal["outcome"] in {"regression", "no_gain", "mixed"}:
                print(record["id"], signal["summary"], signal["primary_support"]["url"])
```

Retain the versioned files, manifest and HF commit. A moving `main` or `latest.json` is not a reproducibility pin.

## Fields and missingness

- `annotation_status`: `record_screened` has signals; `record_reviewed_no_signal` has a version/mechanism check without a newly coded outcome; `not_reviewed` lacks a current structured-label pass.
- `selection_protocol`, `controlled_variables`: extracted only where inspected. Null plus `not_assessed` means not extracted, not absent in the paper. Controls apply to the stated comparison.
- `weight_update_boundary`: fixed executor, trained auxiliary policy, trained executor or unassessed. Fixed executor does not certify every component is frozen.
- `transfer_regime`: distinguishes same-model benchmark transfer, held-out models, target adaptation, transductive evaluation, sequential probes and other stated settings.
- Signal `outcome`: improvement, regression, no gain, mixed or not assessed, always with a comparison and scope.
- `retention`: retained, rejected, rolled back, not reported or not assessed. Acceptance in one round is not final retention.
- `attribution`: whole system, ablation, proposal test, edit outcome, usage, case or unassessed. These are designs, not a quality ranking.
- `evidence_quote` is an excerpt of our curated narrative; `primary_support.excerpt` is a short exact normalized-text anchor in the primary paper.
- Empty benchmark applicability does not mean every benchmark. Unknown dates remain null or retain original precision.

## Corrections

HarnessX's `unused-color-tool` is superseded by `color-tool-zero-hit-rate`: the paper measures affected tasks flipped to success, not tool invocation frequency. Zero is a scoped edit outcome, not an isolated causal test. See the pinned source, Figures 8 and 10, in the versioned `corrections.json`.

EvolveNet, TTHE, ModularRSI, RRSI and HarnessPAI have migrated versions/locators in six records. The old unpinned ModularRSI code observation is not represented as a current code audit. The Lean cost/time comparison is restricted to its common-solved subset. Historical v0.1.0 and v0.2.0 files remain unchanged; apply these correction notices when interpreting them.

## Uses, biases and limitations

Use the collection to trace design changes, compare evaluation practices and locate reporting gaps. Filter by review status and scope. Group repeated sources when analyzing studies. Human review is advisable before using an annotation as a pivotal scholarly claim.

The corpus is selected, English-dominant, rapidly changing and subject to publication and survivorship bias. Unsuccessful edits can be absent from papers. The review sample is purposive, not random, so its error rate cannot be extrapolated. Models, budgets, tasks, selection access and denominators differ. Do not pool raw improvements, rank methods on one leaderboard, treat empty signals as no failures, or estimate a global intervention success rate.

Public author names and attribution are retained. No private emails, credentials, private correspondence or participant-level data are distributed; no sensitive personal attributes are inferred. The collection does not establish the safety of autonomous self-modification.

## Rights, citation and maintenance

**CC BY 4.0 applies to project-owned original annotations and compilation only**, with explicit maintainer authorization on October 31, 2026. Third-party papers, excerpts and code retain their original rights and are not relicensed. See `LICENSE-DATA.md` for the scope and governing license link.

Use the exact version in `citation.bib`. No dataset DOI, peer-review certification or acceptance is claimed. Report corrections through [GitHub Issues](https://github.com/LucasXinYu/harness-rsi/issues) with record ID, source version, locator and interpretation. New releases require review, validation and preserved history. No unattended update cadence is guaranteed.
