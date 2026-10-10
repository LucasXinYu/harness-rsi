![Harness RSI — How agent harnesses evolve](docs/assets/project-banner.svg)

<p align="center"><strong>What actually evolves around the model?</strong><br>A survey and visual companion on agent harness optimization and recursive self-improvement.<br><sub>Official project repository · Research in progress · Manuscript forthcoming</sub></p>

<p align="center"><a href="#what-the-survey-finds">Findings</a> · <a href="#across-four-domains">Domain atlas</a> · <a href="#living-collection">Living collection</a> · <a href="#contributors">Contributors</a></p>

We trace **what changed in the target-agent harness, what that change accomplished, and under which conditions it might be useful again**. The evidence follows concrete interfaces, parsers, context-handling rules, recovery branches and persistent skills—not just optimization algorithms or benchmark scores.

**95 category–source records · 62 research papers + 1 benchmark resource · 20 task subcategories · 4 domains**

Domain evidence cutoff: **2026-10-01**. A record is one source within one task subcategory. Records can share a source and include incomplete reporting; these are not 95 independent effects. Selected synthesis is available in this repository; the full manuscript and record collection are forthcoming.

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

The interactive atlas contains 12 selected observations with before/after descriptions, source links, evidence types and reporting limits. It compares changes across papers without attributing a full-system gain to an individual edit.

[Explore the structured findings](docs/project.json) · [Download BibTeX](data/literature.bib) · [Catalog and date provenance](docs/catalog.json)

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

The standalone site lives in `docs/`: domain tabs, evidence-linked comparisons, monthly/cumulative charts, source disclosures and local artwork. The manuscript link will be added when available.

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

The build updates website statistics, downloadable data, charts and this README together. Source-linked findings live in `docs/project.json` and are revised separately from collection counts.

[Suggest a paper or correction](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml) · [Contribution guide](CONTRIBUTING.md) · [Validation](https://github.com/LucasXinYu/harness-rsi/actions/workflows/validate.yml)
