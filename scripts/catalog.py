#!/usr/bin/env python3
"""Build a living bibliography using only Python's standard library."""
import argparse
import collections
import calendar
import datetime as dt
import hashlib
import html
import importlib.util
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
    missing = set(mapped) - {e['id'] for e in entries}
    if missing:
        raise ValueError('Literature Map references missing from BibTeX: ' + ', '.join(sorted(missing)))
    # The manuscript bibliography also contains supporting references and aliases.
    # Membership of this collection is defined by the curated Literature Map.
    entries = [e for e in entries if e['id'] in mapped]
    selected_bib = '\n\n'.join('@'+e['bib_type']+'{'+e['id']+',\n'+
        '\n'.join('  '+k+' = {'+v+'},' for k,v in e.items() if k not in ('id','bib_type'))+'\n}'
        for e in entries)+'\n'
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
    (ROOT/'data/literature.bib').write_text(selected_bib)
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
           '<rect width="1000" height="390" rx="12" fill="#0c1521"/>',
           '<g font-family="Arial,sans-serif" font-size="13" fill="#e9f2f6">',
           f'<text x="28" y="34" font-size="21">Collected papers by publication month</text><text x="28" y="57" fill="#9eb3c6">{year} · Search through {cutoff}</text>']
    for i in range(5):
        value = maximum*i/4
        y = top+ploth-ploth*i/4
        out += [f'<path d="M{left} {y}h{plotw}" stroke="#283b4b"/>', f'<text x="{left-12}" y="{y+4}" text-anchor="end" fill="#9eb3c6">{value:g}</text>']
    for i,row in enumerate(rows):
        x = left + slot * (i+.5)
        h = ploth * row['papers'] / maximum
        color = '#ffc080' if row['partial'] else '#8ec6ff'
        label = dt.date.fromisoformat(row['month']+'-01').strftime('%b') + ('*' if row['partial'] else '')
        out += [f'<rect x="{x-slot*.28:.1f}" y="{top+ploth-h:.1f}" width="{slot*.56:.1f}" height="{h:.1f}" rx="3" fill="{color}"/>',
                f'<text x="{x:.1f}" y="{top+ploth-h-10:.1f}" text-anchor="middle">{row["papers"]}</text>',
                f'<text x="{x:.1f}" y="{top+ploth+24}" text-anchor="middle" fill="#9eb3c6">{label}</text>']
    note = '* Partial month. ' if any(r['partial'] for r in rows) else ''
    out += [f'<text x="28" y="368" fill="#9eb3c6">{note}Known release months: {stats["monthly_coverage"]}/{stats["papers"]} papers. Official resources are excluded.</text></g></svg>']
    return '\n'.join(out)+'\n'


