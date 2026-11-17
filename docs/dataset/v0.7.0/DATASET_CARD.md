# Harness RSI Evidence Dataset

## Status and purpose

**v0.7.0, November 17, 2026.** Maintained by the Harness RSI project team as a companion to *From Harness Optimization to Recursive Self-Improvement: A Survey of Language Model Agents*. Xin Yu leads the project. Codex assisted search, extraction and validation; it is not a scholarly author. No additional funding is asserted for this dataset release.

This resource documents what agent harnesses change, how changes are selected, what outcomes are reported, and what the evidence cannot establish. It is a curated evidence collection, not a new benchmark or a collection of reproduced experiments.

## Composition and coverage

| Quantity | v0.1.0 | v0.2.0 | v0.3.0 | v0.4.0 / v0.4.1 | v0.5.0 | v0.6.0 | v0.7.0 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Category-source records | 95 | 113 | 132 | 145 | 159 | 162 | 166 |
| Distinct works | 63 | 81 | 100 | 113 | 126 | 129 | 133 |
| Records with structured signals | 4 | 22 | 30 | 43 | 57 | 60 | 64 |
| Scoped signals | 6 | 24 | 32 | 45 | 59 | 62 | 66 |
| Documented primary-source checks | Not claimed | 28 | 47 | 60 | 74 | 77 | 81 |
| Inherited records without a new primary audit | 95 | 85 | 85 | 85 | 85 | 85 | 85 |
| Populated selection/control fields | 0 | 28 | 47 | 60 | 74 | 77 | 81 |
| Independently human-adjudicated records | Not claimed | 0 | 0 | 0 | 0 | 0 | 0 |

This release adds four works to v0.6.0. Each contributes one comparison with explicit controls, a primary-text locator and a statement of its limits. The bibliography contains 343 papers and 11 resources. The 95 records in the original October atlas and all prior versioned exports retain their original contents.

## Collection and review

The November 8–17 submission-date search returned 144 distinct arXiv IDs across four queries. We supplemented it with cs.AI, cs.CL and cs.LG announcement titles, and checked earlier candidates against their full texts. The search log reports the query counts, URLs, version checks and the pending queue size (397).

ELITE separates downstream evaluation from structural validity during evolution. The small-model harness study tests six completion checks jointly and reports an interval spanning zero. EasyFoam tests a frozen skill library on new tasks from families also present in development. ValidityMem tests memory filtering under simulated, matched error rates. Each result applies to its named benchmark and control condition.

Evidence uses pinned papers and locators. First release, inspected revision, metadata check and claim review are distinct dates. Full third-party papers are not distributed. Short support anchors and hashes identify inspected HTML renderings; arXiv can regenerate HTML without changing the PDF version.

`primary_source_checked` means AI-assisted inspection of the specified claim, protocol and limitations. It is not experimental reproduction or independent dual annotation. The 85 inherited records remain `legacy_curated`. Human adjudication is pending; no agreement statistic is fabricated. Automatic excerpt matching checks traceability, not scientific truth.

## Files and loading

`dataset.json` and `records.jsonl` preserve the nested representation; `schema.json` specifies it. `primary-checked.records.jsonl` contains only the 81 targeted primary-checked records. Seventeen have no structured outcome; use `signals.csv` for the 66 scoped observations. This subset is not independently human-adjudicated.

`sources.json`, `screening.json`, `search-log.json`, `corrections.json`, `quality-report.json`, `citation.bib` and `checksums.json` accompany every version. The v0.7.0 search log records its query counts, source URLs and pending queue size; the historical logs remain separately archived.

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
| `review-queue.csv` | 85 primary-source reviews and 81 human-adjudication tasks; reviewer fields are blank |

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
