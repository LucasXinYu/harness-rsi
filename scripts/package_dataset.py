"""Build a reviewable Hugging Face upload bundle from validated versioned exports.

This prepares files only. It does not upload, grant a license, or advance latest.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='A new directory; existing packages are never overwritten.')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('dataset_v020', ROOT/'scripts/dataset_v020.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    expected = builder.outputs(ROOT)
    for path, content in expected.items():
        if not path.is_file() or path.read_bytes() != content.encode():
            raise SystemExit('Generated file stale: ' + str(path))
    config = json.loads((ROOT/'data/dataset_v020/release.json').read_text())
    if config.get('license', {}).get('id') != 'cc-by-4.0':
        raise SystemExit('This release packager requires the recorded scoped license authorization.')
    version = 'v' + config['version']
    args.output.mkdir(parents=True, exist_ok=False)
    upload = args.output/'hf-upload'
    upload.mkdir()
    shutil.copytree(ROOT/'docs/dataset'/version, upload/version)
    for archived in sorted((ROOT/'docs/dataset').glob('v*')):
        if archived.is_dir() and archived.name != version:
            shutil.copytree(archived, upload/archived.name)
    metadata = json.loads((ROOT/'docs/dataset'/version/'dataset.json').read_text())['metadata']
    shutil.copy2(ROOT/'DATASET_PROTOCOL.md', upload/'PROTOCOL.md')
    if config.get('license'):
        shutil.copy2(ROOT/'LICENSE-DATA.md', upload/'LICENSE-DATA.md')
    card = (ROOT/'DATASET_CARD.md').read_text()
    configs = [('primary_checked', 'primary-checked.flat.jsonl'),
               ('all_records', 'records.flat.jsonl'), ('signals', 'signals.flat.jsonl'),
               ('papers', 'papers.flat.jsonl')]
    yaml = ['---', 'license: cc-by-4.0', 'pretty_name: Harness RSI Evidence Dataset', 'language:', '- en',
            'size_categories:', '- n<1K', 'tags:', '- agents', '- harness-optimization',
            '- recursive-self-improvement', '- evidence-curation', 'configs:']
    for name, filename in configs:
        yaml += ['- config_name: ' + name]
        if name == 'primary_checked': yaml += ['  default: true']
        yaml += ['  data_files:', '  - split: data', '    path: ' + version + '/' + filename]
    yaml += ['---', '', '> CC BY 4.0 covers project-owned original annotations and compilation only. '
             'Third-party papers, support excerpts and code retain their rights; see [license scope](LICENSE-DATA.md). '
             f"Default preview: {metadata['primary_checked_record_count']} targeted AI-assisted primary checks, not human-adjudicated gold labels.", '',
             'Versioned files: [' + version + '](https://huggingface.co/datasets/lucas1026/harness-rsi-evidence/tree/main/' + version + '). The 85 inherited records are available '
             'in `all_records` with explicit review status.', '', '[Survey preprint](https://www.preprints.org/manuscript/202610.2293) · [Atlas](https://lucasxinyu.github.io/harness-rsi/) · [GitHub](https://github.com/LucasXinYu/harness-rsi)', '']
    (upload/'README.md').write_text('\n'.join(yaml) + card)
    (upload/'UPLOAD-NOTES.md').write_text(
        '# Publication checklist\n\n'
        '- Retain the maintainer-authorized scoped license and third-party exclusions.\n'
        '- Upload this folder to lucas1026/harness-rsi-evidence. Preserve existing history.\n'
        f"- Verify configurations: {metadata['primary_checked_record_count']} primary checks / {metadata['record_count']} records / {metadata['signal_count']} signals / {metadata['distinct_source_count']} papers.\n"
        '- Download the committed version and verify checksums; record the actual HF commit.\n'
        '- Do not infer publication from this package; record the actual upload and commit.\n')
    source = args.output/'rebuild-source'
    for relative in ['scripts/dataset_v020.py', 'scripts/validate_dataset.py',
                     'scripts/package_dataset.py', 'requirements-validation.txt',
                     'DATASET_CARD.md', 'DATASET_PROTOCOL.md', 'LICENSE-DATA.md']:
        target = source/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/relative, target)
    shutil.copytree(ROOT/'data/dataset_v020', source/'data/dataset_v020')
    # The builder verifies archived bytes before exporting the candidate.
    for relative in {**config['frozen_v010_sha256'], **config.get('frozen_v020_sha256', {})}:
        target = source/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/relative, target)
    (source/'REBUILD.md').write_text(
        '# Rebuild\n\nUse Python 3.9 or later. From this directory:\n\n'
        '```sh\npython3 -m pip install -r requirements-validation.txt\n'
        'python3 scripts/validate_dataset.py\n'
        'python3 -c "from pathlib import Path; from scripts.dataset_v020 import outputs; '
        '[(p.parent.mkdir(parents=True, exist_ok=True), p.write_text(t)) '
        'for p,t in outputs(Path.cwd()).items()]"\n```\n\n'
        'Source caches and third-party full papers are not distributed. Validation without '
        '`--source-cache` checks structure and provenance constraints, not primary-text anchor matches.\n')
    manifest = {str(p.relative_to(args.output)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(args.output.rglob('*')) if p.is_file()}
    (args.output/'PACKAGE-CHECKSUMS.json').write_text(json.dumps(manifest, indent=2)+'\n')
    archive = Path(str(args.output) + '.zip')
    if archive.exists(): raise SystemExit('Archive exists: ' + str(archive))
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as out:
        for path in sorted(args.output.rglob('*')):
            if not path.is_file(): continue
            info = zipfile.ZipInfo(str(path.relative_to(args.output)), tuple(map(int, config['prepared_on'].split('-'))) + (0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            out.writestr(info, path.read_bytes())
    print(json.dumps({'directory': str(args.output.resolve()), 'archive': str(archive.resolve()),
                      'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                      'published': False}, indent=2))


if __name__ == '__main__':
    main()
