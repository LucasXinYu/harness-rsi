import copy
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('dataset_builder', ROOT / 'scripts/dataset.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads((ROOT / 'docs/evidence.json').read_text())
        self.annotations = json.loads((ROOT / 'data/dataset_annotations.json').read_text())

    def test_exports_preserve_frozen_record_units_and_missingness(self):
        files = builder.dataset_outputs(ROOT)
        release = ROOT / 'docs/dataset/v0.1.0'
        dataset = json.loads(files[release / 'dataset.json'])
        self.assertEqual(dataset['metadata']['record_count'], 95)
        self.assertEqual(dataset['metadata']['screened_record_count'], 4)
        self.assertEqual(dataset['metadata']['signal_count'], 6)
        originals = {record['id']: record for record in self.evidence['records']}
        for record in dataset['records']:
            for field, value in originals[record['id']].items():
                self.assertEqual(record[field], value)
            self.assertIsNone(record['selection_protocol'])
            self.assertIsNone(record['controlled_variables'])
            if record['annotation_status'] == 'not_reviewed':
                self.assertEqual(record['signals'], [])
        jsonl = [json.loads(line) for line in files[release / 'records.jsonl'].splitlines()]
        self.assertEqual(jsonl, dataset['records'])
        rows = list(csv.DictReader(io.StringIO(files[release / 'records.csv'])))
        self.assertEqual(len(rows), 95)
        for row, record in zip(rows, dataset['records']):
            self.assertEqual(json.loads(row['signals']), record['signals'])
            self.assertEqual(json.loads(row['sections']), record['sections'])
            self.assertIsNone(json.loads(row['selection_protocol']))

    def test_manifest_and_release_pointer_match_payloads(self):
        files = builder.dataset_outputs(ROOT)
        release = ROOT / 'docs/dataset/v0.1.0'
        manifest = json.loads(files[release / 'checksums.json'])
        for name, expected in manifest.items():
            self.assertEqual(hashlib.sha256(files[release / name].encode()).hexdigest(), expected)
        pointer = json.loads(files[ROOT / 'docs/dataset/latest.json'])
        self.assertEqual(pointer['sha256'], manifest['dataset.json'])
        self.assertNotIn('CC BY', json.loads(files[release / 'dataset.json'])['metadata']['license_status'])

    def test_annotations_reject_fabricated_quotes_and_cross_setting_labels(self):
        bad = copy.deepcopy(self.annotations)
        signal = next(iter(bad.values()))['signals'][0]
        signal['evidence_quote'] = 'Invented improvement claim'
        with self.assertRaisesRegex(ValueError, 'excerpt'):
            builder.validate_annotations(self.evidence, bad)
        bad = copy.deepcopy(self.annotations)
        next(iter(bad.values()))['signals'][0]['benchmark_ids'] = ['unrelated-benchmark']
        with self.assertRaisesRegex(ValueError, 'benchmark'):
            builder.validate_annotations(self.evidence, bad)
        bad = copy.deepcopy(self.annotations)
        next(iter(bad.values()))['signals'][0]['outcome'] = 'always works'
        with self.assertRaisesRegex(ValueError, 'outcome'):
            builder.validate_annotations(self.evidence, bad)

    def test_usage_is_not_automatically_a_null_performance_effect(self):
        signal = self.annotations['browser-mediated-interaction--harnessx2026']['signals'][0]
        self.assertEqual(signal['outcome'], 'not_assessed')
        self.assertEqual(signal['attribution'], 'usage_observation')

    def test_membership_snapshots_do_not_predate_first_collection(self):
        annotations = json.loads((ROOT / 'data/annotations.json').read_text())
        history = json.loads((ROOT / 'data/history.json').read_text())
        for snapshot in history:
            for kind in ('paper', 'resource'):
                for key in snapshot[kind + '_ids']:
                    if key in annotations:
                        self.assertLessEqual(annotations[key]['added_on'], snapshot['date'])


if __name__ == '__main__':
    unittest.main()
