![Harness RSI — How agent harnesses evolve](docs/assets/project-banner.svg)

<p align="center"><strong>What actually evolves around the model?</strong><br>The research companion to our survey of harness optimization and recursive self-improvement.<br><sub>Private project preview · Manuscript forthcoming · Public hosting not enabled</sub></p>

<p align="center"><a href="#what-we-study">Our work</a> · <a href="#compare-the-mechanisms">Compare mechanisms</a> · <a href="#evidence-you-can-trace">Evidence</a> · <a href="#maintenance-and-versions">Maintenance</a> · <a href="#authors">Authors</a></p>

We trace **what changed in the target-agent harness, what that change accomplished, and under which conditions it might be useful again**. The central object is a reusable change to an interface, parser, context rule, recovery branch or persistent skill. A benchmark score alone does not tell that story.

**95 category–source records · 62 research papers + 1 benchmark resource · 20 task subcategories · 4 domains**

## What we study

| Question | What this project provides |
| :-- | :-- |
| **How is a harness improved?** | A comparison of editable components, proposers, evaluators, search and optimization history. The site explains how these parts interact. |
| **Does the improver change too?** | A distinction between optimizing a task harness and reusing revised improvement capabilities in later rounds. Task gains alone do not establish general RSI. |
| **What actually emerges?** | Task-organized records of seed capabilities, reported failures, concrete edits, outcomes and limits; comparisons of recurring functions and domain-specific implementations. |

The website lets readers move from a research question to a concrete mechanism, then to benchmark-specific evidence and its primary source. It accompanies the survey with inspectable data and an interface for comparison.

## Compare the mechanisms

![Four domains compared through concrete interface, evidence and recovery edits](docs/assets/mechanism-map.svg)

The interactive site lets you choose **any two domains** and switch between interfaces, decision evidence and recovery. Each comparison reveals the actual editable artifact, before/after behavior, reported result, source location and conditions for reuse. The diagram shows selected mechanisms and intended outputs; it does not claim that these changes compose into one pipeline or transfer across domains.

**Repair the connection, not just the reasoning.** Some gains come from making an existing intention reach the right tool, object or observation. A higher task score need not mean a new reasoning capability.

**More context and more tools are not enough.** Useful additions resolve a pending decision. Rejected tools and failed branches matter alongside successful changes; these cases do not establish a universal preference for smaller harnesses.

**A retry rule carries conditions for reuse.** Recovery depends on a detectable failure, observable state and an available corrective action. Transfer between related placement tasks is documented; cross-domain analogies remain hypotheses.

<details><summary>Representative observations and their sources</summary>

