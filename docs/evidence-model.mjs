// Shared by the browser and data checks. Filtering never duplicates a source record.
export function selectRecords(data, domain, category = 'all', benchmark = 'all') {
  return data.records.filter(record => record.domain === domain &&
    (category === 'all' || record.category_id === category) &&
    (benchmark === 'all' || record.benchmarks.some(item => item.id === benchmark)));
}

export function selectPatterns(data, records, benchmark = 'all') {
  const ids = new Set(records.map(record => record.id));
  return data.patterns.map(pattern => ({...pattern, cases: pattern.cases.filter(item =>
    ids.has(item.record) && (benchmark === 'all' || item.benchmarks === undefined || item.benchmarks.includes(benchmark))
  )})).filter(pattern => pattern.cases.length > 0);
}

export function sourceCount(records) {
  return new Set(records.map(record => record.key)).size;
}
