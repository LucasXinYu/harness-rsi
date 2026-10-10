![Harness RSI — How agent harnesses evolve](docs/assets/project-banner.svg)

<p align="center"><strong>What actually evolves around the model?</strong><br>A survey and visual companion on agent harness optimization and recursive self-improvement.<br><sub>Official project repository · Research in progress · Manuscript forthcoming</sub></p>

<p align="center"><a href="#what-the-survey-finds">Findings</a> · <a href="#across-four-domains">Domain atlas</a> · <a href="#living-collection">Living collection</a> · <a href="#contributors">Contributors</a></p>

We trace **what changed in the target-agent harness, what that change accomplished, and under which conditions it might be useful again**. The evidence follows concrete interfaces, parsers, context-handling rules, recovery branches and persistent skills—not just optimization algorithms or benchmark scores.

**95 category–source records · 62 research papers + 1 benchmark resource · 20 task subcategories · 4 domains**

Domain evidence cutoff: **2026-10-01**. A record is one source within one task subcategory. Records can share a source and include incomplete reporting; these are not 95 independent effects. All 95 domain records are available in the benchmark explorer and downloadable data. The manuscript is forthcoming.

## What the survey finds

**Repair the connection, not just the reasoning.** Some gains come from making an existing intention reach the right tool, object or observation. A higher task score need not mean a new reasoning capability.

**More context and more tools are not enough.** Useful additions resolve a pending decision. Rejected tools and failed branches matter alongside successful changes; these cases do not establish a universal preference for smaller harnesses.

**A retry rule carries conditions for reuse.** Recovery depends on a detectable failure, observable state and an available corrective action. Transfer between related placement tasks is documented; cross-domain analogies remain hypotheses.

## Across four domains

| Domain | Concrete changes highlighted | Records |
| :-- | :-- | --: |
| Coding | Keep the edit payload intact. Read the region, not the whole world. Recover from the failure that actually happened. | 36 |
| Reasoning & information | Check the question before computing the answer. Retrieve the evidence that separates answers. Make a failed proof actionable. | 33 |
| Interactive & embodied | Bind an action to the right object. Turn task rules into executable checks. Recover from the observed physical state. | 17 |
| Visual understanding & generation | Keep claims attached to observations. Recheck the interval with the same frames. Compare drafts against concrete failure conditions. | 9 |

### A few results—and what they establish

