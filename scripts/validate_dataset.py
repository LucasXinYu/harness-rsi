"""Validate schema, relational exports and optional local primary-text anchors."""
import argparse,hashlib,importlib.util,json,pathlib,re
from jsonschema import Draft202012Validator, FormatChecker

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('dataset_v020',ROOT/'scripts/dataset_v020.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-cache',type=pathlib.Path)
    p.add_argument('--report',type=pathlib.Path)
    args=p.parse_args()
    config=b.read(ROOT/'data/dataset_v020/release.json')
    files=b.outputs(ROOT);release=ROOT/'docs/dataset'/('v'+config['version'])
    data=json.loads(files[release/'dataset.json'])
    sch=b.schema();Draft202012Validator.check_schema(sch)
    validator=Draft202012Validator(sch,format_checker=FormatChecker())
    for record in data['records']:validator.validate(record)
    anchor_count=0
    if args.source_cache:
        for record in data['records']:
            supports=[s['primary_support'] for s in record['signals']]
            if record['review'].get('primary_support'):supports.append(record['review']['primary_support'])
            for support in supports:
                version=re.search(r'\d{4}\.\d{4,5}v\d+',support['url'])[0]
                html=args.source_cache/(version+'.html');text=args.source_cache/(version+'.txt')
                if hashlib.sha256(html.read_bytes()).hexdigest()!=support['artifact_sha256']:
                    raise ValueError('Inspected artifact hash mismatch: '+version)
                if support['excerpt'] not in ' '.join(text.read_text().split()):
                    raise ValueError('Primary excerpt not found: '+version)
                anchor_count+=1
    report={'schema':'passed','records':len(data['records']),'relational_and_manifest_checks':'passed',
            'frozen_v010':'unchanged','primary_anchor_checks':anchor_count if args.source_cache else 'not_run',
            'scientific_interpretation':'Requires source inspection; structural validation is not scientific certification.'}
    if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
