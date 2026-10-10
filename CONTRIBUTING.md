# Maintaining Harness RSI

This repository is the literature companion to an ongoing survey. The homepage and GitHub README show aggregate publication trends and collection updates. The research atlas presents selected before/after changes, outcomes and limits across four task domains. Individual paper records remain in the source data; the manuscript stays in Overleaf.

## Add or correct a paper

Check the primary source, identify the principal contribution, and distinguish harness changes from task outputs, model training, and supporting infrastructure. Record a concise description of the mechanism and its relevance. A title containing “RSI” does not establish recursive improvement of the optimizer.

For the current workflow, update `literature.bib` and `literature_map.tex` in the survey workspace, then import them:

```sh
python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD
python3 -m unittest discover -s tests
python3 scripts/catalog.py check
git diff
git add data docs/catalog.json docs/stats.json docs/literature.bib docs/assets/publication-timeline.svg docs/assets/collection-growth.svg README.md
git commit -m "Update literature collection"
git push
```

Use the actual collection-update date. The import rebuilds the README, chart, and website data. It preserves each record’s original `added_on` and release-date annotation. If correcting a release date, edit that record in `data/annotations.json`, include the primary-source URL and date basis, and rebuild with `python3 scripts/catalog.py build`.

The GitHub issue template accepts paper suggestions and corrections. Contributions should give the title, primary-source link, suggested category, and a short explanation of relevance. Do not upload copyrighted paper PDFs.

## Data definitions

| Field or file | Meaning |
| :-- | :-- |
| `data/literature.bib` | Bibliographic identity and source URL, selected from the survey bibliography using Literature Map membership; extra manuscript references and aliases are excluded. |
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

**Publication timeline:** the website defaults to cumulative counts and offers monthly counts and a year selector. The GitHub README shows cumulative growth, with monthly counts in an expandable section. Earlier years contribute to a later year’s cumulative opening total. Only months through the search cutoff appear; a partially covered final month is marked. A zero means no included records for that month, not that no relevant work was published. Year-only and undated papers are excluded from these charts but retained in the collection total.

These plots describe the entire survey collection, including adjacent methods, surveys, benchmarks, and supporting work. They are not a field-wide census or a count of direct Harness RSI methods. Official resources are excluded from paper counts. `docs/stats.json` contains only aggregate counts, publication-month series, update dates, and collection snapshots; the homepage does not load individual paper records.

**Collection history:** dated corpus snapshots beginning with the initial import. The baseline and subsequent imports are retained. Additions and removals produce real collection-history points. Never substitute publication dates or BibTeX access dates for historical collection dates.

## Build, preview, and validate

Python 3.11 or later is sufficient; no third-party packages are needed.

```sh
python3 scripts/catalog.py build
python3 -m unittest discover -s tests
python3 scripts/catalog.py check
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000` for the standalone research homepage. Its domain tabs work without a backend. All assets are local, including the Manrope typeface (SIL Open Font License in `docs/assets/fonts/`). There are no analytics, remote font requests, or API keys.

## Update domain findings

`docs/project.json` contains four domain summaries, 12 selected observations and three cross-domain comparisons. Each observation provides:

- Task setting and the concrete before/after change.
- An observed outcome and an evidence type (case, full-system result, ablation, or transfer).
- A limit on interpretation, especially component attribution and portability.
- Primary-source citation keys, links and section or artifact locators.

Read the relevant source before editing these fields. Supplied architecture, proposed changes, intermediate discoveries and retained modifications are not interchangeable. A task answer or generated image is not automatically a reusable harness artifact. Do not turn an overall score increase into a component-level causal claim.

The build checks count consistency, source identity and comparison-to-evidence links. It does **not** verify scientific claims. Cases cited in the manuscript but not in the curated Literature Map may appear in `additional_finding_sources` with an explicit scope note. They are excluded from collection statistics until formally imported into the Map.

The evidence summary is frozen separately from the working collection: the 95 category–source records cover four domains, 62 research papers and one benchmark resource through October 1, 2026. The homepage exposes selected synthesis, not the complete 95-record release. Updating bibliography counts does not automatically extend that evidence cutoff or add new observations. Do not imply independent discoveries when a source appears in several categories.

Run `python3 scripts/catalog.py build` after changing findings or contributors so the README stays synchronized. The cumulative/monthly SVG charts, JSON and downloadable BibTeX are generated; edit their source data, not generated output.

## Visual design and attribution

Preserve the light violet project identity, local Manrope typeface and responsive layouts. The cross-domain visual comparison is accessible HTML connected to the same findings data as the atlas. Its cells link to source-bearing evidence disclosures; do not replace them with an untraceable illustration. Keep the page focused on findings and aggregate trends rather than a paper directory.

New research figures should be original, source-linked SVG diagrams or appropriately attributed reusable artwork. Check labels at desktop and mobile sizes, and provide informative alternative text. The recursive ribbon is project artwork, not a scientific finding; its editable source lives in `scripts/identity.py`.

Contributor names and roles are stored in `docs/project.json`. Xin (Lucas) Yu leads research direction and editorial decisions; Codex is credited as an OpenAI AI assistant, not as a human researcher or scholarly author.

## GitHub hosting

The README displays aggregate counts, cumulative and monthly SVG charts, and collection updates, without enumerating papers. The `docs/` folder is also a complete static website.

The repository starts private. Website deployment is a separate, manual action: after deciding to publish the collection, set GitHub Pages to use GitHub Actions and run **Publish literature website**. That workflow refuses to run on a private repository. It deploys only `docs/`. No automatic web-publication or literature-discovery schedule is configured. The official-project branding identifies this repository as the project home; it does not imply that the survey has been published or accepted.

## File boundaries

Do not add unpublished manuscript drafts, local audit ledgers, credentials, Overleaf exports, or downloaded paper PDFs. Repository-specific files stay here; they do not get imported into the Overleaf project. The repository currently has no blanket license grant; source papers retain their original rights.


## Updating benchmark evidence

The benchmark explorer is a companion to the domain evidence, not a leaderboard. Keep each study's seed, evaluation setting, actual artifact and attribution limits together.

1. Review the source manuscript and the relevant primary paper or released artifact. Update the domain record before changing a synthesis.
2. Maintain explicit benchmark memberships in `data/evidence_annotations.json`. Distinguish transfer, evaluation and case settings. Do not infer a concrete mechanism for every dataset named by a paper.
3. Add comparison notes only where a record supports them. Use a note's optional `benchmarks` list to restrict it to supported settings; an empty list makes a note visible only at the broader category level. A Liar's Dice case, for example, must not become a Balatro discovery.
4. Import the reviewed appendix with `python3 scripts/import_evidence.py --source /path/to/section4_supp.tex --date YYYY-MM-DD`. Its sibling `literature.bib` supplies manuscript references. The importer refuses an unreviewed new record until its benchmark assignment exists.
5. Update `docs/updates.json` with the actual date, additions, corrections or changed conclusions. Preserve previous entries. Update the snapshot totals and cutoff in `docs/project.json` when the underlying evidence set changes. Bibliography imports have their own collection history.
6. Run the Python tests, `node tests/evidence_model_test.mjs`, `python3 scripts/catalog.py build` and `python3 scripts/catalog.py check`. Check the rendered site, then commit the data and interface together. Repository history retains earlier evidence versions.

`docs/evidence.json` contains the export date, source-file hash, all domain records, primary-source locators and curated comparisons. A source repeated across subcategories is not an independent replication. Benchmark/setting labels include study-specific cases and transfer suites; their number is not the number of independent evolution experiments. Tests verify structural consistency and attribution boundaries; they do not replace reading the primary evidence.
