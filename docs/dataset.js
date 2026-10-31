import {selectSignals, recordLink} from './dataset-model.mjs';

const labels = {improvement: 'Reported improvement', regression: 'Reported regression',
  no_gain: 'No reported gain', mixed: 'Mixed trade-off', not_assessed: 'Effect not assessed'};
const element = (tag, className, text) => {
  const item = document.createElement(tag);
  item.className = className;
  if (text !== undefined) item.textContent = text;
  return item;
};

async function initDataset() {
  const pointerResponse = await fetch('dataset/latest.json');
  if (!pointerResponse.ok) throw new Error('Dataset release pointer unavailable');
  const pointer = await pointerResponse.json();
  const response = await fetch(pointer.path);
  if (!response.ok) throw new Error('Dataset unavailable');
  const dataset = await response.json();
  const metadata = dataset.metadata;
  const root = pointer.path.replace('dataset.json', '');
  document.getElementById('dataset-version').textContent = `v${metadata.version} · released ${metadata.released_on}`;
  document.getElementById('dataset-coverage').textContent =
    `${metadata.record_count} category–source records · ${metadata.distinct_source_count} distinct sources · targeted search through ${metadata.literature_search_through ?? metadata.evidence_cutoff}`;
  document.getElementById('dataset-screening').textContent =
    `${metadata.screened_record_count}/${metadata.record_count} records have structured signals · ${metadata.signal_count} scoped observations · ${metadata.primary_checked_record_count ?? 0} targeted primary checks · ${metadata.legacy_record_count ?? metadata.unreviewed_record_count} inherited records`;
  for (const link of document.querySelectorAll('[data-dataset-file]')) {
    link.href = root + link.dataset.datasetFile;
  }
  const filter = document.getElementById('dataset-outcome');
  function render() {
    const signals = selectSignals(dataset, filter.value);
    const cards = signals.map(({record, signal}) => {
      const card = element('article', 'dataset-signal');
      const badge = element('span', `dataset-badge outcome-${signal.outcome}`, labels[signal.outcome]);
      card.append(badge, element('h3', '', record.title), element('p', '', signal.summary));
      const scope = element('p', 'dataset-scope', `Scope: ${signal.scope}`);
      const attribution = element('p', 'dataset-detail',
        `${signal.attribution.replaceAll('_', ' ')} · retention: ${signal.retention.replaceAll('_', ' ')}`);
      const proof = element('details', 'dataset-proof');
      proof.append(element('summary', '', 'Trace this annotation'));
      proof.append(element('blockquote', '', signal.evidence_quote));
      proof.append(element('p', 'dataset-detail', 'Excerpt of our curated record. Primary-text anchors and review scope are available in the linked record and versioned data.'));
      const primary = element('a', '', `${signal.primary_source.name} ↗`);
      primary.href = signal.primary_source.url;
      proof.append(primary, element('p', 'dataset-detail', signal.primary_source.locator));
      const link = element('a', 'dataset-record-link', 'Read original record & limits ↗');
      link.href = recordLink(record);
      card.append(scope, attribution, proof, link);
      return card;
    });
    const container = document.getElementById('dataset-signals');
    container.replaceChildren(...cards);
    if (!cards.length) container.append(element('p', '', 'No screened signals match. This is not evidence that the outcome is absent.'));
    document.getElementById('dataset-filter-status').textContent = `${signals.length} scoped observations shown; not independent experiments.`;
  }
  filter.addEventListener('change', render);
  render();
}

initDataset().catch(error => {
  console.error(error);
  document.getElementById('dataset-error').hidden = false;
});
