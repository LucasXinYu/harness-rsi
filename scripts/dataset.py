"""Build a versioned, additive view of the unchanged survey evidence."""
import csv
import hashlib
import io
import json
import re


OUTCOMES = ('improvement', 'regression', 'no_gain', 'mixed', 'not_assessed')
RETENTION = ('retained', 'rejected', 'rolled_back', 'not_reported', 'not_assessed')
ATTRIBUTION = ('illustrative_case', 'full_system_comparison', 'reported_proposal_test',
               'usage_observation', 'component_ablation', 'not_assessed')
COMPONENTS = ('instructions', 'tools', 'context', 'memory', 'control')


def serialize(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def validate_annotations(evidence, annotations):
    records = {record['id']: record for record in evidence['records']}
    if set(annotations) - records.keys():
        raise ValueError('Dataset annotation refers to an unknown record')
    for record_id, annotation in annotations.items():
        record = records[record_id]
        signals = annotation['signals']
        if not signals or len({signal['id'] for signal in signals}) != len(signals):
            raise ValueError('Missing or duplicate signal ID')
        for signal in signals:
            if not re.fullmatch(r'[a-z0-9-]+', signal['id']):
                raise ValueError('Invalid signal ID')
            for field, vocabulary in [('outcome', OUTCOMES), ('retention', RETENTION),
                                      ('attribution', ATTRIBUTION)]:
                if signal[field] not in vocabulary:
                    raise ValueError('Invalid ' + field)
            if not signal['components'] or set(signal['components']) - set(COMPONENTS):
                raise ValueError('Invalid component')
            if set(signal['benchmark_ids']) - {item['id'] for item in record['benchmarks']}:
                raise ValueError('Signal has an unrelated benchmark')
            sections = {section['label']: section['text'] for section in record['sections']}
            quote = signal['evidence_quote']
            if not quote or quote not in sections.get(signal['section'], ''):
                raise ValueError('Signal excerpt is not in its frozen record')
            source_index = signal['source_index']
            if type(source_index) is not int or not 0 <= source_index < len(record['sources']):
                raise ValueError('Invalid source index')
            if not signal['scope'] or not signal['summary']:
                raise ValueError('Signal requires scope and interpretation')


def dataset_outputs(root):
    if (root / 'data/dataset_v020/release.json').exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('dataset_v020', root / 'scripts/dataset_v020.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.outputs(root)
    evidence_bytes = (root / 'docs/evidence.json').read_bytes()
    evidence = json.loads(evidence_bytes)
    config = json.loads((root / 'data/dataset.json').read_text())
    annotations = json.loads((root / 'data/dataset_annotations.json').read_text())
    annotation_digest = hashlib.sha256((root / 'data/dataset_annotations.json').read_bytes()).hexdigest()
    if annotation_digest != config['annotations_sha256']:
        raise ValueError('Dataset annotations changed: review and version the release explicitly')
    digest = hashlib.sha256(evidence_bytes).hexdigest()
    if digest != config['frozen_evidence_sha256']:
        raise ValueError('Frozen evidence changed: create a reviewed dataset version, do not silently rebase')
    if not re.fullmatch(r'\d+\.\d+\.\d+', config['version']):
        raise ValueError('Invalid dataset version')
    validate_annotations(evidence, annotations)
    records = []
    for record in evidence['records']:
        signals = annotations.get(record['id'], {}).get('signals', [])
        expanded = []
        for signal in signals:
            source = record['sources'][signal['source_index']]
            expanded.append({**signal, 'primary_source': source})
        records.append({**record, 'annotation_status': 'record_screened' if signals else 'not_reviewed',
                        'selection_protocol': None, 'controlled_variables': None,
                        'signals': expanded})
    metadata = {**config, 'evidence_cutoff': evidence['cutoff'],
                'record_count': len(records),
                'distinct_source_count': len({record['key'] for record in records}),
                'screened_record_count': len(annotations),
                'unreviewed_record_count': len(records) - len(annotations),
                'signal_count': sum(len(record['signals']) for record in records)}
    dataset = {'metadata': metadata, 'records': records}
    schema = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'title': config['name'] + ' record', 'type': 'object',
        'required': ['id', 'key', 'domain', 'category', 'sections', 'sources', 'benchmarks',
                     'annotation_status', 'selection_protocol', 'controlled_variables', 'signals'],
        'properties': {
            'id': {'type': 'string'}, 'key': {'type': 'string'},
            'domain': {'type': 'string'}, 'category': {'type': 'string'},
            'category_id': {'type': 'string'}, 'title': {'type': 'string'},
            'evidence_status': {'type': 'string'},
            'sections': {'type': 'array', 'items': {'type': 'object', 'required': ['label', 'text']}},
            'sources': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'url', 'locator']}},
            'benchmarks': {'type': 'array', 'items': {'type': 'object', 'required': ['id', 'role']}},
            'annotation_status': {'enum': ['record_screened', 'not_reviewed']},
            'selection_protocol': {'type': ['string', 'null']},
            'controlled_variables': {'type': ['array', 'null'], 'items': {'type': 'string'}},
            'signals': {'type': 'array', 'items': {
                'type': 'object',
                'required': ['id', 'outcome', 'retention', 'attribution', 'components', 'benchmark_ids',
                             'scope', 'summary', 'section', 'evidence_quote', 'source_index', 'primary_source'],
                'properties': {
                    'id': {'type': 'string'}, 'outcome': {'enum': list(OUTCOMES)},
                    'retention': {'enum': list(RETENTION)}, 'attribution': {'enum': list(ATTRIBUTION)},
                    'components': {'type': 'array', 'items': {'enum': list(COMPONENTS)}, 'minItems': 1},
                    'benchmark_ids': {'type': 'array', 'items': {'type': 'string'}},
                    'scope': {'type': 'string'}, 'summary': {'type': 'string'},
                    'section': {'type': 'string'}, 'evidence_quote': {'type': 'string'},
                    'source_index': {'type': 'integer', 'minimum': 0},
                    'primary_source': {'type': 'object', 'required': ['name', 'url', 'locator']}
                }
            }}
        }
    }
    table = io.StringIO(newline='')
    columns = ['id', 'key', 'domain', 'category', 'title', 'annotation_status',
               'selection_protocol', 'controlled_variables', 'benchmarks', 'sections', 'sources', 'signals']
    writer = csv.DictWriter(table, fieldnames=columns, lineterminator='\n')
    writer.writeheader()
    for record in records:
        writer.writerow({field: json.dumps(record[field], ensure_ascii=False)
                         if isinstance(record[field], (list, dict)) or record[field] is None
                         else record[field] for field in columns})
    release = root / 'docs/dataset' / ('v' + config['version'])
    files = {
        release / 'dataset.json': serialize(dataset),
        release / 'records.jsonl': ''.join(json.dumps(record, ensure_ascii=False) + '\n' for record in records),
        release / 'records.csv': table.getvalue(),
        release / 'schema.json': serialize(schema),
        release / 'DATASET_CARD.md': (root / 'DATASET_CARD.md').read_text(),
        release / 'citation.bib': ('@misc{harness_rsi_evidence_v010,\n'
                                 '  title = {Harness RSI Evidence Dataset},\n'
                                 '  author = {{Harness RSI project team}},\n'
                                 '  year = {2026},\n  version = {' + config['version'] + '},\n'
                                 '  url = {https://lucasxinyu.github.io/harness-rsi/dataset/v' + config['version'] + '/dataset.json},\n'
                                 '  note = {Category-source evidence records; frozen literature cutoff ' + evidence['cutoff'] + '}\n}\n')
    }
    files[release / 'checksums.json'] = serialize({path.name: hashlib.sha256(content.encode()).hexdigest()
                                                for path, content in files.items()})
    files[root / 'docs/dataset/latest.json'] = serialize({
        'version': config['version'], 'released_on': config['released_on'],
        'path': 'dataset/v' + config['version'] + '/dataset.json',
        'sha256': hashlib.sha256(files[release / 'dataset.json'].encode()).hexdigest()})
    return files