def validate_project(project, records):
    """Check traceability and aggregate consistency, not scientific claim truth."""
    pdf_url = project['paper'].get('pdf_url')
    if pdf_url:
        prefix = project['website_url'].rstrip('/') + '/paper/'
        if not pdf_url.startswith(prefix) or not re.fullmatch(r'[A-Za-z0-9_.-]+\.pdf', pdf_url[len(prefix):]):
            raise ValueError('Paper PDF must use the project paper directory')
        pdf_path = ROOT/'docs/paper'/pdf_url[len(prefix):]
        if not pdf_path.is_file() or not pdf_path.read_bytes().startswith(b'%PDF-'):
            raise ValueError('Paper PDF is missing or invalid')
        dt.date.fromisoformat(project['paper']['version_date'])
    profiles = project['paper']['author_profiles']
    if [person['name'] for person in profiles] != project['paper']['authors']:
        raise ValueError('Author profiles must match manuscript author order')
    for person in profiles:
        if not person.get('role') or not person.get('identity_sources'):
            raise ValueError('Author profile requires role and identity sources')
        if person.get('github_url') and not re.fullmatch(r'https://github\.com/[A-Za-z0-9-]+', person['github_url']):
            raise ValueError('Author GitHub URL must identify a profile')
    evidence, domains = project['evidence'], project['domains']
    catalog = {r['id']: r for r in records}
    for source in project.get('additional_finding_sources', []):
        if source['id'] in catalog or not source.get('note') or not source['url'].startswith('https://'):
            raise ValueError('Invalid additional finding source')
        catalog[source['id']] = source
    if sum(d['records'] for d in domains) != evidence['records']:
        raise ValueError('Domain record totals disagree with evidence summary')
    if sum(d['subcategories'] for d in domains) != evidence['subcategories']:
        raise ValueError('Subcategory totals disagree with evidence summary')
    dt.date.fromisoformat(evidence['cutoff'])
    identities = set()
    for domain in domains:
        for finding in domain['findings']:
            identity = (domain['id'], finding['id'])
            if identity in identities:
                raise ValueError('Duplicate finding identity')
            identities.add(identity)
            for field in ('before','after','result','evidence_type','limit'):
                if not finding.get(field):
                    raise ValueError('Missing finding evidence: '+field)
            if not finding['sources']:
                raise ValueError('Finding needs source evidence')
            for source in finding['sources']:
                if source['key'] not in catalog or not source['locator']:
                    raise ValueError('Missing source or evidence locator: '+source['key'])
                if source['url'] != catalog[source['key']]['url']:
                    raise ValueError('Finding source URL differs from bibliography: '+source['key'])
    for insight in project['insights']:
        for cell in insight['cells']:
            if (cell['domain'],cell['finding']) not in identities:
                raise ValueError('Cross-domain comparison points to missing evidence')
        domain_ids = {d['id'] for d in domains}
        comparison = insight.get('comparison', {})
        if {cell['domain'] for cell in insight['cells']} != domain_ids or len(insight['cells']) != len(domains):
            raise ValueError('Comparison needs exactly one observation per domain')
        if set(comparison.get('axes', {})) != domain_ids:
            raise ValueError('Comparison axes must cover the same domains as its evidence')
        if not all(comparison.get(k) for k in ('shared_move', 'difference', 'questions')):
            raise ValueError('Comparison needs a shared function, differences and reuse questions')
        for axis in comparison['axes'].values():
            if len(axis.get('pipeline', [])) != 3 or not all(axis['pipeline']) or not axis.get('artifact') or not axis.get('boundary'):
                raise ValueError('Incomplete comparison mechanism')


def validate_updates(updates, evidence):
    releases = updates['releases']
    if not releases or len({r['id'] for r in releases}) != len(releases):
        raise ValueError('Release IDs must be present and unique')
    dates = []
    for release in releases:
        dates.append(dt.date.fromisoformat(release['date']))
        if release.get('kind') not in ('website', 'evidence') or not release['changes']:
            raise ValueError('Release needs a kind and description')
    if dates != sorted(dates, reverse=True):
        raise ValueError('Release dates must be newest first')
    latest = next((r for r in releases if r['kind'] == 'evidence'), None)
    if not latest or latest['date'] != evidence['updated_on'] or latest['records'] != len(evidence['records']):
        raise ValueError('Latest evidence release must match the exported snapshot')
    if not any(r['kind'] == 'website' for r in releases):
        raise ValueError('Missing website release date')


