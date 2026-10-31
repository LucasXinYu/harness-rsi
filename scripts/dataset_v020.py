"""Deterministic, relational exports for the reviewed evidence release."""
import collections
import csv
import hashlib
import io
import json
import re

OUTCOMES = ['improvement', 'regression', 'no_gain', 'mixed', 'not_assessed']
ATTRIBUTIONS = ['illustrative_case', 'full_system_comparison', 'reported_proposal_test',
                'usage_observation', 'component_ablation', 'reported_edit_outcome', 'not_assessed']
BOUNDARIES = ['not_assessed', 'fixed_executor', 'auxiliary_weights_trained', 'executor_weights_trained']

def dumps(x): return json.dumps(x, ensure_ascii=False, indent=2) + '\n'
def digest(x): return hashlib.sha256(x).hexdigest()
def read(path): return json.loads(path.read_text())
def csv_text(rows, columns):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=columns, lineterminator='\n')
    writer.writeheader()
    for row in rows: writer.writerow({key: row.get(key) for key in columns})
    return out.getvalue()

def schema():
    string = {'type': 'string', 'minLength': 1}
    nullable = {'type': ['string', 'null']}
    support = {'type': ['object', 'null'], 'required': ['url', 'locator', 'excerpt', 'artifact_sha256', 'checked_on'],
               'properties': {'url': {'type': 'string', 'format': 'uri'}, 'locator': string, 'excerpt': string,
                              'artifact_sha256': {'type': 'string', 'pattern': '^[a-f0-9]{64}$'},
                              'checked_on': {'type': 'string', 'format': 'date'}}, 'additionalProperties': False}
    source = {'type': 'object', 'required': ['name', 'url', 'locator', 'source_version', 'first_release_date',
                 'source_version_date', 'metadata_checked_on', 'metadata_basis'],
              'properties': {**{k: string for k in ['name', 'locator', 'metadata_basis']},
                 'url': {'type': 'string', 'format': 'uri'},
                 **{k: nullable for k in ['source_version', 'first_release_date', 'source_version_date', 'metadata_checked_on']}},
              'additionalProperties': False}
    signal = {'type': 'object', 'required': ['id', 'outcome', 'retention', 'attribution', 'components',
                 'benchmark_ids', 'scope', 'summary', 'section', 'evidence_quote', 'source_index', 'primary_source', 'primary_support'],
              'properties': {
                  **{k: string for k in ['id', 'scope', 'summary', 'section', 'evidence_quote']},
                  'outcome': {'enum': OUTCOMES},
                  'retention': {'enum': ['retained', 'rejected', 'rolled_back', 'not_reported', 'not_assessed']},
                  'attribution': {'enum': ATTRIBUTIONS},
                  'components': {'type': 'array', 'minItems': 1, 'uniqueItems': True,
                                 'items': {'enum': ['instructions', 'tools', 'context', 'memory', 'control']}},
                  'benchmark_ids': {'type': 'array', 'uniqueItems': True, 'items': string},
                  'source_index': {'type': 'integer', 'minimum': 0},
                  'primary_source': {'type': 'object', 'required': ['name', 'url', 'locator']},
                  'primary_support': support}, 'additionalProperties': False}
    props = {k: string for k in ['id', 'key', 'domain', 'category', 'category_id', 'title', 'evidence_status', 'transfer_regime']}
    props.update({
        'annotation_status': {'enum': ['record_screened', 'not_reviewed', 'record_reviewed_no_signal']},
        'selection_protocol': nullable,
        'controlled_variables': {'type': ['array', 'null'], 'items': string},
        'weight_update_boundary': {'enum': BOUNDARIES},
        'sections': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['label', 'text'],
                     'properties': {'label': string, 'text': string}, 'additionalProperties': False}},
        'sources': {'type': 'array', 'minItems': 1, 'items': source},
        'benchmarks': {'type': 'array', 'items': {'type': 'object', 'required': ['id', 'role'],
                       'properties': {'id': string, 'role': string}, 'additionalProperties': False}},
        'signals': {'type': 'array', 'items': signal},
        'provenance': {'type': 'object', 'required': ['introduced_in', 'original_record_id', 'legacy_evidence_cutoff'],
                       'properties': {'introduced_in': string, 'original_record_id': nullable, 'legacy_evidence_cutoff': nullable},
                       'additionalProperties': False},
        'missingness': {'type': 'object', 'required': ['selection_protocol', 'controlled_variables'],
                       'properties': {k: {'enum': ['not_assessed', 'reported', 'not_reported']} for k in ['selection_protocol', 'controlled_variables']},
                       'additionalProperties': False},
        'review': {'type': 'object', 'required': ['status', 'reviewed_on', 'reviewer', 'human_review_status', 'scope'],
                   'properties': {'status': {'enum': ['legacy_curated', 'primary_source_checked']},
                     'reviewed_on': nullable, 'reviewer': nullable, 'human_review_status': {'enum': ['pending', 'not_recorded', 'adjudicated']},
                     'scope': string, 'primary_support': support}, 'additionalProperties': False}
    })
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'Harness RSI evidence record v0.2', 'type': 'object',
            'required': list(props), 'properties': props, 'additionalProperties': False}

