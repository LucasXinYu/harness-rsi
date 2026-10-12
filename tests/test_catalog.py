import importlib.util
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('catalog', Path(__file__).resolve().parents[1]/'scripts/catalog.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class CatalogTests(unittest.TestCase):
    def test_nested_bib_fields_and_duplicates(self):
        source = '@misc{x,\n title = {{A {Nested} Title}},\n url = {https://example.org/x},\n year = {2026}\n}\n'
        self.assertEqual(c.plain(c.bib_entries(source)[0]['title']), 'A Nested Title')
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            c.bib_entries(source+source)

    def test_revision_does_not_replace_first_submission(self):
        entry = {'eprint':'2601.12345','url':'https://arxiv.org/abs/2601.12345v3'}
        result = c.release_date(entry,'',{'dates':['[Submitted on 3 Jan 2026 (v1), last revised 20 Sep 2026 (v3)]']})
        self.assertEqual(result['value'],'2026-01-03')
        self.assertEqual(result['precision'],'day')

    def test_partial_dates_are_not_fabricated(self):
        entry = {'eprint':'2601.12345','url':'https://arxiv.org/abs/2601.12345'}
        self.assertEqual(c.release_date(entry,'',{})['value'],'2026-01')
        self.assertEqual(c.release_date({'year':'2026','url':'https://example.org'},'',{})['value'],'2026')
        self.assertIsNone(c.release_date({'url':'https://example.org'},'',{})['value'])

    def test_monthly_counts_exclude_resources_and_inexact_dates(self):
        records = [
            {'kind':'paper','category':c.FOCUS,'release':{'value':'2026-01-05','precision':'day'}},
            {'kind':'paper','category':'Other','release':{'value':'2026-01','precision':'month'}},
            {'kind':'paper','category':'Other','release':{'value':'2026','precision':'year'}},
            {'kind':'paper','category':'Other','release':{'value':None,'precision':'unknown'}},
            {'kind':'resource','category':'Resources','release':{'value':'2026-01-01','precision':'day'}}]
        stats = c.statistics(records,[])
        self.assertEqual(stats['papers'],4)
        self.assertEqual(stats['resources'],1)
        self.assertEqual(stats['monthly'],{'2026-01':2})
        self.assertEqual(stats['focus_monthly'],{'2026-01':1})

    def test_publication_series_spans_years_and_stops_at_cutoff(self):
        stats = {'monthly': {'2025-12': 2, '2026-02': 3}}
        rows = c.publication_series(stats, '2026-03-01')
        january = next(row for row in rows if row['month'] == '2026-01')
        self.assertEqual(january, {'month': '2026-01', 'papers': 0, 'cumulative': 2, 'partial': False})
        self.assertEqual(rows[-1], {'month': '2026-03', 'papers': 0, 'cumulative': 5, 'partial': True})
        self.assertFalse(any(row['month'] > '2026-03' for row in rows))
        self.assertEqual(sum(row['papers'] for row in rows), rows[-1]['cumulative'])

    def test_completed_month_and_out_of_horizon_data(self):
        stats = {'monthly': {'2024-02': 1}}
        self.assertFalse(c.publication_series(stats, '2024-02-29')[-1]['partial'])
        self.assertTrue(c.publication_series(stats, '2024-02-28')[-1]['partial'])
        with self.assertRaisesRegex(ValueError, 'cutoff'):
            c.publication_series(stats, '2024-01-31')

    def test_import_history_preserves_baseline_and_counts_removals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source';source.mkdir();(root/'data').mkdir()
            c.write_json(root/'data/config.json',{'search_cutoff':'2026-10-01'})
            def source_files(keys):
                (source/'literature.bib').write_text('\n'.join('@misc{'+k+',\n title = {Paper '+k+'},\n year = {2026},\n url = {https://example.org/'+k+'}\n}' for k in keys))
                (source/'literature_map.tex').write_text('\\section{Harness Optimization and Search Workflows}\n'+''.join('\\subsection*{'+str(i)+'. Paper '+k+'}\n\\textbf{Reference:} \\citep{'+k+'}.\\par\nA method description.\n\n' for i,k in enumerate(keys))+'\\bibliographystyle{plain}\n')
            with patch.object(c,'ROOT',root):
                source_files(['a']);c.import_sources(source,'2026-10-03')
                source_files(['a','b']);c.import_sources(source,'2026-10-04')
                self.assertEqual(c.read_json(root/'data/annotations.json')['a']['added_on'],'2026-10-03')
                c.import_sources(source,'2026-10-05')  # No new snapshot for unchanged membership.
                self.assertEqual(len(c.read_json(root/'data/history.json')),2)
                source_files(['b']);c.import_sources(source,'2026-10-06')
                self.assertEqual(c.read_json(root/'data/history.json')[-1]['paper_ids'],['b'])
                source_files(['a','b']);c.import_sources(source,'2026-10-07')
                self.assertEqual(c.read_json(root/'data/annotations.json')['a']['added_on'],'2026-10-03')
                with self.assertRaisesRegex(ValueError,'backdated'):
                    c.import_sources(source,'2026-10-02')
                # A manuscript-only alias must not inflate the Map-defined corpus.
                with (source/'literature.bib').open('a') as out:
                    out.write('@misc{extra,\n title = {Supporting reference},\n year = {2026},\n url = {https://example.org/extra}\n}\n')
                c.import_sources(source,'2026-10-08')
                self.assertEqual(set(c.read_json(root/'data/annotations.json')), {'a','b'})
                self.assertEqual(len(c.read_json(root/'data/history.json')), 4)

    def test_findings_require_resolvable_evidence_and_counts(self):
        project=c.read_json(c.ROOT/'docs/project.json')
        records=c.load_catalog()
        c.validate_project(project,records)
        bad=copy.deepcopy(project)
        bad['domains'][0]['records']+=1
        with self.assertRaisesRegex(ValueError,'totals'):
            c.validate_project(bad,records)
        bad=copy.deepcopy(project)
        bad['insights'][0]['cells'][0]['finding']='nonexistent'
        with self.assertRaisesRegex(ValueError,'missing evidence'):
            c.validate_project(bad,records)
        bad=copy.deepcopy(project)
        bad['domains'][0]['findings'][0]['sources'][0]['url']='https://example.org/wrong-paper'
        with self.assertRaisesRegex(ValueError,'differs'):
            c.validate_project(bad,records)
        bad=copy.deepcopy(project)
        del bad['insights'][0]['comparison']['axes']['coding']
        with self.assertRaisesRegex(ValueError,'same domains'):
            c.validate_project(bad,records)
        bad=copy.deepcopy(project)
        bad['insights'][0]['cells'].append(bad['insights'][0]['cells'][0])
        with self.assertRaisesRegex(ValueError,'exactly one'):
            c.validate_project(bad,records)

    def test_current_corpus_totals_and_generated_output(self):
        records=c.load_catalog()
        stats=c.statistics(records,c.read_json(c.ROOT/'data/history.json'))
        self.assertEqual(sum(stats['categories'].values()),len(records))
        self.assertEqual(stats['papers']+stats['resources'],len(records))
        self.assertEqual(sum(stats['monthly'].values()),stats['monthly_coverage'])
        for path,expected in c.outputs().items():
            self.assertEqual(path.read_text(),expected,str(path))

    def test_benchmark_evidence_scope_and_export_consistency(self):
        data=c.read_json(c.ROOT/'docs/evidence.json')
        project=c.read_json(c.ROOT/'docs/project.json')
        records=c.load_catalog()
        c.validate_evidence(data,project,records)
        annotations=c.read_json(c.ROOT/'data/evidence_annotations.json')
        self.assertEqual(data['patterns'],annotations['patterns'])
        self.assertEqual(data['benchmarks'],annotations['benchmarks'])
        self.assertEqual({r['id'] for r in data['records']},set(annotations['records']))
        for record in data['records']:
            for field,value in annotations['records'][record['id']].items():
                self.assertEqual(record[field],value)
        bad=copy.deepcopy(data)
        bad['patterns'][0]['cases'][0]['benchmarks']=['imaginary-benchmark']
        with self.assertRaisesRegex(ValueError,'unsupported benchmark'):
            c.validate_evidence(bad,project,records)
        bad=copy.deepcopy(data)
        bad['records'][0]['sources'][0]['locator']=''
        with self.assertRaisesRegex(ValueError,'locator'):
            c.validate_evidence(bad,project,records)
        bad=copy.deepcopy(data)
        bad['records'][0]['key']='invented-paper'
        with self.assertRaises(ValueError):
            c.validate_evidence(bad,project,records)

    def test_evidence_records_keep_important_attribution_limits(self):
        data=c.read_json(c.ROOT/'docs/evidence.json')
        records={r['id']:r for r in data['records']}
        modular=records['terminal-based-engineering-tasks--modularrsi2026']
        self.assertEqual(next(b['role'] for b in modular['benchmarks'] if b['id']=='terminal-bench-2-0'),'transfer')
        self.assertIn('not Terminal-Bench test cases',modular['sections'][-1]['text'])
        rho=records['terminal-based-engineering-tasks--rho2026']
        self.assertEqual(rho['benchmarks'][0]['id'],'terminal-bench-2-x-minor-unspecified')
        self.assertIn('do not run those scripts',rho['sections'][-1]['text'])
        aide=records['machine-learning-engineering--aide2_2026']
        self.assertEqual(aide['benchmarks'][0]['role'],'transfer')
        self.assertIn('never enters evolutionary selection',aide['sections'][-1]['text'])

    def test_evidence_release_is_dated_and_matches_the_snapshot(self):
        data=c.read_json(c.ROOT/'docs/evidence.json')
        updates=c.read_json(c.ROOT/'docs/updates.json')
        c.validate_updates(updates,data)
        # A newer UI release must not force a fabricated evidence/export date.
        newer=copy.deepcopy(updates)
        tomorrow=(c.dt.date.fromisoformat(updates['releases'][0]['date'])+c.dt.timedelta(days=1)).isoformat()
        newer['releases'].insert(0,{'id':'ui-only','date':tomorrow,'kind':'website','changes':['Presentation only.'],'records':len(data['records'])})
        c.validate_updates(newer,data)
        wrong=copy.deepcopy(updates)
        next(r for r in wrong['releases'] if r['kind']=='evidence')['records']+=1
        with self.assertRaisesRegex(ValueError,'exported snapshot'):
            c.validate_updates(wrong,data)
        wrong=copy.deepcopy(updates)
        wrong['releases'].reverse()
        with self.assertRaisesRegex(ValueError,'newest first'):
            c.validate_updates(wrong,data)


if __name__=='__main__':
    unittest.main()
