import importlib.util
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

    def test_current_corpus_totals_and_generated_output(self):
        records=c.load_catalog()
        stats=c.statistics(records,c.read_json(c.ROOT/'data/history.json'))
        self.assertEqual(sum(stats['categories'].values()),len(records))
        self.assertEqual(stats['papers']+stats['resources'],len(records))
        self.assertEqual(sum(stats['monthly'].values()),stats['monthly_coverage'])
        for path,expected in c.outputs().items():
            self.assertEqual(path.read_text(),expected,str(path))


if __name__=='__main__':
    unittest.main()