def svg_mechanisms(project):
    """A compact repository overview generated from the website's comparison data."""
    import textwrap
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="642" viewBox="0 0 1120 642" role="img" aria-labelledby="title desc">',
        '<title id="title">Shared questions, task-specific harness edits</title>',
        '<desc id="desc">A four-domain comparison of interfaces, decision evidence and recovery. Each cell shows a selected harness edit and its input-to-intended-output relation. These are separate examples, not a combined pipeline or tested transfer.</desc>',
        '<rect width="1120" height="642" rx="12" fill="#0c1521"/>',
        '<g font-family="Arial,Helvetica,sans-serif">',
        '<text x="30" y="34" font-size="10" letter-spacing="1.7" fill="#79ead3">THE COMPARISON AT A GLANCE</text>',
        '<text x="30" y="75" font-size="29" fill="#e9f2f6">Shared questions. Task-specific edits.</text>',
        '<text x="30" y="102" font-size="13" fill="#a3b3c5">Read across a domain; compare down a question. The underlying changes stay linked to their sources.</text>']
    headers = ['Interface: what must stay intact?', 'Evidence: what changes a decision?', 'Recovery: what triggers a retry?']
    for i, header in enumerate(headers):
        x = 210 + 296*i
        out.append(f'<text x="{x}" y="145" font-size="12" fill="#b7cbdc">{html.escape(header)}</text>')
    colors = ['#79ead3', '#b6a4ff', '#ffc080', '#8ec6ff']
    for row, domain in enumerate(project['domains']):
        y = 162 + row*104
        color = colors[row]
        for n, line in enumerate(textwrap.wrap(domain['name'], 21)):
            out.append(f'<text x="30" y="{y+31+n*21}" font-size="15" font-weight="600" fill="{color}">{html.escape(line)}</text>')
        out.append(f'<text x="30" y="{y+84}" font-size="10" fill="#8ea7bc">{domain["records"]} category–source records</text>')
        for col, insight in enumerate(project['insights']):
            x = 202 + 296*col
            a,edit,b = insight['comparison']['axes'][domain['id']]['pipeline']
            out += [f'<rect x="{x}" y="{y}" width="281" height="92" rx="5" fill="#142231" stroke="#304559"/>',
                f'<path d="M{x+1} {y+5}V{y+87}" stroke="{color}" stroke-width="2"/>',
                f'<text x="{x+15}" y="{y+29}" font-size="16" fill="{color}">{html.escape(edit)}</text>']
            for n,line in enumerate(textwrap.wrap(a+' → '+b, 34)):
                out.append(f'<text x="{x+15}" y="{y+53+n*17}" font-size="12" fill="#b8c9d8">{html.escape(line)}</text>')
    out += ['<path d="M30 591H1090" stroke="#304559"/>',
        '<text x="30" y="615" font-size="11" fill="#9eb3c6">Selected mechanisms and intended outputs · Comparative synthesis, not evidence of cross-domain transfer</text>', '</g></svg>']
    return '\n'.join(out)+'\n'


