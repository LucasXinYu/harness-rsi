#!/usr/bin/env python3
"""Build a living bibliography using only Python's standard library."""
import argparse
import collections
import calendar
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
FOCUS = 'Harness Optimization and Search Workflows'


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def bib_entries(text):
    entries = []
    for match in re.finditer(r'^@(\w+)\s*\{\s*([^,]+),', text, re.M):
        start = match.end()
        depth, i = 1, start
        while i < len(text) and depth:
            if text[i] == '{' and text[i-1] != '\\':
                depth += 1
            elif text[i] == '}' and text[i-1] != '\\':
                depth -= 1
            i += 1
        if depth:
            raise ValueError('Unclosed BibTeX entry: ' + match[2])
        body, fields = text[start:i-1], {}
        for field in re.finditer(r'^\s*(\w+)\s*=\s*', body, re.M):
            p = field.end()
            if body[p:p+1] == '{':
                d, j = 1, p+1
                while j < len(body) and d:
                    if body[j] == '{' and body[j-1] != '\\':
                        d += 1
                    elif body[j] == '}' and body[j-1] != '\\':
                        d -= 1
                    j += 1
                if d:
                    raise ValueError('Unclosed BibTeX field: ' + field[1])
                value = body[p+1:j-1]
            else:
                value = body[p:].split('\n')[0].rstrip(',').strip('"')
            fields[field[1].lower()] = value
        entries.append({'id': match[2].strip(), 'bib_type': match[1].lower(), **fields})
    keys = [e['id'] for e in entries]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate citation keys')
    return entries


def plain(text):
    text = re.sub(r'\\cite\w*\{[^}]*\}', '', text)
    text = re.sub(r'\\(?:par|entryspace|newpage)\b', ' ', text)
    text = re.sub(r'\\(?:tau)\b', 'τ', text)
    # Common TeX accents, including brace-wrapped forms.
    for accent, combining in [('"', '\u0308'), ("'", '\u0301'), ('`', '\u0300'), ('^', '\u0302')]:
        text = re.sub(r'\\' + re.escape(accent) + r'\{?([A-Za-z])\}?',
                      lambda m: unicodedata.normalize('NFC', m[1]+combining), text)
    text = re.sub(r'\\(?:textbf|emph|textit|texttt|textrm)\{([^{}]*)\}', r'\1', text)
    text = text.replace('\\&', '&').replace('\\%', '%').replace('\\_', '_')
    text = text.replace('$', '').replace('{', '').replace('}', '')
    text = text.replace('---', '—').replace('--', '–').replace('``', '“').replace("''", '”')
    return re.sub(r'\s+', ' ', text).strip()


def map_entries(text):
    result, category = {}, None
    tokens = list(re.finditer(r'^\\(section|subsection\*)\{(.+)\}\s*$', text, re.M))
    for i, token in enumerate(tokens):
        if token[1] == 'section':
            category = plain(token[2])
            continue
        end = tokens[i+1].start() if i+1 < len(tokens) else text.find('\\bibliographystyle', token.end())
        body = text[token.end():end if end != -1 else len(text)]
        reference = re.search(r'\\textbf\{Reference:\}\s*\\citep\{([^}]+)\}\.\\par', body)
        if not reference or not category:
            raise ValueError('Missing reference/category: ' + token[2])
        key = reference[1]
        if key in result:
            raise ValueError('Duplicate map reference: ' + key)
        prose = body[reference.end():]
        prose = re.sub(r'\\textbf\{(?:First submitted|Submitted):\}[^\n]*', '', prose)
        prose = re.sub(r'\\textbf\{Survey role:\}[^\n]*', '', prose)
        prose = prose.split('\\end{document}')[0]
        result[key] = {'category': category, 'summary': plain(prose), 'source_note': plain(body)}
    return result