| Domain | A concrete observation | Evidence boundary |
| :-- | :-- | :-- |
| Coding | The complete Multi-task Self-Harness recovers 7 of 12 SWE-Bench Pro tasks where the seed exceeds the input limit. [DGM](https://proceedings.iclr.cc/paper_files/paper/2026/file/aa5f5e6eb6f613ec412f1d948dfa21a5-Paper-Conference.pdf), [SICA](https://openreview.net/forum?id=rShJCyLsOr), [Multi-task Self-Harness](https://arxiv.org/abs/2609.38372v1), [AIDE²](https://arxiv.org/abs/2609.26457v1) | This is not a truncation-only ablation. DGM, SICA and AIDE² offer complementary implementations rather than a shared evaluated patch. |
| Reasoning & information | A richer Lean helper-lemma branch encounters context and assembly failures. A heavily used Rocq lemma-search proposal is rejected without accuracy gains. [Lean co-evolution](https://arxiv.org/abs/2607.17352v1), [Prover-interface evolution](https://arxiv.org/abs/2609.39544v3) | More tools and more decomposition do not reliably yield completed proofs; final status matters as much as tool usage. |
| Interactive & embodied | Zetta’s cumulative stack transfers unchanged to three related tasks: mean success rises from 64% to 84%. [Zetta](https://arxiv.org/abs/2608.16590v1), [HarnessPAI](https://arxiv.org/abs/2609.29166v1) | The result does not isolate individual recovery branches or establish transfer to other domains. HarnessPAI supplies a complementary state-estimation repair. |
| Visual understanding & generation | VideoEvolve improves a kettle case, but a light-switch regression persists despite additional calls. [VideoEvolve](https://arxiv.org/abs/2610.01766v1) | All configurations use the same frames. Additional reasoning costs compute and can preserve the same mistaken interpretation. |

</details>

## Evidence you can trace

**95 records** connect **20 task subcategories** to concrete studies. The benchmark explorer adds **27 comparison lenses** and **12 selected domain observations**. Filter by domain, subcategory and benchmark/setting, then inspect the seed, actual edit, outcome and original evidence.

**A record follows this chain:** task and seed → reported problem → reusable harness edit → observed result → primary-source location and limitations.

The frozen survey evidence covers work through **2026-10-01**. A record is one source within one subcategory: records may share a paper, include negative results or expose missing artifacts. They are not 95 independent effects. Full-system gains are not attributed to individual edits without supporting evidence. A transfer evaluation retains its original discovery setting.

| Inspect or download | Contents |
| :-- | :-- |
| [Full evidence export](docs/evidence.json) | All domain records, benchmark memberships, comparisons and source locations |
| [Selected findings and comparisons](docs/project.json) | Before/after changes, outcomes, evidence types and limits |
| [Bibliography](data/literature.bib) / [catalog](docs/catalog.json) | Source identities, classification and publication-date provenance |
| [Update history](docs/updates.json) / [data definitions](CONTRIBUTING.md#data-definitions) | Dated releases, counting rules and curation process |

## Maintenance and versions

We will continue to add verified studies, benchmark-level harness changes and revised syntheses as new evidence becomes available. Each evidence release will be dated and traceable; the paper’s frozen snapshot will remain identifiable.

| State | Date | What it means |
| :-- | :-- | :-- |
| **Frozen paper evidence** | 2026-10-01 | 95 category–source records; evidence export dated 2026-10-10 |
| **Living literature collection** | 2026-10-10 | Search horizon; 235 papers and 11 official resources; collection updated 2026-10-10 |
| **Website presentation** | 2026-10-11 | Compare mechanisms, not just domain labels; this update adds no studies or experimental findings |

**Our maintenance commitments**

- **Trace every substantive change.** New evidence identifies a task setting, starting harness, reusable edit, observed result and primary-source location. Reporting gaps remain explicit.
- **Keep versions and units distinct.** A revised paper updates its source record. One artifact evaluated on several settings is not counted as several independent discoveries.
- **Publish corrections with context.** A correction records what changed and why. Conflicting code, unclear retention and negative results remain attached to the original setting.
- **Preserve the paper snapshot.** The frozen survey cutoff stays identifiable. A bibliography import or website redesign does not silently extend the evidence collection.

Updates are maintained by the project team after source verification. Literature membership, evidence revisions and website changes have separate dates. There is no automated claim of a complete or continuously refreshed search.

The workflow is **find and screen → trace the actual change → revise comparisons → validate and record a dated release**. A website redesign does not create a new evidence snapshot. An added bibliography entry does not automatically become evidence for a domain finding.

[Suggest a paper](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml) · [Correct an evidence record](https://github.com/LucasXinYu/harness-rsi/issues/new?template=evidence.yml) · [Curation and contribution guide](CONTRIBUTING.md). Issue access is currently limited to repository collaborators.

## Living collection

**235 collected papers & manuscripts** · **11 official resources** · Collection updated **2026-10-10**

![Cumulative collected literature by release month](docs/assets/collection-growth.svg)

This collection is broader and newer than the frozen domain evidence. It includes surveys, adjacent methods, benchmarks and supporting work. **223/235** papers have known release months; year-only and undated records stay in the total but are not plotted. Resources are counted separately. These are collection statistics, not a census of the field or a count of methods achieving RSI.

<details><summary>Monthly counts and actual collection updates</summary>

![Monthly collected literature](docs/assets/publication-timeline.svg)

Publication dates use the first arXiv submission where available, then recorded bibliographic dates or identifier months. Provenance is retained per entry. The latest plotted month may be incomplete. These dates differ from the import dates below; collection history is never reconstructed from publication dates.

| Collection snapshot | Papers | Resources |
| :-- | --: | --: |
| 2026-10-03 | 177 | 10 |
| 2026-10-10 | 235 | 11 |

</details>

## Preview the website

The standalone site lives in `docs/`: an interactive harness cover, source-linked result spotlights, workflow explorer, two-domain comparison studio, benchmark evidence notebook, collection charts and dated maintenance notes. Assets and data are served locally; no account, API key or analytics are required.

```sh
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. Public hosting is not enabled. Pushing repository changes does not publish GitHub Pages; the deployment workflow remains a separate manual action.

## Authors

**From Harness Optimization to Recursive Self-Improvement: A Survey of Language Model Agents**

Xin Yu · Chengyuan Liu · Wenxin Long · Haochen Zhang · Lingzhou Xue

Department of Statistics, The Pennsylvania State University<br>
University Park, PA 16802, USA

The arXiv identifier and citation will be added when the preprint is available. Project branding does not imply publication or acceptance.

## Contributors

Project development and assistance are separate from scholarly authorship.

| Contributor | Role | Contribution |
| :-- | :-- | :-- |
| [Xin (Lucas) Yu](https://github.com/LucasXinYu) | Project lead | Research direction, literature curation, and editorial decisions. |
| Codex | AI assistant · OpenAI | Assistance with implementation, visualization, literature organization, and editing. |

<details><summary>Maintainer quick start</summary>

Import the reviewed survey bibliography and Literature Map with an actual collection-update date. Map membership determines the collection; extra manuscript references and aliases do not automatically count.

```sh
python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD
python3 scripts/catalog.py build
python3 -m unittest discover -s tests
node tests/evidence_model_test.mjs
python3 scripts/catalog.py check
```

The build synchronizes this README, diagrams, statistics and downloadable bibliography. Findings live in `docs/project.json`; benchmark assignments and comparative notes live in `data/evidence_annotations.json`. These are edited separately from bibliography counts. Follow the [evidence update procedure](CONTRIBUTING.md#updating-benchmark-evidence), add a dated release note, review the rendered site and commit the source and generated files together.

[Validation workflow](https://github.com/LucasXinYu/harness-rsi/actions/workflows/validate.yml) · [Contribution guide](CONTRIBUTING.md)

</details>
