# Maintaining Harness RSI

This repository is the literature companion to an ongoing survey. The homepage and GitHub README show aggregate publication trends and collection updates. The research atlas will explain editable harnesses and evolved mechanisms across domains once findings are ready. Individual paper records remain in the source data; the manuscript stays in Overleaf.

## Add or correct a paper

Check the primary source, identify the principal contribution, and distinguish harness changes from task outputs, model training, and supporting infrastructure. Record a concise description of the mechanism and its relevance. A title containing “RSI” does not establish recursive improvement of the optimizer.

For the current workflow, update `literature.bib` and `literature_map.tex` in the survey workspace, then import them:

```sh
python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD
python3 -m unittest discover -s tests
python3 scripts/catalog.py check
git diff
git add data docs/catalog.json docs/stats.json docs/assets/publication-timeline.svg README.md
git commit -m "Update literature collection"
git push
```

Use the actual collection-update date. The import rebuilds the README, chart, and website data. It preserves each record’s original `added_on` and release-date annotation. If correcting a release date, edit that record in `data/annotations.json`, include the primary-source URL and date basis, and rebuild with `python3 scripts/catalog.py build`.

The GitHub issue template accepts paper suggestions and corrections. Contributions should give the title, primary-source link, suggested category, and a short explanation of relevance. Do not upload copyrighted paper PDFs.

## Data definitions

| Field or file | Meaning |
| :-- | :-- |
| `data/literature.bib` | Bibliographic identity and source URL, copied from the survey bibliography. |
| `data/annotations.json` | One annotation per citation key: primary category, record kind, method summary, release date with provenance, and first-added date. |
| `kind: paper` | A paper or manuscript in the literature map, including surveys, adjacent methods, and benchmarks. This is not a claim of peer review or RSI capability. |
| `kind: resource` | An official benchmark page, code resource, or implementation reference, counted separately from papers. |
| `category` | The primary thematic contribution inherited from the Literature Map. Each record has one category so category totals do not double-count. |
| `release.value` | First arXiv submission where available; arXiv identifier month as fallback; otherwise the bibliographic publication date. It is not the date a revised version appeared. Venue-based fallbacks can be later than an unrecorded preprint. |
| `release.precision` | `day`, `month`, `year`, or `unknown`. Month/year values remain partial dates. No first-of-month/year date is fabricated. |
| `release.source` / `release.basis` | Evidence URL and description of the recorded date. Initial dates come from existing source checks and Literature Map notes. |
| `added_on` | First addition to this repository, preserved during subsequent imports and re-additions where historical snapshots exist. All initial entries share the baseline date because earlier discovery dates are not reconstructed. |
| `data/history.json` | Dated snapshots containing citation keys. One end-of-day snapshot is retained per changed day. Counts can decrease after removals; a corrected summary alone does not create a growth point. Git history retains the detailed edits. |
| `search_cutoff` | The literature-search horizon, distinct from the collection-update date. Update it only when the search has actually been extended. |

Versions of the same arXiv record are one work. Preprint and published versions should share a record when they represent the same work. Duplicate citation keys, DOI identifiers, and arXiv IDs are rejected by the build. A paper without a DOI/arXiv ID still needs manual duplicate review.

## Read the charts correctly

**Publication timeline:** the website defaults to monthly counts and offers a cumulative view and year selector. The GitHub README shows monthly counts for the search-cutoff year. Earlier years contribute to a later year’s cumulative opening total. Only months through the search cutoff appear; a partially covered final month is marked. A zero means no included records for that month, not that no relevant work was published. Year-only and undated papers are excluded from these charts but retained in the collection total.

These plots describe the entire survey collection, including adjacent methods, surveys, benchmarks, and supporting work. They are not a field-wide census or a count of direct Harness RSI methods. Official resources are excluded from paper counts. `docs/stats.json` contains only aggregate counts, publication-month series, update dates, and collection snapshots; the homepage does not load individual paper records.

**Collection history:** dated corpus snapshots beginning with the initial import. There is initially one point. Future additions and removals produce real collection-history points. Never substitute publication dates or BibTeX access dates for historical collection dates.

## Build, preview, and validate

Python 3.11 or later is sufficient; no third-party packages are needed.

```sh
python3 scripts/catalog.py build
python3 -m unittest discover -s tests
python3 scripts/catalog.py check
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000` for the standalone research homepage. Its domain tabs work without a backend. All assets are local and there are no analytics, external fonts, or API keys.

The homepage is a scaffold: editable scope, evolved mechanisms, and evidence remain empty until the domain studies are ready. `docs/project.json` contains the planned domain names and empty `findings` arrays, plus null arXiv and website URLs. The renderer intentionally displays empty states; presenting findings will require an evidence-backed study view. Do not fill it with inferred results, placeholder scores, or invented links. The aggregate activity section is populated from the actual bibliography. Keep domain findings empty until source-supported content is ready. Counts and the data-update date come from the import pipeline, not the date of a website redesign.

The validation workflow checks source consistency, identifiers, date precision, snapshot totals, and generated-file freshness. These checks do **not** verify a paper’s scientific claims; reading the primary sources remains necessary.

## GitHub hosting

The README displays aggregate counts, a monthly SVG chart, and collection updates, without enumerating papers. The `docs/` folder is also a complete static website.

The repository starts private. Website deployment is a separate, manual action: after deciding to publish the collection, set GitHub Pages to use GitHub Actions and run **Publish literature website**. That workflow refuses to run on a private repository. It deploys only `docs/`. No automatic web-publication or literature-discovery schedule is configured.

## File boundaries

Do not add unpublished manuscript drafts, local audit ledgers, credentials, Overleaf exports, or downloaded paper PDFs. Repository-specific files stay here; they do not get imported into the Overleaf project. The repository currently has no blanket license grant; source papers retain their original rights.