def parse_day(value):
    for fmt in ('%Y-%m-%d', '%d %b %Y', '%d %B %Y'):
        try:
            return dt.datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def release_date(entry, note, metadata):
    # Existing primary-source audit dates and explicit first-submission notes only.
    for line in metadata.get('dates', []):
        match = re.search(r'Submitted on (\d{1,2} \w+ \d{4})', line)
        if match and parse_day(match[1]):
            return {'value': parse_day(match[1]), 'precision': 'day', 'basis': 'First arXiv submission',
                    'source': metadata.get('source_url', entry['url'])}
    match = re.search(r'First submitted:\s*(\d{4}-\d{2}-\d{2}|\d{1,2} \w+ \d{4})', note)
    if match and parse_day(match[1]):
        return {'value': parse_day(match[1]), 'precision': 'day', 'basis': 'First submission recorded in literature map', 'source': entry['url']}
    arxiv = entry.get('eprint', '')
    if re.match(r'^\d{4}\.\d+', arxiv):
        return {'value': '20'+arxiv[:2]+'-'+arxiv[2:4], 'precision': 'month',
                'basis': 'arXiv identifier month; exact day not recorded', 'source': entry['url']}
    year, month = entry.get('year', ''), entry.get('month', '').lower()[:3]
    if re.fullmatch(r'\d{4}', year):
        months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        if month in months:
            return {'value': f'{year}-{months.index(month)+1:02}', 'precision': 'month', 'basis': 'Bibliographic publication month (first public release unknown)', 'source': entry['url']}
        return {'value': year, 'precision': 'year', 'basis': 'Bibliographic publication year (first public release unknown)', 'source': entry['url']}
    return {'value': None, 'precision': 'unknown', 'basis': 'No publication date recorded', 'source': entry['url']}


def import_sources(source, date):
    dt.date.fromisoformat(date)
    bib = (source/'literature.bib').read_text()
    entries = bib_entries(bib)
    mapped = map_entries((source/'literature_map.tex').read_text())
    if {e['id'] for e in entries} != set(mapped):
        raise ValueError('BibTeX and literature map keys differ')
    previous_path = ROOT/'data/annotations.json'
    previous = read_json(previous_path) if previous_path.exists() else {}
    history_path = ROOT/'data/history.json'
    history = read_json(history_path) if history_path.exists() else []
    if history and date < history[-1]['date']:
        raise ValueError('Collection history cannot be backdated')
    meta_path = source/'notes/citation_audit/parsed_metadata.json'
    metadata = {v['key']: v for v in read_json(meta_path)} if meta_path.exists() else {}
    annotations = {}
    for e in entries:
        key, m = e['id'], mapped[e['id']]
        earlier_seen = [h['date'] for h in history if key in h['paper_ids']+h['resource_ids']]
        annotations[key] = {
            'category': m['category'],
            'kind': 'resource' if m['category'] == 'Official Benchmark and Implementation Resources' else 'paper',
            'summary': m['summary'],
            'added_on': previous.get(key, {}).get('added_on', min(earlier_seen) if earlier_seen else date),
            'release': previous.get(key, {}).get('release') or release_date(e, m['source_note'], metadata.get(key, {})),
        }
    (ROOT/'data/literature.bib').write_text(bib)
    write_json(previous_path, annotations)
    snapshot = {'date': date, 'paper_ids': sorted(k for k,a in annotations.items() if a['kind']=='paper'),
                'resource_ids': sorted(k for k,a in annotations.items() if a['kind']=='resource')}
    if not history or any(snapshot[k] != history[-1][k] for k in ('paper_ids','resource_ids')):
        if history and history[-1]['date'] == date:
            history[-1] = snapshot
        else:
            history.append(snapshot)
    write_json(history_path, history)
    config = read_json(ROOT/'data/config.json')
    config['updated_on'] = date
    config['source_sha256'] = hashlib.sha256(bib.encode()).hexdigest()
    write_json(ROOT/'data/config.json', config)


