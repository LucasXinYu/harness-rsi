![Harness RSI — A living research atlas](docs/assets/project-banner.svg)

<p align="center"><strong>The official project repository for Harness RSI</strong><br>Research in progress · Survey and domain findings forthcoming</p>

<p align="center"><a href="#living-collection">Collection activity</a> · <a href="#research-atlas">Research atlas</a> · <a href="#contributors">Contributors</a> · <a href="CONTRIBUTING.md">Contribute</a></p>

## Research atlas

We study **what an agent can change in its harness, what mechanisms emerge, and what evidence supports those changes** across task domains. The website is the visual companion: domain studies, annotated figures, and an evolving picture of the collected literature.

| Editable harness | Evolved mechanism | Supporting evidence |
| :-- | :-- | :-- |
| Components and modification boundaries | Concrete changes in how the agent works | Source papers, artifacts, traces, and evaluations |

The standalone homepage is ready for domain studies and a growing figure library, with expandable images and source captions. Findings remain unfilled until the research is ready.

**Project links:** arXiv paper — forthcoming · Public website — forthcoming · [Bibliography data](data/literature.bib) · [Validation](https://github.com/LucasXinYu/harness-rsi/actions/workflows/validate.yml)

## Living collection

**177 papers & manuscripts** · **10 official resources** · Updated **2026-10-03**

![Collected papers by publication month](docs/assets/publication-timeline.svg)

The survey collection includes related methods, surveys, and benchmarks. **173/177 papers** have known release months and appear in these charts. Official resources are counted separately. Search through **2026-10-01**.

<details>
<summary>How to read the statistics</summary>

The chart uses first arXiv submission where available and bibliographic publication dates otherwise. These counts describe our collection, not a census of the field or a count of methods that achieve RSI. Monthly and cumulative views exclude papers without month-level dates. The final month stops at the search cutoff.

Publication dates and collection updates are different: the snapshots below record actual imports. The first snapshot is the baseline; earlier collection activity has not been reconstructed. Future imports extend this history, and removals can reduce the total.

[Full data and date methodology](CONTRIBUTING.md#data-definitions)

</details>

### Collection updates

| Collection snapshot | Papers | Official resources |
| :-- | --: | --: |
| 2026-10-03 | 177 | 10 |

## Contributors

| Contributor | Role | Contribution |
| :-- | :-- | :-- |
| [Xin (Lucas) Yu](https://github.com/LucasXinYu) | Project lead | Research direction, literature curation, and editorial decisions. |
| Codex | AI assistant · OpenAI | Assistance with implementation, visualization, literature organization, and editing. |

## Run the website

A static website with local assets. No API keys, analytics, or third-party build dependencies.

```sh
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. Figure assets and captions are managed through `docs/project.json`; see the [figure guide](CONTRIBUTING.md#add-research-figures).

## Keep it growing

[Suggest a paper or correction](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml) · [Report a website issue](https://github.com/LucasXinYu/harness-rsi/issues/new?template=website.yml)

Update the survey bibliography and Literature Map, then import them. One build refreshes the website statistics, chart, and this README together.

```sh
python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD
python3 -m unittest discover -s tests
python3 scripts/catalog.py check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for verification, attribution, figures, and update policies.