def svg_cumulative(stats, cutoff):
    year = cutoff[:4]
    rows = [r for r in publication_series(stats, cutoff) if r['month'].startswith(year)]
    left, top, width, height = 60, 104, 884, 182
    maximum = max(50, ((rows[-1]['cumulative']+49)//50)*50)
    points = [(left+width*i/max(1,len(rows)-1), top+height*(1-r['cumulative']/maximum)) for i,r in enumerate(rows)]
    line = ' '.join(f'{x:.1f},{y:.1f}' for x,y in points)
    desc = '; '.join(f'{r["month"]}: {r["cumulative"]}' for r in rows)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="366" viewBox="0 0 1000 366" role="img" aria-labelledby="title desc">',
        '<title id="title">Cumulative collected literature by publication month</title>',
        '<desc id="desc">'+html.escape(desc)+'. Only papers with known months. Earlier years included.</desc>',
        '<rect width="1000" height="366" rx="16" fill="#0c1521"/>',
        '<g font-family="Arial,sans-serif" fill="#e9f2f6">',
        '<text x="30" y="35" font-size="21">A growing literature collection</text>',
        f'<text x="30" y="61" font-size="13" fill="#9eb3c6">{year} · Cumulative by release month · Search through {cutoff}</text>',
        f'<text x="945" y="37" text-anchor="end" font-size="24">{stats["papers"]} papers</text>',
        f'<text x="945" y="61" text-anchor="end" font-size="12" fill="#9eb3c6">{stats["resources"]} resources tracked separately</text>']
    for i in range(5):
        y = top+height*(1-i/4)
        out += [f'<path d="M{left} {y}h{width}" stroke="#283b4b"/>',f'<text x="{left-10}" y="{y+4}" text-anchor="end" font-size="11" fill="#9eb3c6">{maximum*i/4:g}</text>']
    out += [f'<polygon points="{left},{top+height} {line} {left+width},{top+height}" fill="#133632"/>',f'<polyline points="{line}" fill="none" stroke="#79ead3" stroke-width="2.5"/>']
    for row,(x,y) in zip(rows,points):
        label = dt.date.fromisoformat(row['month']+'-01').strftime('%b')+('*' if row['partial'] else '')
        out += [f'<circle cx="{x}" cy="{y}" r="4" fill="#79ead3"/>',f'<text x="{x}" y="{y-12}" text-anchor="middle" font-size="11">{row["cumulative"]}</text>',f'<text x="{x}" y="{top+height+23}" text-anchor="middle" font-size="11" fill="#9eb3c6">{label}</text>']
    out += [f'<text x="30" y="345" font-size="11" fill="#9eb3c6">{stats["monthly_coverage"]}/{stats["papers"]} papers have known months. * Partial month. Collection coverage, not a census or count of achieved RSI.</text></g></svg>']
    return '\n'.join(out)+'\n'


def validate_evidence(data, project, catalog_records):
    """Fail on broken provenance, mismatched coverage or cross-setting assignments."""
    dt.date.fromisoformat(data['updated_on'])
    dt.date.fromisoformat(data['cutoff'])
    records = {r['id']: r for r in data['records']}
    benchmarks = {b['id']: b for b in data['benchmarks']}
    sources = {r['id'] for r in catalog_records} | {r['id'] for r in project.get('additional_finding_sources', [])}
    if len(records) != len(data['records']) or len(benchmarks) != len(data['benchmarks']):
        raise ValueError('Duplicate evidence identity')
    if len(records) != project['evidence']['records']:
        raise ValueError('Evidence coverage total differs from manuscript snapshot')
    if len({r['key'] for r in records.values()}) != project['evidence']['papers'] + project['evidence']['resources']:
        raise ValueError('Evidence source count differs from manuscript snapshot')
    for domain in project['domains']:
        rows = [r for r in records.values() if r['domain'] == domain['id']]
        if len(rows) != domain['records'] or len({r['category_id'] for r in rows}) != domain['subcategories']:
            raise ValueError('Domain evidence counts disagree')
    used_benchmarks = set()
    for record in records.values():
        if record['key'] not in sources or not record['sources'] or not record['sections']:
            raise ValueError('Unresolved evidence source: '+record['id'])
        for source in record['sources']:
            if not source['url'].startswith('https://') or not source['locator']:
                raise ValueError('Evidence requires primary URL and locator')
        for setting in record['benchmarks']:
            if setting['id'] not in benchmarks or setting['role'] not in ('study','transfer','evaluation','case','setting'):
                raise ValueError('Unresolved benchmark or setting role')
            used_benchmarks.add(setting['id'])
    if used_benchmarks != set(benchmarks):
        raise ValueError('Benchmark has no supporting record')
    if len({p['id'] for p in data['patterns']}) != len(data['patterns']):
        raise ValueError('Duplicate pattern identity')
    for pattern in data['patterns']:
        if not pattern['cases'] or not pattern['lesson']:
            raise ValueError('Pattern lacks evidence')
        for case in pattern['cases']:
            if case['record'] not in records or not case['change']:
                raise ValueError('Pattern points to missing evidence')
            allowed = {b['id'] for b in records[case['record']]['benchmarks']}
            if not set(case.get('benchmarks', [])) <= allowed:
                raise ValueError('Pattern claims an unsupported benchmark scope')
            if not set(case.get('change_by_benchmark', {})) <= allowed:
                raise ValueError('Benchmark-specific text has an unsupported scope')


def markdown(stats, config, project, evidence_data, updates):
    evidence = project['evidence']
    website = next(r for r in updates['releases'] if r['kind']=='website')
    lines = ['![Harness RSI — How agent harnesses evolve](docs/assets/project-banner.svg)', '',
        '<p align="center"><strong>What actually evolves around the model?</strong><br>A curated, source-traceable evidence dataset and research atlas of reported agent-harness changes.<br><sub>Survey companion · Versioned data · Reported gains, failures and evidence limits</sub></p>', '',
        '<p align="center"><a href="'+html.escape(project['paper']['pdf_url'], quote=True)+'"><strong>Read the paper (PDF) ↗</strong></a> · <a href="https://lucasxinyu.github.io/harness-rsi/paper/">Abstract &amp; citation ↗</a> · <a href="https://lucasxinyu.github.io/harness-rsi/">Interactive website ↗</a> · <a href="https://lucasxinyu.github.io/harness-rsi/#benchmarks">Benchmark evidence</a> · <a href="https://lucasxinyu.github.io/harness-rsi/#activity">Literature growth</a></p>', '',
        f'**Author preprint · {project["paper"]["version_date"]} · Not peer-reviewed.** The GitHub reading version uses an independent single-column layout, not an ACL template. This revision integrates six newly collected studies and the October 24 manuscript update, with contextual synthesis through October 27; the October 1 frozen evidence is unchanged. It is not a replacement of the manuscripts submitted to ARR or Preprints.org. [October 19 submission-era copy](docs/paper/Harness_RSI_Preprint_2026-10-19.pdf) and [October 20 reading copy](docs/paper/Harness_RSI_Preprint_2026-10-20.pdf) remain archived; [Preprints.org v1](https://www.preprints.org/manuscript/202610.2293), posted October 23, is available under DOI [10.20944/preprints202610.2293.v1](https://doi.org/10.20944/preprints202610.2293.v1).', '',
        '<p align="center"><a href="#video-overview">Video</a> · <a href="#what-we-study">Our work</a> · <a href="#compare-the-mechanisms">Compare mechanisms</a> · <a href="#evidence-you-can-trace">Evidence</a> · <a href="#maintenance-and-versions">Maintenance</a> · <a href="#authors">Authors</a></p>', '',
        '**October 27 literature and manuscript update:** Six verified additions cover executor-specific harnesses, fallback routing, memory policies, skill distillation and evaluator validity. [Read the source-linked synthesis](docs/LITERATURE_UPDATE_2026-10-27.md). The updated reading PDF includes the October 24 draft; frozen evidence and submitted platform versions remain unchanged.', '',
        'We trace **what changed in the target-agent harness, what that change accomplished, and under which conditions it might be useful again**. The central object is a reusable change to an interface, parser, context rule, recovery branch or persistent skill. A benchmark score alone does not tell that story.', '',
        f'**{evidence["records"]} category–source records · {evidence["papers"]} research papers + {evidence["resources"]} benchmark resource · {evidence["subcategories"]} task subcategories · {len(project["domains"])} domains**', '',
        '## Video overview', '',
        'https://github.com/user-attachments/assets/0e9ac11f-9b77-4d50-b94d-86f829bbab5d', '',
        '**[▶ Watch the full 90-second overview](https://github.com/LucasXinYu/harness-rsi/blob/main/docs/assets/harness-rsi-overview.mp4)**', '',
        '90-second silent video · Inline preview: 720 × 900 · [Download the original 1080 × 1350 MP4 (20.8 MB)](https://github.com/LucasXinYu/harness-rsi/raw/refs/heads/main/docs/assets/harness-rsi-overview.mp4)', '',
        '## What we study', '',
        '| Question | What this project provides |', '| :-- | :-- |',
        '| **How is a harness improved?** | A comparison of editable components, proposers, evaluators, search and optimization history. The site explains how these parts interact. |',
        '| **Does the improver change too?** | A distinction between optimizing a task harness and reusing revised improvement capabilities in later rounds. Task gains alone do not establish general RSI. |',
        '| **What actually emerges?** | Task-organized records of seed capabilities, reported failures, concrete edits, outcomes and limits; comparisons of recurring functions and domain-specific implementations. |', '',
        'The website lets readers move from a research question to a concrete mechanism, then to benchmark-specific evidence and its primary source. It accompanies the survey with inspectable data and an interface for comparison.', '',
        '## Compare the mechanisms', '',
        '![Four domains compared through concrete interface, evidence and recovery edits](docs/assets/mechanism-map.svg)', '',
        'The interactive site lets you choose **any two domains** and switch between interfaces, decision evidence and recovery. Each comparison reveals the actual editable artifact, before/after behavior, reported result, source location and conditions for reuse. The diagram shows selected mechanisms and intended outputs; it does not claim that these changes compose into one pipeline or transfer across domains.', '']
    for insight in project['insights']:
        lines += ['**'+insight['title']+'** '+insight['summary'], '']
    lines += ['<details><summary>Representative observations and their sources</summary>', '',
        '| Domain | A concrete observation | Evidence boundary |', '| :-- | :-- | :-- |']
    selections = [('coding','bounded-context'),('reasoning','proof-state'),('interactive','physical-recovery'),('visual','visual-recheck')]
    for domain_id, finding_id in selections:
        domain = next(d for d in project['domains'] if d['id']==domain_id)
        finding = next(f for f in domain['findings'] if f['id']==finding_id)
        refs = ', '.join('['+x['name']+']('+x['url']+')' for x in finding['sources'])
        lines += ['| '+domain['name']+' | '+finding['result']+' '+refs+' | '+finding['limit']+' |']
    lines += ['', '</details>', '', '## Evidence dataset', '',
        '**Harness RSI Evidence Dataset v0.3.0** contains **132 category–source records, 100 distinct works and 32 scoped signals**. Nineteen records were added on November 1; earlier dataset releases remain immutable. Records are not independent interventions.', '',
        '**47 records with documented primary-source checks · 85 inherited narrative records · 0 independently human-adjudicated records.** Review provenance, training boundaries, transfer regimes, selection rules and scientific corrections are explicit. Seventeen checked records carry no coded outcome.', '',
        '[Inspect the dataset](https://lucasxinyu.github.io/harness-rsi/dataset/) · [Dataset card](DATASET_CARD.md) · [Curation protocol](DATASET_PROTOCOL.md) · [JSON](docs/dataset/v0.3.0/dataset.json) · [Normalized CSV](docs/dataset/v0.3.0/records.csv) · [Schema](docs/dataset/v0.3.0/schema.json) · [Quality report](docs/dataset/v0.3.0/quality-report.json) · [Corrections](docs/dataset/v0.3.0/corrections.json)', '',
        'This is targeted AI-assisted source inspection, not independent reproduction or exhaustive coverage. **Project-owned annotations and compilation are CC BY 4.0; third-party rights are excluded.** See [the license scope](LICENSE-DATA.md). [Historical v0.1.0](docs/dataset/v0.1.0/dataset.json) is preserved byte-for-byte; its HarnessX hit-rate interpretation is superseded by the correction notice.', '',
        '```sh', 'python3 examples/inspect_dataset.py --outcome regression', '```', '',
        '## Evidence you can trace', '',
        f'**{len(evidence_data["records"])} records** connect **{evidence["subcategories"]} task subcategories** to concrete studies. The benchmark explorer adds **{len(evidence_data["patterns"])} comparison lenses** and **12 selected domain observations**. Filter by domain, subcategory and benchmark/setting, then inspect the seed, actual edit, outcome and original evidence.', '',
        '**A record follows this chain:** task and seed → reported problem → reusable harness edit → observed result → primary-source location and limitations.', '',
        f'The frozen survey evidence covers work through **{evidence["cutoff"]}**. A record is one source within one subcategory: records may share a paper, include negative results or expose missing artifacts. They are not {evidence["records"]} independent effects. Full-system gains are not attributed to individual edits without supporting evidence. A transfer evaluation retains its original discovery setting.', '',
        '| Inspect or download | Contents |', '| :-- | :-- |',
        '| [Full evidence export](docs/evidence.json) | All domain records, benchmark memberships, comparisons and source locations |',
        '| [Selected findings and comparisons](docs/project.json) | Before/after changes, outcomes, evidence types and limits |',
        '| [Bibliography](data/literature.bib) / [catalog](docs/catalog.json) | Source identities, classification and publication-date provenance |',
        '| [Update history](docs/updates.json) / [data definitions](CONTRIBUTING.md#data-definitions) | Dated releases, counting rules and curation process |', '',
        '## Maintenance and versions', '', updates['commitment'], '',
        '**Literature synthesis through November 1, 2026.** [Read the latest comparison supplement](docs/LITERATURE_UPDATE_2026-11-01.md): optimizer evolution, memory governance, unchanged transfer and negative evidence. This adds 20 verified papers; 96 keyword hits remain unscreened. The manuscript has not been revised in this dataset release. The [October 27 supplement](docs/LITERATURE_UPDATE_2026-10-27.md) remains available. Earlier [October 20](docs/LITERATURE_UPDATE_2026-10-20.md) and [October 24](docs/LITERATURE_UPDATE_2026-10-24.md) syntheses remain traceable. Earlier PDFs, submitted manuscripts and the evidence dataset are preserved.', '',
        '| State | Date | What it means |', '| :-- | :-- | :-- |',
        f'| **Frozen paper evidence** | {evidence["cutoff"]} | {evidence["records"]} category–source records; evidence export dated {evidence_data["updated_on"]} |',
        f'| **Living literature collection** | {config["search_cutoff"]} | Search horizon; {stats["papers"]} papers and {stats["resources"]} official resources; collection updated {config["updated_on"]} |',
        f'| **Website update** | {website["date"]} | {website["title"]}; see [release notes](docs/updates.json) for the scope of this update |', '',
        '**Our maintenance commitments**', '']
    lines += ['- **'+policy['title']+'.** '+policy['text'] for policy in updates['policy']]
    lines += ['', updates['cadence'], '',
        'The workflow is **find and screen → trace the actual change → revise comparisons → validate and record a dated release**. A website redesign does not create a new evidence snapshot. An added bibliography entry does not automatically become evidence for a domain finding.', '',
        '[Suggest a paper](https://github.com/LucasXinYu/harness-rsi/issues/new?template=paper.yml) · [Correct an evidence record](https://github.com/LucasXinYu/harness-rsi/issues/new?template=evidence.yml) · [Curation and contribution guide](CONTRIBUTING.md). Community suggestions and source-backed corrections are welcome.', '',
        '## Living collection', '',
        f'**{stats["papers"]} collected papers & manuscripts** · **{stats["resources"]} official resources** · Collection updated **{config["updated_on"]}**', '',
        '![Cumulative collected literature by release month](docs/assets/collection-growth.svg)', '',
        f'This collection is broader and newer than the frozen domain evidence. It includes surveys, adjacent methods, benchmarks and supporting work. **{stats["monthly_coverage"]}/{stats["papers"]}** papers have known release months; year-only and undated records stay in the total but are not plotted. Resources are counted separately. These are collection statistics, not a census of the field or a count of methods achieving RSI.', '',
        '<details><summary>Monthly counts and actual collection updates</summary>', '',
        '![Monthly collected literature](docs/assets/publication-timeline.svg)', '',
        'Publication dates use the first arXiv submission where available, then recorded bibliographic dates or identifier months. Provenance is retained per entry. The latest plotted month may be incomplete. These dates differ from the import dates below; collection history is never reconstructed from publication dates.', '',
        '| Collection snapshot | Papers | Resources |', '| :-- | --: | --: |']
    lines += [f'| {h["date"]} | {h["papers"]} | {h["resources"]} |' for h in stats['history'][-5:]]
    lines += ['', '</details>', '', '## Website and local preview', '',
        '**Visit [lucasxinyu.github.io/harness-rsi](https://lucasxinyu.github.io/harness-rsi/)** — no sign-in required.', '',
        'The standalone site lives in `docs/`: an interactive harness cover, source-linked result spotlights, workflow explorer, two-domain comparison studio, benchmark evidence notebook, collection charts and dated maintenance notes. Assets and data are served locally; no account, API key or analytics are required.', '',
        '```sh', 'python3 -m http.server 8000 --directory docs', '```', '',
        'Open http://localhost:8000 for a local preview. Validated website changes pushed to `main` deploy to GitHub Pages; maintainers can also run the publication workflow manually.', '',
        '## Authors', '', '**'+project['paper']['title']+'**', '',
        '| Author | Role | GitHub |', '| :-- | :-- | :-- |']
    for person in project['paper']['author_profiles']:
        account = f'[@{person["github_url"].rsplit("/", 1)[-1]}]({person["github_url"]})' if person.get('github_url') else 'Awaiting confirmation'
        lines += [f'| {person["name"]} | {person["role"]} | {account} |']
    lines += ['', project['paper']['authorship_note'], '',
        f'Correspondence: [{project["paper"]["corresponding_email"]}](mailto:{project["paper"]["corresponding_email"]})', '',
        project['paper']['affiliation']+'<br>', project['paper']['location'], '',
        'The author-hosted reading copy and [Preprints.org v1](https://www.preprints.org/manuscript/202610.2293) are available. DOI: [10.20944/preprints202610.2293.v1](https://doi.org/10.20944/preprints202610.2293.v1). Neither version implies peer review or acceptance.', '',
        '## Contributors', '', 'The five survey authors are listed above with their research roles and verified GitHub links. Project development and AI assistance are listed separately below. GitHub’s automatic Contributors graph reflects attributed commits, not the manuscript author list.', '',
        '| Contributor | Role | Contribution |', '| :-- | :-- | :-- |']
    for person in project.get('contributors', []):
        name = f'[{person["name"]}]({person["url"]})' if person.get('url') else person['name']
        lines += [f'| {name} | {person["role"]} | {person["description"]} |']
    lines += ['', '<details><summary>Maintainer quick start</summary>', '',
        'Follow the [daily literature update procedure](CONTRIBUTING.md#daily-literature-update-procedure). Incremental updates edit `data/literature.bib` and `data/annotations.json`, with actual membership snapshots and dates. Do not reimport an older Overleaf collection over newer entries.', '',
        '```sh', 'python3 scripts/catalog.py build', 'python3 -m unittest discover -s tests',
        'node tests/evidence_model_test.mjs', 'python3 scripts/catalog.py check', '```', '',
        'The build synchronizes this README, diagrams, statistics and downloadable bibliography. Findings live in `docs/project.json`; benchmark assignments and comparative notes live in `data/evidence_annotations.json`. These are edited separately from bibliography counts. Follow the [evidence update procedure](CONTRIBUTING.md#updating-benchmark-evidence), add a dated release note, review the rendered site and commit the source and generated files together.', '',
        '[Validation workflow](https://github.com/LucasXinYu/harness-rsi/actions/workflows/validate.yml) · [Contribution guide](CONTRIBUTING.md)', '', '</details>', '']
    return '\n'.join(lines)


def outputs():
    records = load_catalog()
    config, history = read_json(ROOT/'data/config.json'), read_json(ROOT/'data/history.json')
    if not history:
        raise ValueError('Missing collection baseline')
    for a,b in zip(history,history[1:]):
        if a['date'] >= b['date']:
            raise ValueError('Snapshot dates must increase')
    added_dates = {record['id']: record['added_on'] for record in records}
    for snapshot in history:
        for kind in ('paper', 'resource'):
            for key in snapshot[kind + '_ids']:
                if key in added_dates and added_dates[key] > snapshot['date']:
                    raise ValueError('Snapshot predates first collection date: ' + key)
    for kind in ('paper','resource'):
        current = sorted(r['id'] for r in records if r['kind']==kind)
        if current != history[-1][kind+'_ids']:
            raise ValueError('Latest snapshot does not match current corpus; run import')
    stats = statistics(records, history)
    project = read_json(ROOT/'docs/project.json')
    evidence_data = read_json(ROOT/'docs/evidence.json')
    updates = read_json(ROOT/'docs/updates.json')
    validate_project(project, records)
    validate_evidence(evidence_data, project, records)
    validate_updates(updates, evidence_data)
    dataset = {'config':config, 'stats':stats, 'records':records}
    dataset_spec = importlib.util.spec_from_file_location('harness_dataset', ROOT/'scripts/dataset.py')
    dataset_module = importlib.util.module_from_spec(dataset_spec)
    dataset_spec.loader.exec_module(dataset_module)
    return {**dataset_module.dataset_outputs(ROOT),
            ROOT/'README.md': markdown(stats, config, project, evidence_data, updates),
            ROOT/'docs/assets/mechanism-map.svg': svg_mechanisms(project),
            ROOT/'docs/stats.json': json.dumps(public_statistics(stats, config), ensure_ascii=False, indent=2)+'\n',
            ROOT/'docs/catalog.json': json.dumps(dataset, ensure_ascii=False, indent=2)+'\n',
            ROOT/'docs/assets/publication-timeline.svg': svg_timeline(stats, config['search_cutoff']),
            ROOT/'docs/assets/collection-growth.svg': svg_cumulative(stats, config['search_cutoff']),
            ROOT/'docs/literature.bib': (ROOT/'data/literature.bib').read_text()}


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