def load_catalog():
    entries = bib_entries((ROOT/'data/literature.bib').read_text())
    annotations = read_json(ROOT/'data/annotations.json')
    if {e['id'] for e in entries} != set(annotations):
        raise ValueError('Every BibTeX entry needs exactly one annotation')
    records, identifiers = [], set()
    for e in entries:
        a = annotations[e['id']]
        if a['kind'] not in ('paper', 'resource') or not a['category'] or not a['summary']:
            raise ValueError('Missing classification or summary: ' + e['id'])
        if not e.get('url', '').startswith('https://'):
            raise ValueError('Missing HTTPS primary source: ' + e['id'])
        for field in ('eprint', 'doi'):
            ident = e.get(field, '').lower()
            if not ident:
                continue
            ident = (field, re.sub(r'v\d+$', '', ident))
            if ident in identifiers:
                raise ValueError('Duplicate publication identifier: ' + str(ident))
            identifiers.add(ident)
        release = a['release']
        patterns = {'day': r'\d{4}-\d{2}-\d{2}', 'month': r'\d{4}-\d{2}', 'year': r'\d{4}'}
        precision = release['precision']
        if precision in patterns:
            if not re.fullmatch(patterns[precision], release['value']):
                raise ValueError('Invalid date precision: '+e['id'])
            dt.date.fromisoformat(release['value'] + {'day':'','month':'-01','year':'-01-01'}[precision])
        elif precision != 'unknown' or release['value'] is not None:
            raise ValueError('Unknown dates must be null')
        dt.date.fromisoformat(a['added_on'])
        records.append({'id': e['id'], 'title': plain(e['title']), 'authors': plain(e.get('author', '')),
                        'year': plain(e.get('year', 'n.d.')), 'url': e['url'],
                        'venue': plain(e.get('booktitle', e.get('journal', 'arXiv preprint' if e.get('eprint') else 'Manuscript / official resource'))),
                        'doi': e.get('doi'), 'arxiv': e.get('eprint'), **a})
    return records


def statistics(records, history):
    papers = [r for r in records if r['kind']=='paper']
    monthly = collections.Counter(r['release']['value'][:7] for r in papers if r['release']['precision'] in ('day','month'))
    focused = collections.Counter(r['release']['value'][:7] for r in papers if r['category']==FOCUS and r['release']['precision'] in ('day','month'))
    return {'papers': len(papers), 'resources': len(records)-len(papers),
            'categories': dict(collections.Counter(r['category'] for r in records)),
            'monthly': dict(sorted(monthly.items())), 'focus_monthly': dict(sorted(focused.items())),
            'monthly_coverage': sum(monthly.values()),
            'date_precision': dict(collections.Counter(r['release']['precision'] for r in papers)),
            'history': [{'date': h['date'], 'papers': len(h['paper_ids']), 'resources': len(h['resource_ids'])} for h in history]}


def publication_series(stats, cutoff):
    """Include empty elapsed months; never imply future months have zero papers."""
    through = dt.date.fromisoformat(cutoff)
    final_month = cutoff[:7]
    if any(month > final_month for month in stats['monthly']):
        raise ValueError('Publication month exceeds the search cutoff')
    first_year = min((int(month[:4]) for month in stats['monthly']), default=through.year)
    cumulative, rows = 0, []
    for year in range(first_year, through.year + 1):
        for month in range(1, (through.month if year == through.year else 12) + 1):
            key = f'{year}-{month:02}'
            count = stats['monthly'].get(key, 0)
            cumulative += count
            rows.append({'month': key, 'papers': count, 'cumulative': cumulative,
                         'partial': key == final_month and through.day < calendar.monthrange(year, month)[1]})
    return rows


def public_statistics(stats, config):
    return {'papers': stats['papers'], 'resources': stats['resources'],
            'monthly_coverage': stats['monthly_coverage'],
            'search_cutoff': config['search_cutoff'], 'updated_on': config['updated_on'],
            'timeline': publication_series(stats, config['search_cutoff']),
            'history': stats['history']}


