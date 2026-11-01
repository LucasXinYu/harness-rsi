"""Inspect scoped reported observations without treating them as independent trials."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outcome', choices=['improvement', 'regression', 'no_gain', 'mixed', 'not_assessed'])
    parser.add_argument('--path', type=Path, help='Pinned dataset JSON; defaults to the current release pointer.')
    arguments = parser.parse_args()
    if arguments.path is None:
        docs = Path(__file__).resolve().parents[1] / 'docs'
        pointer = json.loads((docs / 'dataset/latest.json').read_text())
        arguments.path = docs / pointer['path']
    dataset = json.loads(arguments.path.read_text())
    metadata = dataset['metadata']
    print(f"{metadata['name']} v{metadata['version']}: {metadata['screened_record_count']}/"
          f"{metadata['record_count']} records screened for structured signals")
    for record in dataset['records']:
        for signal in record['signals']:
            if arguments.outcome and signal['outcome'] != arguments.outcome:
                continue
            print(f"\n{record['id']} / {signal['id']}: {signal['outcome']}")
            print(signal['summary'])
            print('Scope:', signal['scope'])
            print('Attribution:', signal['attribution'], '| retention:', signal['retention'])
            print('Source:', signal['primary_source']['url'], signal['primary_source']['locator'])
    print('\nSignals are not independent trials. Unreviewed records do not imply no failures.')


if __name__ == '__main__':
    main()