def validate(records, sources):
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate record ID')
    keys = [s['key'] for s in sources]
    if len(keys) != len(set(keys)): raise ValueError('Duplicate source key')
    arxiv_ids = [s['arxiv_id'] for s in sources if s['arxiv_id']]
    if len(arxiv_ids) != len(set(arxiv_ids)): raise ValueError('Duplicate canonical arXiv work')
    if set(keys) != {r['key'] for r in records}: raise ValueError('Source registry membership mismatch')
    for r in records:
        if r['id'] != r['category_id']+'--'+r['key']: raise ValueError('Unstable record identity')
        if r['weight_update_boundary'] not in BOUNDARIES: raise ValueError('Invalid weight boundary')
        checked = r['review']['status'] == 'primary_source_checked'
        expected_status = ('record_screened' if r['signals'] else
                           'record_reviewed_no_signal' if checked else 'not_reviewed')
        if r['annotation_status'] != expected_status: raise ValueError('Annotation status contradicts review/signals')
        if checked and (not r['review']['reviewed_on'] or not r['selection_protocol']):
            raise ValueError('Source review lacks date or selection protocol')
        if not checked and r['review']['reviewed_on']: raise ValueError('Inherited row cannot claim current review')
        for field in ['selection_protocol', 'controlled_variables']:
            if (r[field] is not None) != (r['missingness'][field] == 'reported'):
                raise ValueError('Missingness contradicts value')
        sigids = [s['id'] for s in r['signals']]
        if len(sigids) != len(set(sigids)): raise ValueError('Duplicate signal ID')
        for s in r['signals']:
            if s['outcome'] not in OUTCOMES or s['attribution'] not in ATTRIBUTIONS: raise ValueError('Invalid signal label')
            if set(s['benchmark_ids']) - {b['id'] for b in r['benchmarks']}: raise ValueError('Unrelated signal benchmark')
            text = next((x['text'] for x in r['sections'] if x['label'] == s['section']), '')
            if not s['evidence_quote'] or s['evidence_quote'] not in text: raise ValueError('Fabricated curated excerpt')
            if not 0 <= s['source_index'] < len(r['sources']): raise ValueError('Invalid source index')
            p = s['primary_support']
            if not checked or not p or not re.fullmatch('[a-f0-9]{64}', p['artifact_sha256']):
                raise ValueError('Signal lacks inspected primary support')
            ident = re.search(r'\d{4}\.\d{4,5}v\d+', p['url'])
            actual = r['sources'][s['source_index']]['url']
            if ident and ident[0] not in actual: raise ValueError('Signal source-version mismatch')
            if len(p['excerpt'].split()) > 25: raise ValueError('Support excerpt too long')