def svg_timeline(stats, cutoff):
    year = int(cutoff[:4])
    rows = [r for r in publication_series(stats, cutoff) if r['month'].startswith(str(year))]
    left, top, plotw, ploth = 64, 85, 895, 220
    maximum = max(10, ((max(r['papers'] for r in rows)+9)//10)*10)
    slot = plotw / len(rows)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="390" viewBox="0 0 1000 390" role="img" aria-labelledby="title desc">',
           f'<title id="title">Collected papers by publication month · {year}</title>',
           '<desc id="desc">'+html.escape('; '.join(f'{r["month"]}: {r["papers"]}'+(' (partial month)' if r['partial'] else '') for r in rows))+'. Counts describe the survey collection, including related work, not all papers in the field.</desc>',
           '<rect width="1000" height="390" rx="12" fill="#f6f6f1"/>',
           '<g font-family="Arial,sans-serif" font-size="13" fill="#1b4033">',
           f'<text x="28" y="34" font-size="21">Collected papers by publication month</text><text x="28" y="57" fill="#6a796e">{year} · Search through {cutoff}</text>']
    for i in range(5):
        value = maximum*i/4
        y = top+ploth-ploth*i/4
        out += [f'<path d="M{left} {y}h{plotw}" stroke="#d9dfd3"/>', f'<text x="{left-12}" y="{y+4}" text-anchor="end" fill="#6a796e">{value:g}</text>']
    for i,row in enumerate(rows):
        x = left + slot * (i+.5)
        h = ploth * row['papers'] / maximum
        color = '#b27548' if row['partial'] else '#335e45'
        label = dt.date.fromisoformat(row['month']+'-01').strftime('%b') + ('*' if row['partial'] else '')
        out += [f'<rect x="{x-slot*.28:.1f}" y="{top+ploth-h:.1f}" width="{slot*.56:.1f}" height="{h:.1f}" rx="3" fill="{color}"/>',
                f'<text x="{x:.1f}" y="{top+ploth-h-10:.1f}" text-anchor="middle">{row["papers"]}</text>',
                f'<text x="{x:.1f}" y="{top+ploth+24}" text-anchor="middle" fill="#6a796e">{label}</text>']
    note = '* Partial month. ' if any(r['partial'] for r in rows) else ''
    out += [f'<text x="28" y="368" fill="#6a796e">{note}Known release months: {stats["monthly_coverage"]}/{stats["papers"]} papers. Official resources are excluded.</text></g></svg>']
    return '\n'.join(out)+'\n'


def markdown(stats, config, project):
    lines = ['![Harness RSI — A living research atlas](docs/assets/project-banner.svg)', '',
             '<p align="center"><strong>The official project repository for Harness RSI</strong><br>Research in progress · Survey and domain findings forthcoming</p>', '',
             '<p align="center"><a href="#living-collection">Collection activity</a> · <a href="#research-atlas">Research atlas</a> · <a href="#contributors">Contributors</a> · <a href="CONTRIBUTING.md">Contribute</a></p>', '',
             '## Research atlas', '',
             'We study **what an agent can change in its harness, what mechanisms emerge, and what evidence supports those changes** across task domains. The website is the visual companion: domain studies, annotated figures, and an evolving picture of the collected literature.', '',
             '| Editable harness | Evolved mechanism | Supporting evidence |',
             '| :-- | :-- | :-- |',
             '| Components and modification boundaries | Concrete changes in how the agent works | Source papers, artifacts, traces, and evaluations |', '',
             'The standalone homepage is ready for domain studies and a growing figure library, with expandable images and source captions. Findings remain unfilled until the research is ready.', '',
             '**Project links:** arXiv paper — forthcoming · Public website — forthcoming · [Bibliography data](data/literature.bib) · [Validation](https://github.com/LucasXinYu/harness-rsi/actions/workflows/validate.yml)', '',
             '## Living collection', '',
             f'**{stats["papers"]} papers & manuscripts** · **{stats["resources"]} official resources** · Updated **{config["updated_on"]}**', '',
             '![Collected papers by publication month](docs/assets/publication-timeline.svg)', '',
             f'The survey collection includes related methods, surveys, and benchmarks. **{stats["monthly_coverage"]}/{stats["papers"]} papers** have known release months and appear in these charts. Official resources are counted separately. Search through **{config["search_cutoff"]}**.', '',
             '<details>', '<summary>How to read the statistics</summary>', '',
             'The chart uses first arXiv submission where available and bibliographic publication dates otherwise. These counts describe our collection, not a census of the field or a count of methods that achieve RSI. Monthly and cumulative views exclude papers without month-level dates. The final month stops at the search cutoff.', '',
             'Publication dates and collection updates are different: the snapshots below record actual imports. The first snapshot is the baseline; earlier collection activity has not been reconstructed. Future imports extend this history, and removals can reduce the total.', '',
             '[Full data and date methodology](CONTRIBUTING.md#data-definitions)', '', '</details>', '',
             '### Collection updates', '',
             '| Collection snapshot | Papers | Official resources |', '| :-- | --: | --: |']
    lines += [f'| {h["date"]} | {h["papers"]} | {h["resources"]} |' for h in stats['history'][-5:]]
    lines += ['', '## Contributors', '', '| Contributor | Role | Contribution |', '| :-- | :-- | :-- |']
    for person in project.get('contributors', []):
        name = f'[{person["name"]}]({person["url"]})' if person.get('url') else person['name']
        lines += [f'| {name} | {person["role"]} | {person["description"]} |']
    lines += ['', '## Run the website', '',
              'A static website with local assets. No API keys, analytics, or third-party build dependencies.', '',
              '```sh', 'python3 -m http.server 8000 --directory docs', '```', '',
              'Open http://localhost:8000. Figure assets and captions are managed through `docs/project.json`; see the [figure guide](CONTRIBUTING.md#add-research-figures).', '',
              '## Keep it growing', '',
              '[Suggest a paper or correction](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml) · [Report a website issue](https://github.com/LucasXinYu/harness-rsi/issues/new?template=website.yml)', '',
              'Update the survey bibliography and Literature Map, then import them. One build refreshes the website statistics, chart, and this README together.', '',
              '```sh', 'python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD',
              'python3 -m unittest discover -s tests', 'python3 scripts/catalog.py check', '```', '',
              'See [CONTRIBUTING.md](CONTRIBUTING.md) for verification, attribution, figures, and update policies.', '']
    return '\n'.join(lines)


def outputs():
    records = load_catalog()
    config, history = read_json(ROOT/'data/config.json'), read_json(ROOT/'data/history.json')
    if not history:
        raise ValueError('Missing collection baseline')
    for a,b in zip(history,history[1:]):
        if a['date'] >= b['date']:
            raise ValueError('Snapshot dates must increase')
    for kind in ('paper','resource'):
        current = sorted(r['id'] for r in records if r['kind']==kind)
        if current != history[-1][kind+'_ids']:
            raise ValueError('Latest snapshot does not match current corpus; run import')
    stats = statistics(records, history)
    dataset = {'config':config, 'stats':stats, 'records':records}
    return {ROOT/'README.md': markdown(stats, config, read_json(ROOT/'docs/project.json')),
            ROOT/'docs/stats.json': json.dumps(public_statistics(stats, config), ensure_ascii=False, indent=2)+'\n',
            ROOT/'docs/catalog.json': json.dumps(dataset, ensure_ascii=False, indent=2)+'\n',
            ROOT/'docs/assets/publication-timeline.svg': svg_timeline(stats, config['search_cutoff'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command',required=True)
    imp = subs.add_parser('import', help='Import BibTeX + Literature Map; preserve collection dates')
    imp.add_argument('--source',type=Path,required=True)
    imp.add_argument('--date',required=True,help='Actual import date, YYYY-MM-DD; never a paper date')
    subs.add_parser('build')
    subs.add_parser('check')
    args = parser.parse_args()
    if args.command == 'import':
        import_sources(args.source,args.date)
    generated = outputs()
    if args.command == 'check':
        stale = [str(p.relative_to(ROOT)) for p,v in generated.items() if not p.exists() or p.read_text()!=v]
        if stale:
            raise SystemExit('Stale generated files: '+', '.join(stale))
    else:
        for p,v in generated.items():
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(v)
    records = load_catalog()
    print(f'Validated {len(records)} records; generated files are current.')


if __name__ == '__main__':
    main()
