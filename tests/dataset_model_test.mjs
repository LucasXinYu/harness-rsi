import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {selectSignals, recordLink} from '../docs/dataset-model.mjs';

const dataset = JSON.parse(readFileSync(new URL('../docs/dataset/v0.1.0/dataset.json', import.meta.url)));
assert.equal(selectSignals(dataset).length, 6);
assert.equal(selectSignals(dataset, 'regression').length, 1);
assert.equal(selectSignals(dataset, 'no_gain').length, 1);
assert.equal(selectSignals(dataset, 'mixed').length, 1);
assert.equal(selectSignals(dataset, 'improvement').length, 2);
assert.equal(selectSignals(dataset, 'not_assessed').length, 1);
assert.equal(dataset.records.filter(record => record.annotation_status === 'not_reviewed').length, 91);
for (const {record, signal} of selectSignals(dataset)) {
  assert(recordLink(record).includes('setting=all'));
  assert(signal.primary_source.url.startsWith('https://'));
  assert(signal.primary_source.locator.length > 0);
  assert(signal.benchmark_ids.every(id => record.benchmarks.some(benchmark => benchmark.id === id)));
}
assert.equal(selectSignals(dataset, 'regression')[0].signal.benchmark_ids.length, 0);
const current = JSON.parse(readFileSync(new URL('../docs/dataset/v0.2.0/dataset.json', import.meta.url)));
assert.equal(selectSignals(current).length, 24);
for (const {record} of selectSignals(current)) assert.equal(recordLink(record), `dataset/#${encodeURIComponent(record.id)}`);
console.log('Validated dataset filtering, partial coverage, and signal-scope boundaries.');
