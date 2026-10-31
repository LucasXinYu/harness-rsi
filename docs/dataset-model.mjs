export function selectSignals(dataset, outcome = 'all') {
  return dataset.records.flatMap(record => record.signals
    .filter(signal => outcome === 'all' || signal.outcome === outcome)
    .map(signal => ({record, signal})));
}

export function recordLink(record) {
  if (record.provenance) return `dataset/#${encodeURIComponent(record.id)}`;
  const parameters = new URLSearchParams({domain: record.domain, category: record.category_id, setting: 'all'});
  return `#benchmarks?${parameters}`;
}
