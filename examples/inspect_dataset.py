"""Inspect scoped reported observations without treating them as independent trials."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outcome', choices=['improvement', 'regression', 'no_gain', 'mixed', 'not_assessed'])
    parser.add_argument('--path', type=Path, default=Path(__file__).resolve().parents[1] /
                        'docs/dataset/v0.1.0/dataset.json')
    arguments = parser.parse_args()
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