def outputs(root):
    d = root/'data/dataset_v020'
    config = read(d/'release.json')
    for name, expected in config['inputs_sha256'].items():
        if digest((d/name).read_bytes()) != expected: raise ValueError('Unreviewed input change: '+name)
    for path, expected in config['frozen_v010_sha256'].items():
        if digest((root/path).read_bytes()) != expected: raise ValueError('Published v0.1.0 modified: '+path)
    records, sources = read(d/'records.json'), read(d/'sources.json')
    validate(records, sources)
    checked = sum(r['review']['status']=='primary_source_checked' for r in records)
    labeled = sum(bool(r['signals']) for r in records)
    meta = {**config, 'record_count': len(records), 'distinct_source_count': len(sources),
            'primary_checked_record_count': checked, 'legacy_record_count': len(records)-checked,
            'screened_record_count': labeled, 'unreviewed_record_count': len(records)-labeled,
            'signal_count': sum(len(r['signals']) for r in records),
            'evidence_cutoff': config['literature_search_through'],
            'evidence_cutoff_meaning': 'Targeted search horizon, not a universal primary-review date; see per-record dates.'}
    meta.pop('inputs_sha256'); meta.pop('frozen_v010_sha256')
    dataset = {'metadata': meta, 'records': records}
    release = root/'docs/dataset'/('v'+config['version'])
    files = {release/'dataset.json': dumps(dataset), release/'records.jsonl': ''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),
             release/'schema.json': dumps(schema()), release/'sources.json': dumps(sources),
             release/'screening.json': dumps(read(d/'screening.json')), release/'corrections.json': dumps(read(d/'corrections.json')),
             release/'search-log.json': dumps(read(d/'search-log.json')),
             release/'DATASET_CARD.md': (root/'DATASET_CARD.md').read_text(),
             release/'PROTOCOL.md': (root/'DATASET_PROTOCOL.md').read_text()}
    if config.get('license'):
        files[release/'LICENSE-DATA.md']=(root/'LICENSE-DATA.md').read_text()
    files[release/'primary-checked.records.jsonl']=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records if r['review']['status']=='primary_source_checked')
    flatrecords=[]; flatsignals=[]; joins=[]; source_rows=[]; components=[]; signal_benchmarks=[]; reviews=[]; controls=[]; queue=[]
    for r in records:
        flatrecords.append({**r, 'review_status': r['review']['status'], 'reviewed_on': r['review']['reviewed_on'],
                            'selection_protocol_missingness': r['missingness']['selection_protocol'],
                            'controlled_variables_missingness': r['missingness']['controlled_variables'],
                            'narrative': '\n\n'.join(s['label']+': '+s['text'] for s in r['sections'])})
        controls.extend({'record_id': r['id'], 'control': c} for c in r['controlled_variables'] or [])
        queue.append({'record_id':r['id'], 'key':r['key'], 'domain':r['domain'], 'current_review_status':r['review']['status'],
                      'next_action':'human_adjudication' if r['review']['status']=='primary_source_checked' else 'primary_source_review',
                      'source_url':r['sources'][0]['url'], 'source_locator':r['sources'][0]['locator'],
                      'reviewer_1':None,'reviewer_2':None,'adjudication':None,'reviewed_on':None})
        reviews.append({'record_id': r['id'], **{k:v for k,v in r['review'].items() if k!='primary_support'}})
        for i,s in enumerate(r['sources']):source_rows.append({'record_id':r['id'],'source_index':i,**s})
        for b in r['benchmarks']:joins.append({'record_id':r['id'],'benchmark_id':b['id'],'role':b['role']})
        for s in r['signals']:
            uid=r['id']+'::'+s['id'];p=s['primary_support']
            flatsignals.append({'signal_id':uid,'record_id':r['id'],'key':r['key'],**s,
                                'source_url':p['url'],'source_locator':p['locator'],'support_excerpt':p['excerpt'],
                                'source_sha256':p['artifact_sha256'],'checked_on':p['checked_on']})
            components.extend({'signal_id':uid,'component':c} for c in s['components'])
            signal_benchmarks.extend({'signal_id':uid,'benchmark_id':b} for b in s['benchmark_ids'])
    tables={
      'records.csv':(flatrecords,['id','key','domain','category_id','title','annotation_status','review_status','reviewed_on','weight_update_boundary','transfer_regime','selection_protocol','selection_protocol_missingness','controlled_variables_missingness','narrative']),
      'signals.csv':(flatsignals,['signal_id','record_id','key','outcome','retention','attribution','scope','summary','source_url','source_locator','support_excerpt','source_sha256','checked_on']),
      'papers.csv':(sources,['key','title','authors','kind','arxiv_id','doi']),
      'record_sources.csv':(source_rows,['record_id','source_index','name','url','locator','source_version','first_release_date','source_version_date','metadata_checked_on','metadata_basis']),
      'record_benchmarks.csv':(joins,['record_id','benchmark_id','role']),
      'record_controls.csv':(controls,['record_id','control']),
      'signal_components.csv':(components,['signal_id','component']),
      'signal_benchmarks.csv':(signal_benchmarks,['signal_id','benchmark_id']),
      'reviews.csv':(reviews,['record_id','status','reviewed_on','reviewer','human_review_status','scope']),
      'review-queue.csv':(queue,['record_id','key','domain','current_review_status','next_action','source_url','source_locator','reviewer_1','reviewer_2','adjudication','reviewed_on'])}
    for name,(rows,cols) in tables.items():files[release/name]=csv_text(rows,cols)
    for name,(rows,cols) in tables.items():
        if name in ['records.csv','signals.csv','papers.csv']:
            files[release/(name[:-4]+'.flat.jsonl')]=''.join(json.dumps({k:r.get(k) for k in cols},ensure_ascii=False)+'\n' for r in rows)
    quality={'records':len(records),'distinct_sources':len(sources),'primary_checked_records':checked,
             'legacy_records_without_new_primary_audit':len(records)-checked,'signal_records':labeled,
             'signals':len(flatsignals),'human_adjudicated_records':sum(r['review']['human_review_status']=='adjudicated' for r in records),
             'selection_protocol_populated':sum(bool(r['selection_protocol']) for r in records),
             'controlled_variables_populated':sum(bool(r['controlled_variables']) for r in records),
             'domains':dict(collections.Counter(r['domain'] for r in records)),
             'outcomes':dict(collections.Counter(s['outcome'] for s in flatsignals)),
             'screening_decisions':dict(collections.Counter(s['decision'] for s in read(d/'screening.json'))),
             'structural_validation':'passed','independent_reproduction':False,
             'limitations':'Counts report coverage, not an overall quality score or field-wide evidence census.'}
    files[release/'quality-report.json']=dumps(quality)
    checked_ids={r['id'] for r in records if r['review']['status']=='primary_source_checked'}
    columns=tables['records.csv'][1]
    files[release/'primary-checked.flat.jsonl']=''.join(json.dumps({k:r.get(k) for k in columns},ensure_ascii=False)+'\n' for r in flatrecords if r['id'] in checked_ids)
    files[release/'citation.bib']='@misc{harness_rsi_evidence_v020,\n  title = {Harness RSI Evidence Dataset},\n  author = {{Harness RSI project team}},\n  year = {2026},\n  version = {'+config['version']+'},\n  url = {https://huggingface.co/datasets/lucas1026/harness-rsi-evidence},\n  note = {Versioned source-traceable curation; AI-assisted review coverage disclosed in the dataset card}\n}\n'
    files[release/'checksums.json']=dumps({p.name:digest(text.encode()) for p,text in sorted(files.items())})
    pointer={'version':config['version'],'status':config['status'],'prepared_on':config['prepared_on'],'released_on':config['released_on'],
             'path':'dataset/v'+config['version']+'/dataset.json','sha256':digest(files[release/'dataset.json'].encode())}
    pointer_name='latest.json' if config['status']=='released' else 'candidate.json'
    files[root/'docs/dataset'/pointer_name]=dumps(pointer)
    return files