- **Whole-harness result.** The complete Multi-task Self-Harness recovers 7 of 12 SWE-Bench Pro tasks where the seed exceeds the input limit. This is not a truncation-only ablation. DGM, SICA and AIDE² offer complementary implementations rather than a shared evaluated patch. Sources: [DGM](https://proceedings.iclr.cc/paper_files/paper/2026/file/aa5f5e6eb6f613ec412f1d948dfa21a5-Paper-Conference.pdf), [SICA](https://openreview.net/forum?id=rShJCyLsOr), [Multi-task Self-Harness](https://arxiv.org/abs/2609.38372v1), [AIDE²](https://arxiv.org/abs/2609.26457v1).
- **Related-task transfer.** Zetta’s cumulative stack transfers unchanged to three related tasks: mean success rises from 64% to 84%. The result does not isolate individual recovery branches or establish transfer to other domains. HarnessPAI supplies a complementary state-estimation repair. Sources: [Zetta](https://arxiv.org/abs/2608.16590v1), [HarnessPAI](https://arxiv.org/abs/2609.29166v1).
- **Combined-component ablation.** At a fixed three-image budget, AutoRef’s held-out average falls from 7.37 to 6.93 when its combined failure-aware selector is replaced. The ablation does not isolate order swapping. Reusable selection and composition procedures are the harness artifacts; a generated image is not. Sources: [AutoRef](https://arxiv.org/abs/2609.35530v1), [COMFYCLAW](https://arxiv.org/abs/2607.01709v1), [VideoWeaver](https://arxiv.org/abs/2606.08091v2).

## Benchmark evidence explorer

The website pairs **12 domain observations** with **27 comparison lenses** and **95 source records**. Filter by domain, subcategory and benchmark/setting; read the concrete change alongside its seed, outcome, primary-source location and reporting limits.

Examples include empty-patch recovery and dependency-aware verification in repository repair; bounded completion checks in terminal tasks; contrasting-label retrieval in classification; and failure-aware draft selection in image generation. These are source-grounded comparisons, not prescriptions that every benchmark shares the same solution.

Single-source observations are identified. Transfers retain their original discovery setting. Where a source reports an evolution experiment without a final artifact, the explorer shows the gap rather than inventing a common pattern. Full-system improvements are not attributed to individual edits.

[Download all domain evidence](docs/evidence.json) · [Selected domain findings](docs/project.json) · [Download BibTeX](data/literature.bib) · [Catalog and date provenance](docs/catalog.json)

### A living companion, beyond the paper

We will continue to add verified studies, benchmark-level harness changes and revised syntheses as new evidence becomes available. Each evidence release will be dated and traceable; the paper’s frozen snapshot will remain identifiable.

Updates follow the availability and verification of new evidence. Collection imports and evidence revisions are dated separately; prior versions remain in repository history.

Latest evidence release: **2026-10-10**. [Dated changes](docs/updates.json). Collection updates below track bibliography membership separately from evidence revisions.

## Living collection

**235 papers & manuscripts** · **11 official resources** · Updated **2026-10-10**

![Cumulative collected literature by release month](docs/assets/collection-growth.svg)

The working literature collection is broader and newer than the frozen domain evidence above. It includes surveys, adjacent methods, benchmarks and supporting work. Search through **2026-10-10**; **223/235** papers have known release months. Resources are excluded from paper counts.

<details><summary>Monthly publication counts and counting methodology</summary>

![Monthly collected literature](docs/assets/publication-timeline.svg)

First arXiv submission is used when available; otherwise the recorded bibliographic date or identifier month is used. Date provenance is retained per entry. Year-only records remain in the total but are excluded from monthly and cumulative charts. These are collection statistics, not a field-wide census or a count of methods achieving RSI.

Publication dates differ from collection dates. The snapshots below record actual imports. We do not reconstruct collection history before the initial snapshot. Removals can reduce totals. [Data definitions](CONTRIBUTING.md#data-definitions).

</details>

### Collection updates

| Snapshot | Papers | Resources |
| :-- | --: | --: |
| 2026-10-03 | 177 | 10 |
| 2026-10-10 | 235 | 11 |

## Website

The standalone site lives in `docs/`: domain tabs, benchmark filters, a detailed evidence notebook, comparisons, monthly/cumulative charts and dated release notes. The manuscript link will be added when available.

```sh
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. Public hosting is not yet enabled; updating this repository does not itself publish GitHub Pages.

## Contributors

| Contributor | Role | Contribution |
| :-- | :-- | :-- |
| [Xin (Lucas) Yu](https://github.com/LucasXinYu) | Project lead | Research direction, literature curation, and editorial decisions. |
| Codex | AI assistant · OpenAI | Assistance with implementation, visualization, literature organization, and editing. |

## Keep it growing

Import the current survey bibliography and Literature Map. Map membership defines the collection; extra manuscript references and citation aliases are not automatically counted.

```sh
python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD
python3 -m unittest discover -s tests
python3 scripts/catalog.py check
```

The build updates website statistics, downloadable data, charts and this README together. Source-linked findings live in `docs/project.json`. Benchmark assignments and comparative notes live in `data/evidence_annotations.json`; imported domain records live in `docs/evidence.json`. They are revised separately from collection counts.

After reviewing changed records and benchmark assignments:

```sh
python3 scripts/import_evidence.py --source /path/to/section4_supp.tex --date YYYY-MM-DD
# Add a dated entry to docs/updates.json describing the actual changes.
python3 scripts/catalog.py build
python3 -m unittest discover -s tests
node tests/evidence_model_test.mjs
python3 scripts/catalog.py check
```

[Suggest a paper or correction](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml) · [Contribution guide](CONTRIBUTING.md) · [Validation](https://github.com/LucasXinYu/harness-rsi/actions/workflows/validate.yml)
