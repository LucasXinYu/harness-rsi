# Harness RSI Evidence Dataset

## Status and purpose

**v0.5.0 — released November 14, 2026.** Maintained by the Harness RSI project team as a companion to *From Harness Optimization to Recursive Self-Improvement: A Survey of Language Model Agents*. Xin Yu leads the project. Codex assisted search, extraction and validation; it is not a scholarly author. No additional funding is asserted for this dataset release.

This resource documents what agent harnesses change, how changes are selected, what outcomes are reported, and what the evidence cannot establish. It is a curated evidence collection, not a new benchmark or a collection of reproduced experiments.

## Composition and coverage

| Quantity | v0.1.0 | v0.2.0 | v0.3.0 | v0.4.0 / v0.4.1 | v0.5.0 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Category-source records | 95 | 113 | 132 | 145 | 159 |
| Distinct works | 63 | 81 | 100 | 113 | 126 |
| Records with structured signals | 4 | 22 | 30 | 43 | 57 |
| Scoped signals | 6 | 24 | 32 | 45 | 59 |
| Documented primary-source checks | Not claimed | 28 | 47 | 60 | 74 |
| Inherited records without a new primary audit | 95 | 85 | 85 | 85 | 85 |
| Populated selection/control fields | 0 | 28 | 47 | 60 | 74 |
| Independently human-adjudicated records | Not claimed | 0 | 0 | 0 | 0 |

The 126 works comprise 125 papers and one benchmark resource. v0.5.0 adds 14 records and 14 scoped observations: 13 new works and one new multi-domain record for an existing work's v2. MemSkill v3 and RSI-Dojo v2 retain their scoped labels after version rechecks. The two legacy Multi-Task Self-Harness v1 records remain unchanged. Records and signals are not independent effects. All five earlier releases remain byte-for-byte unchanged; their correction notices remain applicable.

Targeted discovery runs through **November 14, 2026**, with a seven-day overlap beginning October 28. New additions were first posted November 2–11. The original survey atlas retains its **October 1** cutoff and 95 records. The broader bibliography contains 335 papers and 11 resources; it is a separate collection, not the dataset denominator.

The dataset spans coding, reasoning, interactive, visual and cross-domain settings. Existing task categories accommodate this batch; no new category or historical reassignment was needed. This release emphasizes continual forgetting, total improvement cost, statistical acceptance, verifier validity, student-specific skill reuse and coupled weight/harness training. Positive, mixed and regression observations are all retained.

## Collection and review

See `PROTOCOL.md` for eligibility and scientific distinctions. Four date-bounded arXiv queries returned 295 unique works: 24 already collected, 17 newly inspected and included in the bibliography, and 254 pending keyword candidates. Of the 17 additions, 13 contribute evidence records; four remain contextual bibliography entries. Eighty older pending candidates outside this result set remain queued, for 334 cumulative pending candidates. These are keyword matches, not an eligible-study denominator. Supplemental primary-site searches and unresolved follow-ups are recorded separately. BOXBOX v2 remains pending because its latest full text could not be retrieved. No PRISMA completeness or recall estimate is claimed.

All 106 arXiv works in the prior evidence-source registry were checked through the official unversioned-ID API. Three post-November-4 revisions were inspected: MemSkill v3, RSI-Dojo v2 and Multi-Task Self-Evolving Harnesses v2. This is not a version audit of all 335 bibliography papers. Other records retain their earlier review dates. The screening ledger retains prior decisions and distinguishes contextual exclusions from evidence inclusions; version migrations are separately recorded in `corrections.json`.

Evidence uses pinned papers and locators. First release, inspected revision, metadata check and claim review are distinct dates. Full third-party papers are not distributed. Short support anchors and hashes identify inspected HTML renderings; arXiv can regenerate HTML without changing the PDF version.

`primary_source_checked` means AI-assisted inspection of the specified claim, protocol and limitations. It is not experimental reproduction or independent dual annotation. The 85 inherited records remain `legacy_curated`. Human adjudication is pending; no agreement statistic is fabricated. Automatic excerpt matching checks traceability, not scientific truth.

## Files and loading

`dataset.json` and `records.jsonl` preserve the nested representation; `schema.json` specifies it. `primary-checked.records.jsonl` contains only the 74 targeted primary-checked records. Seventeen have no structured outcome; use `signals.csv` for the 59 scoped observations. This subset is not independently human-adjudicated.

`sources.json`, `screening.json`, `search-log.json`, `corrections.json`, `quality-report.json`, `citation.bib` and `checksums.json` accompany every version. The v0.5.0 search log preserves its query counts and pending identities; the historical logs remain separately archived.

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
| `review-queue.csv` | 85 primary-source reviews and 74 human-adjudication tasks; reviewer fields are blank |

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
