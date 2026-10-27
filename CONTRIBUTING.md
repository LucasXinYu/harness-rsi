# Maintaining Harness RSI

This repository publishes a source-traceable evidence dataset and research atlas accompanying an ongoing survey. The homepage and GitHub README explain the survey’s three questions: how improvement works, whether the improver changes too, and what concrete harness mechanisms emerge. They combine aggregate collection trends, a two-domain comparison studio and a benchmark evidence notebook. Individual paper records remain in the source data; the manuscript stays in Overleaf.

## Evidence dataset releases

Read `DATASET_CARD.md` before interpreting the additive outcome/retention annotations. `data/dataset.json` defines the release version, date, frozen-input hash, provenance and rights status. `data/dataset_annotations.json` holds scoped signals linked to exact excerpts of the unchanged curated records. `scripts/dataset.py` validates this layer and is called by `catalog.py build/check`; do not edit generated exports directly.

Preserve all 95 category-source units and their IDs. Signals are not independent interventions. Label `not_reviewed` and null separately from verified `not_reported`; do not auto-fill positive or negative outcomes from keywords. Outcome, final retention, usage and component attribution are distinct. Unknown benchmark applicability must remain empty, not expand to all benchmark memberships. An existing record excerpt provides a traceable annotation basis, not proof of a fresh independent primary-source audit.

For a new release, preserve the previously published versioned files, bump the dataset version, update the card and coverage, review every new label and locator, and publish a dated release note. Do not rebase the frozen-source hash or overwrite a published version to hide changed evidence. Bibliography additions alone do not change dataset membership. No dataset-specific license is granted without explicit maintainer approval.

Run the Python tests, `node tests/dataset_model_test.mjs`, and `node --input-type=module --check < docs/dataset.js` in addition to the standard checks. Use `python3 examples/inspect_dataset.py --outcome regression` to verify that downloads are practically inspectable.

## Maintenance and corrections

AI-assisted literature searches are scheduled daily at 09:00 America/Los_Angeles. Publication follows primary-source verification, duplicate checks and repository validation; a scheduled search does not guarantee a new paper or complete coverage. The local updating agent commits and pushes verified changes, and GitHub Pages deploys the website. Keep three states separate:

| Update | Record the change here | Do not silently change |
| :-- | :-- | :-- |
| Literature membership or metadata | `data/literature.bib`, `data/annotations.json`, `data/history.json`, `data/config.json` | Paper evidence cutoff or domain findings |
| Domain evidence or a comparative conclusion | Reviewed evidence records, annotations, findings and an `evidence` release in `docs/updates.json` | Historical versions, original discovery setting or evidence limits |
| Interface, presentation or project information | Site source and a `website` release in `docs/updates.json` | Search horizon or evidence export date |

Release entries use a unique ID, actual date, `kind`, a concise description and the current evidence record count. Keep newest entries first and preserve earlier ones. The latest **evidence** release matches the evidence export date; the latest release overall may be a newer website update. Keep the manuscript cutoff identifiable even when the living collection grows.

For an evidence correction:

