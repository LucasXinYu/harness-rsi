#!/usr/bin/env python3
"""Export the survey's domain records; keep benchmark assignments explicitly curated.

Usage: python3 scripts/import_evidence.py --source /path/to/section4_supp.tex --date YYYY-MM-DD
The export does not infer benchmark-specific mechanisms from a paper's evaluation list.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def argument(text, start):
    if text[start] != '{':
        raise ValueError('Expected braced argument')
    depth, pos = 1, start + 1
    while depth:
        if pos >= len(text):
            raise ValueError('Unclosed TeX argument')
        if text[pos] == '\\':
            pos += 2
            continue
        if text[pos] == '{':
            depth += 1
        elif text[pos] == '}':
            depth -= 1
        pos += 1
    return text[start + 1:pos - 1], pos


def plain(text):
    text = re.sub(r'(?m)(?<!\\)%.*$', '', text)
    text = text.replace('\\textquotesingle ', "'").replace("Pok\\'emon", 'Pokémon')
    text = text.replace('G\\"{o}del', 'Gödel')
    for cmd, keep in [('texorpdfstring', 0), ('href', 1), ('hyperref', 0)]:
        pattern = r'\\' + cmd + (r'\[[^\]]*\]' if cmd == 'hyperref' else '') + r'(?=\{)'
        while (match := re.search(pattern, text)):
            a, end = argument(text, match.end())
            if cmd != 'hyperref':
                b, end = argument(text, end)
                a = [a, b][keep]
            text = text[:match.start()] + a + text[end:]
    text = re.sub(r'\\(?:label|input)\{[^}]*\}', '', text)
    text = re.sub(r'\\(?:phantomsection|allowbreak)(?:\{\})?', '', text)
    text = text.replace('\\S{}', '§').replace('\\tau', 'τ').replace('\\pi', 'π')
    text = text.replace('\\pm', ' ± ').replace('\\times', '×')
    text = text.replace('$^2$', '²').replace('^2', '²').replace('^3', '³').replace('_{0.5}', '₀.₅')
    text = re.sub(r'\\(?:texttt|textit|emph|textbf|mbox)\{([^{}]*)\}', r'\1', text)
    text = text.replace('\\%', '%').replace('\\_', '_').replace('\\&', '&').replace('\\,', ' ')
    text = text.replace('---', '—').replace('--', '–').replace('~', ' ').replace('$', '')
    text = text.replace('{', '').replace('}', '')
    text = re.sub(r'\s+', ' ', text).strip()
    if '\\' in text:
        raise ValueError('Unconverted TeX: ' + text)
    return text


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def extract(path, catalog):
    text = path.read_text()
    sources = {}
    for line in text.splitlines():
        match = re.match(r'\\item\[(S\d+)\.\].*?\\href\{([^}]+)\}\{([^}]+)\}\.(.*)', line)
        if match:
            sid, url, name, locator = match.groups()
            sources[sid] = {'name': plain(name), 'url': url, 'locator': plain(locator)}
    events = list(re.finditer(r'\\(section|subsection|subsubsection|SecFourSuppEntry)\{', text))
    domain, category, records = None, None, []
    for index, event in enumerate(events):
        kind = event[1]
        title, end = argument(text, event.end() - 1)
        if kind == 'section':
            domain = next((key for prefix, key in [('Coding', 'coding'), ('Reasoning', 'reasoning'), ('Interactive', 'interactive'), ('Visual', 'visual')] if title.startswith(prefix)), None)
        elif kind in ('subsection', 'subsubsection'):
            category = plain(title)
        elif domain:
            citation, start = argument(text, end)
            stop = events[index + 1].start() if index + 1 < len(events) else len(text)
            body = text[start:stop]
            # A concluding synthesis belongs to the subcategory, not its last study.
            body = body.split('\\paragraph{')[0].split('\\clearpage')[0]
            cite = re.search(r'\\cite\w*(?:\[([^\]]*)\])?\{([^}]+)\}', citation)
            key = cite[2]
            fields = list(re.finditer(r'\\SecFourSuppField\{([^}]+)\}', body))
            sections = []
            for i, field in enumerate(fields):
                endfield = fields[i + 1].start() if i + 1 < len(fields) else len(body)
                sections.append({'label': plain(field[1]).rstrip('.'), 'text': plain(body[field.end():endfield])})
            if not fields:
                sections.append({'label': 'Documented artifact', 'text': plain(body)})
            ids = re.findall(r'\\hyperref\[sec4supp:source:(S\d+)\]', citation)
            refs = [sources[sid] for sid in ids]
            if key == 'sica2025':
                refs = [{**ref, 'locator': ref['locator'] + '; Appendix D, updates 6, 8–10, 13–14'} for ref in refs]
            if not refs:
                refs = [{'name': plain(title).split(':')[0].rstrip('.'), 'url': catalog[key]['url'], 'locator': plain(cite[1] or '')}]
            category_id = slug(category)
            records.append({'id': category_id + '--' + key, 'domain': domain,
                'category': category, 'category_id': category_id, 'key': key,
                'title': plain(title).rstrip('.'), 'sections': sections, 'sources': refs})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--date', required=True)
    args = parser.parse_args()
    dt.date.fromisoformat(args.date)
    catalog = {row['id']: row for row in json.loads((ROOT/'docs/catalog.json').read_text())['records']}
    from catalog import bib_entries
    manuscript_sources = {row['id']: row for row in bib_entries((args.source.parent/'literature.bib').read_text())}
    catalog = {**manuscript_sources, **catalog}
    records = extract(args.source, catalog)
    annotations = json.loads((ROOT/'data/evidence_annotations.json').read_text())
    if set(annotations['records']) != {r['id'] for r in records}:
        raise ValueError('Every imported record must have a reviewed benchmark assignment; update annotations first')
    for record in records:
        record.update(annotations['records'][record['id']])
    result = {'updated_on': args.date, 'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
        'source_file': args.source.name, 'cutoff': annotations['cutoff'],
        'benchmarks': annotations['benchmarks'], 'patterns': annotations['patterns'], 'records': records}
    (ROOT/'docs/evidence.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Exported {len(records)} domain records with source locators.')


if __name__ == '__main__':
    main()
