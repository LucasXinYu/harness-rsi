#!/usr/bin/env python3
"""Build a living bibliography using only Python's standard library."""
import argparse
import collections
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


def svg_timeline(stats, year):
    width, height, left, top, plotw, ploth = 1000, 380, 64, 65, 900, 230
    values, focus_values = [], []
    for month in range(1,13):
        limit = f'{year}-{month:02}'
        values.append(sum(v for k,v in stats['monthly'].items() if k <= limit))
        focus_values.append(sum(v for k,v in stats['focus_monthly'].items() if k <= limit))
    maxmonth = max((int(m[5:]) for m in stats['monthly'] if m.startswith(str(year))), default=1)
    maximum = max(20, ((max(values)+39)//40)*40)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Publication timeline of the included literature</title>',
           '<desc id="desc">Cumulative included papers by release month; this is not the project collection history.</desc>',
           '<rect width="1000" height="380" rx="16" fill="#f5f7f3"/>',
           f'<g font-family="Arial,sans-serif" font-size="13" fill="#344c43"><text x="28" y="30" font-size="18" font-weight="bold">Included literature · cumulative by release month · {year}</text>']
    for i in range(5):
        value = maximum*i/4
        y = top+ploth-ploth*i/4
        out += [f'<path d="M{left} {y}h{plotw}" stroke="#d9e2dc"/>', f'<text x="{left-12}" y="{y+4}" text-anchor="end">{value:g}</text>']
    for i in range(maxmonth):
        x = left+plotw*i/11
        out.append(f'<text x="{x}" y="{top+ploth+24}" text-anchor="middle">{dt.date(year,i+1,1):%b}</text>')
    for data,color in [(values,'#195c47'),(focus_values,'#bf682f')]:
        points = [(left+plotw*i/11, top+ploth-ploth*value/maximum) for i,value in enumerate(data[:maxmonth])]
        out.append('<polyline fill="none" stroke="'+color+'" stroke-width="3" points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in points)+'"/>')
        for (x,y),value in zip(points,data):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/><text x="{x}" y="{y-12}" text-anchor="middle" fill="{color}">{value}</text>')
    out += ['<circle cx="32" cy="351" r="5" fill="#195c47"/><text x="44" y="355">All papers with a known release month</text>',
            '<circle cx="400" cy="351" r="5" fill="#bf682f"/><text x="412" y="355">Harness Optimization and Search Workflows category</text></g></svg>']
    return '\n'.join(out)+'\n'


def markdown(records, stats, config):
    lines = ['# Harness RSI', '', '**A living literature collection on agent harness optimization and recursive self-improvement.**', '',
             'Follow the methods, browse the papers, and track how this collection grows.', '',
             f'**{stats["papers"]} papers & manuscripts · {stats["resources"]} official resources · {len(stats["categories"])} thematic categories**', '',
             f'Literature search cutoff: **{config["search_cutoff"]}** · Collection updated: **{config["updated_on"]}**', '',
             '[Browse the bibliography](#literature-by-topic) · [BibTeX](data/literature.bib) · [Data & methodology](CONTRIBUTING.md) · [Suggest a paper](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml)', '',
             '![Publication timeline](docs/assets/publication-timeline.svg)', '',
             'The plot counts **included literature by release month**, using first arXiv submission when available and bibliographic publication dates otherwise. It includes older papers in the cumulative total. It is a view of our collection, not an estimate of every paper in the field. '+f'{stats["monthly_coverage"]}/{stats["papers"]} papers have month-level or finer dates; the others remain listed and are excluded from this monthly plot.', '',
             '## Scope', '',
             'The focus is persistent changes to an agent’s harness: its executable workflow, prompts, tools, memory mechanisms, and improvement process. The collection also includes related search, memory, training, evaluation, and infrastructure work. **Inclusion does not mean that a method achieves recursive self-improvement.** Categories describe primary contributions, not RSI capability levels.', '',
             'Sources and summaries are imported from our survey bibliography and Literature Map. This repository does not redistribute paper PDFs or contain the unpublished ACL manuscript. It is a curated working collection, not an exhaustive census or a replication of reported results.', '',
             '## Collection growth', '',
             'The initial import is a baseline, not historical evidence of when each paper was discovered. Future updates record dated snapshots; removals can reduce the total. Publication dates and `added_on` dates are kept separate.', '',
             '| Snapshot | Papers | Official resources |', '| :-- | --: | --: |']
    lines += [f'| {h["date"]} | {h["papers"]} | {h["resources"]} |' for h in stats['history']]
    lines += ['', '## Explore locally', '', '```sh', 'python3 -m http.server 8000 --directory docs', '```', '',
              'Open http://localhost:8000 for the searchable catalog, topic filters, monthly/quarterly publication views, and collection history. The static `docs/` directory is ready for GitHub Pages when public hosting is enabled.', '',
              '## Literature by topic', '', '| Topic | Records |', '| :-- | --: |']
    for category,count in stats['categories'].items():
        lines.append(f'| {category} | {count} |')
    for category in stats['categories']:
        lines += ['', f'### {category}', '']
        subset = [r for r in records if r['category']==category]
        subset.sort(key=lambda r:(r['release']['value'] or '',r['title']),reverse=True)
        for r in subset:
            date = r['release']['value'] or 'n.d.'
            lines += [f'- **[{r["title"]}]({r["url"]})** ({date}) — {r["summary"]}']
    lines += ['', '## Maintain this collection', '',
              'See [CONTRIBUTING.md](CONTRIBUTING.md) for the import, build, validation, and date policies. Bibliographic fields live in `data/literature.bib`; classification, summaries, date provenance, and first-added dates live in `data/annotations.json`. Charts, this README, and the website data are generated from them.', '',
              '```sh', 'python3 scripts/catalog.py import --source /path/to/overleaf-project --date YYYY-MM-DD',
              'python3 scripts/catalog.py build', 'python3 -m unittest discover -s tests', 'python3 scripts/catalog.py check', '```', '',
              'No external packages, API keys, or build service are required.', '']
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
    return {ROOT/'README.md': markdown(records, stats, config),
            ROOT/'docs/catalog.json': json.dumps(dataset, ensure_ascii=False, indent=2)+'\n',
            ROOT/'docs/assets/publication-timeline.svg': svg_timeline(stats, int(config['search_cutoff'][:4]))}


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