1. Identify the record ID (`subcategory--citationkey`) or finding ID, affected benchmark and precise sentence. Use the [evidence correction form](https://github.com/LucasXinYu/harness-rsi/issues/new?template=evidence.yml).
2. Supply a primary-source URL, version and locator. State whether the problem concerns the seed, actual edit, final retention, result attribution or transfer setting. Mark uncertain facts as unresolved.
3. Check the evidence record **and every selected finding/comparison that relies on it**. A source correction may require narrowing a pattern even if the bibliography stays unchanged.
4. Record the correction, its reason and affected IDs in the release note and commit. Keep negative results and reporting gaps. Do not delete them solely to simplify the story.
5. Run validation and inspect the changed interface. Structural checks do not establish scientific truth; the updating agent or maintainer must read the primary source, locate the supporting evidence and preserve attribution limits.

The repository and website are public. Community paper suggestions and source-backed corrections are welcome through repository issues. Source verification is required before updating the atlas; human maintainers remain responsible for research and editorial decisions.

## Add or correct a paper

Check the primary source, identify the principal contribution, and distinguish harness changes from task outputs, model training, and supporting infrastructure. Record a concise description of the mechanism and its relevance. A title containing “RSI” does not establish recursive improvement of the optimizer.

For incremental updates, edit `data/literature.bib` and the matching `data/annotations.json` entry directly. Preserve existing keys and first-added dates. On a membership change, append a dated snapshot of sorted `paper_ids` and `resource_ids` to `data/history.json`, or replace that day's snapshot if one already exists. Update `data/config.json` with the actual collection-update date; extend its search horizon only after completing the search.

```sh
python3 scripts/catalog.py build
python3 -m unittest discover -s tests
node tests/evidence_model_test.mjs
python3 scripts/catalog.py check
git diff
```

Stage only the reviewed source files and their generated outputs, commit with a descriptive message, and push to `origin main`. Confirm that the remote commit and Pages deployment succeeded. If correcting a release date, include the primary-source URL and date basis before rebuilding. A metadata-only correction does not create a collection-growth point.

The legacy `catalog.py import --source /path/to/overleaf-project` command **replaces collection membership with the source Literature Map**. It is for a deliberate, reviewed reconciliation, not daily updates: running it against an older manuscript can remove newer website entries. Compare both collections and retain reviewed additions before using it.

The GitHub issue template accepts paper suggestions and corrections. Contributions should give the title, primary-source link, suggested category, and a short explanation of relevance. Do not upload copyrighted paper PDFs.

## Daily literature update procedure

The daily schedule runs in the maintainer's local Codex session. The computer must be awake, Codex running, network access available and Git authentication valid. GitHub Actions handles validation and publication after a push; it does not perform the literature search itself. A missed or failed run must not be presented as a successful search.

1. **Resume safely.** Read the prior run record, inspect local changes, fetch the remote branch and fast-forward only when safe. Retry an unfinished push or deployment before creating duplicate additions. Never reset unrelated work or force-push.
2. **Search with overlap.** Start from the last completed search horizon, overlapping seven days to catch indexing delays. On Mondays, also check related surveys and citations of core studies for older omissions. Search harness optimization/evolution, recursive self-improvement, agent workflow search, and evolving tools, skills, memory and context. Save the actual queries, source URLs and date range in local run records outside this public repository.
3. **Verify and screen.** Prefer arXiv, OpenReview, ACL Anthology, official proceedings and author-released papers/code. Confirm identity, first release and any formal venue. Deduplicate preprint/published versions by identifiers and title/authors. Separate reusable harness or improver changes from single-task outputs and weight-only training; label related surveys and background methods accordingly. Keep uncertain candidates pending.
4. **Extract only supported claims.** Read the source before adding a mechanism summary or result. Concrete findings require a section, appendix, figure or implementation locator. Preserve the task setting, seed, actual change, retention status and attribution limits. New collection entries do not automatically expand the frozen domain-evidence snapshot.
5. **Update and publish.** Follow the incremental procedure above. Rebuild the README, aggregate charts, site data and downloadable bibliography; validate, inspect the diff, commit and push relevant changes. Verify the matching Pages run and public data before recording publication as complete. For substantive evidence revisions, preserve the original snapshot and publish a separately dated version with source-backed comparisons.
6. **Record the outcome accurately.** Keep completed-search and publication status separate. Do not fabricate a search cutoff, new publication date, growth point or empty commit when nothing qualifies. Retain pending candidates and specific failure details for the next run. No manuscript or Overleaf edits are part of this routine.

### Verify unattended publication

Run from the repository checkout. Confirm that `origin` is the expected project and that the current branch is `main`. After reviewing and committing only the intended changes, use non-interactive authentication so an expired credential fails instead of leaving the run waiting for input:

```sh
GIT_TERMINAL_PROMPT=0 git -c core.sshCommand='ssh -o BatchMode=yes -o ConnectTimeout=15' push --dry-run origin main
GIT_TERMINAL_PROMPT=0 git -c core.sshCommand='ssh -o BatchMode=yes -o ConnectTimeout=15' push origin main
GIT_TERMINAL_PROMPT=0 git -c core.sshCommand='ssh -o BatchMode=yes -o ConnectTimeout=15' ls-remote origin refs/heads/main
git rev-parse HEAD
```

The remote and local commit IDs must match. Check the Pages run for that same commit and the changed public site data before marking publication complete. A dry run verifies authentication and push negotiation, but does not publish a commit. A successful manual publication does not establish that a scheduled run can start, write files or complete unattended.

After a folder move, verify the scheduled chat's actual working directory and write access, not just the project's sidebar name. Keep separate local status fields for the completed literature search, commit/push, deployment, and scheduled-run test. If any stage fails, record the specific failure and resume that stage on the next run; do not advance research dates or create duplicate commits to mask a failure.

## Data definitions

| Field or file | Meaning |
| :-- | :-- |
| `data/literature.bib` | Bibliographic identity and source URL. The baseline came from the survey Literature Map; subsequent verified additions are maintained here. Extra manuscript references and aliases are not automatically included. |
| `data/annotations.json` | One annotation per citation key: primary category, record kind, method summary, release date with provenance, and first-added date. |
| `kind: paper` | A paper or manuscript in the literature map, including surveys, adjacent methods, and benchmarks. This is not a claim of peer review or RSI capability. |
| `kind: resource` | An official benchmark page, code resource, or implementation reference, counted separately from papers. |
| `category` | The primary thematic contribution, using the Literature Map's taxonomy for both baseline and later additions. Each record has one category so category totals do not double-count. |
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
node tests/evidence_model_test.mjs
node --check docs/app.js
node --input-type=module --check < docs/benchmarks.js
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000` for the standalone research homepage. Its domain tabs work without a backend. All assets are local, including the Manrope typeface (SIL Open Font License in `docs/assets/fonts/`). There are no analytics, remote font requests, or API keys.

## Paper page and citation metadata

`docs/paper/index.html` is the static scholarly landing page. Keep its complete abstract, author order, version date, `citation_*` tags and PDF link consistent with the same manuscript version and `docs/project.json`. Update both displayed BibTeX blocks and their downloadable `.bib` files together. The current author reading version and Preprints.org v1 are distinct: the v1 DOI must not be assigned to the revised reading PDF. Preserve dated PDFs and disclose version differences. Add a website release note for presentation changes; do not advance manuscript or evidence dates.

## Update domain findings

`docs/project.json` contains four domain summaries, 12 selected observations and three cross-domain comparisons. Each observation provides:

- Task setting and the concrete before/after change.
- An observed outcome and an evidence type (case, full-system result, ablation, or transfer).
- A limit on interpretation, especially component attribution and portability.
- Primary-source citation keys, links and section or artifact locators.

Read the relevant source before editing these fields. Supplied architecture, proposed changes, intermediate discoveries and retained modifications are not interchangeable. A task answer or generated image is not automatically a reusable harness artifact. Do not turn an overall score increase into a component-level causal claim.

The build checks count consistency, source identity and comparison-to-evidence links. It does **not** verify scientific claims. Cases cited in the manuscript but not in the curated Literature Map may appear in `additional_finding_sources` with an explicit scope note. They are excluded from collection statistics until formally imported into the Map.

The evidence summary is frozen separately from the working collection: the 95 category–source records cover four domains, 62 research papers and one benchmark resource through October 1, 2026. The website exposes all 95 records in the benchmark explorer and downloadable JSON, alongside 12 selected observations and 27 comparison lenses. Updating bibliography counts does not automatically extend that evidence cutoff or add new observations. Do not imply independent discoveries when a source appears in several categories.

Run `python3 scripts/catalog.py build` after changing findings or contributors so the README stays synchronized. The cumulative/monthly SVG charts, JSON and downloadable BibTeX are generated; edit their source data, not generated output.

## Visual design and attribution

Preserve the dark navy project identity, cyan/blue/violet/amber domain accents, local Manrope typeface and responsive layouts. The cross-domain comparison is accessible HTML connected to the same findings data as the atlas. Its diagrams label the final node as an intended output; these schematics are not extra measured results or demonstrations of transfer. Its cells link to source-bearing evidence disclosures; do not replace them with an untraceable illustration. Keep the page focused on findings and aggregate trends rather than a paper directory.

New research figures should be original, source-linked SVG diagrams or appropriately attributed reusable artwork. Check labels at desktop and mobile sizes, and provide informative alternative text. The animated spatial cover is project artwork, not a scientific result; its source lives in `docs/harness-field.js`. The older ribbon generator in `scripts/identity.py` also rewrites the banner and favicon; do not run it to update the current identity. The README mechanism map is generated from the same comparison data as the website, through `scripts/catalog.py`.

Contributor names and roles are stored in `docs/project.json`. Xin (Lucas) Yu leads research direction and editorial decisions; Codex is credited as an OpenAI AI assistant, not as a human researcher or scholarly author.

## GitHub hosting

The README displays aggregate counts, cumulative and monthly SVG charts, and collection updates, without enumerating papers. The `docs/` folder is also a complete static website.

The public website is hosted at https://lucasxinyu.github.io/harness-rsi/. GitHub Pages uses GitHub Actions: changes to `docs/` or the publication workflow on `main` trigger validation and deployment. Maintainers can also run **Publish literature website** manually. The workflow deploys only `docs/` and refuses to run on a private repository. Daily discovery and source verification follow the procedure above; deployment alone does not extend the research cutoff. The official-project branding identifies this repository as the project home; it does not imply that the survey has been published or accepted.

## File boundaries

Do not add private manuscript drafts, local audit ledgers, credentials, Overleaf exports, or third-party paper PDFs. The maintainer-authorized public author preprints are the explicit exceptions: `docs/paper/Harness_RSI_Preprint_2026-10-19.pdf` (archived submission-era reading copy) `docs/paper/Harness_RSI_Preprint_2026-10-20.pdf` (archived reading version), and `docs/paper/Harness_RSI_Preprint_2026-10-27.pdf` (current GitHub reading version). The README and website link to the current reading version; this does not change submitted manuscripts. Preserve all dated PDFs; publish later manuscript versions under new dated filenames and update the links without overwriting the earlier version. It is not peer-reviewed and does not imply platform posting or acceptance. Repository-specific files stay here; they do not get imported into the Overleaf project. The repository currently has no blanket license grant; source papers retain their original rights.


## Updating benchmark evidence

The benchmark explorer is a companion to the domain evidence, not a leaderboard. Keep each study's seed, evaluation setting, actual artifact and attribution limits together.

1. Review the source manuscript and the relevant primary paper or released artifact. Update the domain record before changing a synthesis.
2. Maintain explicit benchmark memberships in `data/evidence_annotations.json`. Distinguish transfer, evaluation and case settings. Do not infer a concrete mechanism for every dataset named by a paper.
3. Add comparison notes only where a record supports them. Use a note's optional `benchmarks` list to restrict it to supported settings; an empty list makes a note visible only at the broader category level. A Liar's Dice case, for example, must not become a Balatro discovery.
4. Import the reviewed appendix with `python3 scripts/import_evidence.py --source /path/to/section4_supp.tex --date YYYY-MM-DD`. Its sibling `literature.bib` supplies manuscript references. The importer refuses an unreviewed new record until its benchmark assignment exists.
5. Update `docs/updates.json` with the actual date, additions, corrections or changed conclusions. Preserve previous entries. Update the snapshot totals and cutoff in `docs/project.json` when the underlying evidence set changes. Bibliography imports have their own collection history.
6. Run the Python tests, `node tests/evidence_model_test.mjs`, `python3 scripts/catalog.py build` and `python3 scripts/catalog.py check`. Check the rendered site, then commit the data and interface together. Repository history retains earlier evidence versions.

`docs/evidence.json` contains the export date, source-file hash, all domain records, primary-source locators and curated comparisons. A source repeated across subcategories is not an independent replication. Benchmark/setting labels include study-specific cases and transfer suites; their number is not the number of independent evolution experiments. Tests verify structural consistency and attribution boundaries; they do not replace reading the primary evidence.
