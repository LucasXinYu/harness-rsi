import copy
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('dataset_v020',ROOT/'scripts/dataset_v020.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class ReviewedDatasetTests(unittest.TestCase):
    def setUp(self):
        self.records=json.loads((ROOT/'data/dataset_v020/records.json').read_text())
        self.sources=json.loads((ROOT/'data/dataset_v020/sources.json').read_text())

    def test_versioned_exports_and_relational_units(self):
        files=builder.outputs(ROOT)
        config=json.loads((ROOT/'data/dataset_v020/release.json').read_text())
        release=ROOT/'docs/dataset'/('v'+config['version'])
        payload=json.loads(files[release/'dataset.json'])
        self.assertEqual(payload['records'],self.records)
        self.assertEqual(len(payload['records']),132)
        self.assertEqual(payload['metadata']['primary_checked_record_count'],47)
        self.assertEqual(payload['metadata']['signal_count'],32)
        records=list(csv.DictReader(io.StringIO(files[release/'records.csv'])))
        signals=list(csv.DictReader(io.StringIO(files[release/'signals.csv'])))
        self.assertEqual(len(records),132);self.assertEqual(len(signals),32)
        self.assertTrue({s['record_id'] for s in signals}<={r['id'] for r in records})
        self.assertEqual(len({s['signal_id'] for s in signals}),len(signals))
        checked=[json.loads(line) for line in files[release/'primary-checked.records.jsonl'].splitlines()]
        self.assertEqual(len(checked),47)
        self.assertTrue(all(r['review']['status']=='primary_source_checked' for r in checked))
        queue=list(csv.DictReader(io.StringIO(files[release/'review-queue.csv'])))
        self.assertEqual(sum(r['next_action']=='primary_source_review' for r in queue),85)
        manifest=json.loads(files[release/'checksums.json'])
        for name,h in manifest.items():self.assertEqual(hashlib.sha256(files[release/name].encode()).hexdigest(),h)
        self.assertFalse(any('/v0.1.0/' in str(p) or '/v0.2.0/' in str(p) for p in files))

    def test_cross_benchmark_attribution_and_missingness_are_enforced(self):
        bad=copy.deepcopy(self.records);r=next(r for r in bad if r['signals'])
        r['signals'][0]['benchmark_ids']=['invented-setting']
        with self.assertRaisesRegex(ValueError,'benchmark'):builder.validate(bad,self.sources)
        bad=copy.deepcopy(self.records);r=next(r for r in bad if r['signals'])
        r['signals'][0]['evidence_quote']='Invented claim'
        with self.assertRaisesRegex(ValueError,'excerpt'):builder.validate(bad,self.sources)
        bad=copy.deepcopy(self.records);r=next(r for r in bad if r['review']['status']=='legacy_curated')
        r['review']['reviewed_on']='2026-10-31'
        with self.assertRaisesRegex(ValueError,'Inherited'):builder.validate(bad,self.sources)
        bad=copy.deepcopy(self.records);r=next(r for r in bad if r['signals'])
        r['annotation_status']='not_reviewed'
        with self.assertRaisesRegex(ValueError,'Annotation status'):builder.validate(bad,self.sources)
        bad=copy.deepcopy(self.sources);bad[1]['arxiv_id']=bad[0]['arxiv_id']
        with self.assertRaisesRegex(ValueError,'Duplicate canonical'):builder.validate(self.records,bad)

    def test_scientific_correction_does_not_rewrite_history(self):
        rid='browser-mediated-interaction--harnessx2026'
        old=json.loads((ROOT/'docs/dataset/v0.1.0/dataset.json').read_text())
        oldsignal=next(r for r in old['records'] if r['id']==rid)['signals'][0]
        new=next(r for r in self.records if r['id']==rid)['signals'][0]
        self.assertEqual(oldsignal['attribution'],'usage_observation')
        self.assertEqual(new['attribution'],'reported_edit_outcome')
        self.assertEqual(new['outcome'],'no_gain')
        self.assertNotEqual(oldsignal['id'],new['id'])
        self.assertIn('not a call-frequency metric',new['scope'])

    def test_training_and_transfer_boundaries_remain_visible(self):
        bykey={r['key']:r for r in self.records}
        self.assertEqual(bykey['beam2026']['weight_update_boundary'],'auxiliary_weights_trained')
        self.assertEqual(bykey['beam2026']['transfer_regime'],'target_adaptation')
        self.assertEqual(bykey['herd2026']['weight_update_boundary'],'executor_weights_trained')
        self.assertEqual(bykey['oo_harness2026']['transfer_regime'],'cross_domain_fallback')
        self.assertEqual(sum(r['annotation_status']=='record_reviewed_no_signal' for r in self.records),17)

if __name__=='__main__':unittest.main()
