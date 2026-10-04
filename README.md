# Harness RSI

**What can change. What evolution creates.**

A research companion exploring editable agent harnesses and the mechanisms they evolve across task domains.

The research atlas will connect **task domains → editable harnesses → evolved mechanisms → evidence**. Domain findings and the survey link are forthcoming.

## A growing research collection

**177 papers & manuscripts · 10 official resources**

Collection updated: **2026-10-03** · Literature search through: **2026-10-01**

![Collected papers by publication month](docs/assets/publication-timeline.svg)

Counts describe the literature included in our survey, including related methods, surveys, and benchmarks. They do not represent a census of the field or a count of methods that achieve RSI. Official resources are counted separately.

The chart uses first arXiv submission where available and bibliographic publication dates otherwise. **173/177** papers have a known release month; the remaining papers are included in the total but excluded from monthly and cumulative charts. The final month stops at the stated search cutoff.

## Collection updates

These are actual collection snapshots, distinct from the publication months above. The initial import is the baseline; earlier collection activity has not been reconstructed. Future imports extend this history, and removals can reduce the total.

| Collection snapshot | Papers | Official resources |
| :-- | --: | --: |
| 2026-10-03 | 177 | 10 |

## Explore the project

The standalone homepage contains interactive monthly and cumulative publication views and a domain atlas prepared for future findings. The website and this README present aggregate progress; individual records remain in the underlying data.

[Bibliography data](data/literature.bib) · [Counting methodology & contributions](CONTRIBUTING.md) · [Suggest a paper](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml)

Preview the website locally:

```sh
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. The arXiv and public website links will be added when available.

## Keep the collection current

Update the survey bibliography and Literature Map, then import them. One build refreshes the website statistics, monthly chart, and this README together.

```sh
python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD
python3 -m unittest discover -s tests
python3 scripts/catalog.py check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for source verification, date provenance, and update policies. No external packages or API keys are required.
