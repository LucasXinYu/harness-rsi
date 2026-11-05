# Harness RSI Evidence Dataset

## Status and purpose

**v0.4.1 — corrected November 4, 2026.** Maintained by the Harness RSI project team as a companion to *From Harness Optimization to Recursive Self-Improvement: A Survey of Language Model Agents*. Xin Yu leads the project. Codex assisted search, extraction and validation; it is not a scholarly author. No additional funding is asserted for this dataset release.

This resource documents what agent harnesses change, how changes are selected, what outcomes are reported, and what the evidence cannot establish. It is a curated evidence collection, not a new benchmark or a collection of reproduced experiments.

## Composition and coverage

| Quantity | v0.1.0 | v0.2.0 | v0.3.0 | v0.4.0 / v0.4.1 |
| --- | ---: | ---: | ---: | ---: |
| Category-source records | 95 | 113 | 132 | 145 |
| Distinct works | 63 | 81 | 100 | 113 |
| Records with structured signals | 4 | 22 | 30 | 43 |
| Scoped signals | 6 | 24 | 32 | 45 |
| Documented primary-source checks | Not claimed | 28 | 47 | 60 |
| Inherited records without a new primary audit | 95 | 85 | 85 | 85 |
| Populated selection/control fields | 0 | 28 | 47 | 60 |
| Independently human-adjudicated records | Not claimed | 0 | 0 | 0 |

The 113 works comprise 112 papers and one benchmark resource. v0.4.0 adds 13 records and 13 scoped observations, and rechecks KARMA against its November 2 revision. A paper can appear in several categories; records and signals are not independent effects. The v0.4.1 patch corrects RSI-Env benchmark identities, narrows the Masked Erosion model-swap signal to AppWorld, qualifies HCL interactive acceptance, updates version-specific locators and ModularRSI authors, and normalizes Terminal-Bench 2.1 identifiers. Record and signal counts do not change. All four earlier releases remain byte-for-byte unchanged.

Targeted discovery runs through **November 4, 2026**, with a seven-day overlap beginning October 25. The new batch includes papers first posted October 25–November 3. The original survey atlas retains its **October 1** cutoff and 95 records. The broader bibliography contains 318 papers and 11 resources; it is a separate collection, not the dataset denominator.

The dataset spans coding, reasoning, interactive, visual and cross-domain settings. Existing task categories accommodate this batch; no new category or historical reassignment was needed. This release distinguishes retained guidance from task-local edits, router learning from fixed-executor behavior, promotion from deployment selection, and skill-routing accuracy from task completion.

## Collection and review

See `PROTOCOL.md` for eligibility and scientific distinctions. Four date-bounded arXiv queries returned 220 unique works: 22 already collected, 13 newly inspected and included, and 185 unscreened keyword candidates. Fourteen older pending candidates outside this result set remain queued, making 199 pending candidates across the two runs. Pending does not mean eligible or excluded. Prior discovery lacks a complete corpus denominator; no PRISMA completeness or recall estimate is claimed.

All 93 arXiv works already in the source registry were checked through the official unversioned-ID API. KARMA v2 was the only update dated after November 1; its gate, transfer result and limitations were re-inspected. The remaining works retain their earlier claim-review dates. `screening.json` now retains 54 decisions: 50 included extractions and four contextual works. Version migrations are separately recorded in `corrections.json`.

Evidence uses pinned papers and locators. First release, inspected revision, metadata check and claim review are distinct dates. Full third-party papers are not distributed. Short support anchors and hashes identify inspected HTML renderings; arXiv can regenerate HTML without changing the PDF version.

`primary_source_checked` means AI-assisted inspection of the specified claim, protocol and limitations. It is not experimental reproduction or independent dual annotation. The 85 inherited records remain `legacy_curated`. Human adjudication is pending; no agreement statistic is fabricated. Automatic excerpt matching checks traceability, not scientific truth.

## Files and loading

`dataset.json` and `records.jsonl` preserve the nested representation; `schema.json` specifies it. `primary-checked.records.jsonl` contains only the 60 targeted primary-checked records. Seventeen have no structured outcome; use `signals.csv` for the 45 scoped observations. This subset is not independently human-adjudicated.

`sources.json`, `screening.json`, `search-log.json`, `corrections.json`, `quality-report.json`, `citation.bib` and `checksums.json` accompany every version. The v0.4.0 search log preserves its query counts and pending identities; the historical logs remain separately archived.

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
| `review-queue.csv` | 85 primary-source reviews and 60 human-adjudication tasks; reviewer fields are blank |

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
