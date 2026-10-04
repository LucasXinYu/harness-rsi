'use strict';
const byId = id => document.getElementById(id);
let domains = [];
let activeDomain = '';

function selectDomain(id, focus = false) {
  const domain = domains.find(item => item.id === id);
  if (!domain) return;
  activeDomain = id;
  document.querySelectorAll('[role="tab"]').forEach(tab => {
    const selected = tab.dataset.domain === id;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (selected && focus) tab.focus();
  });
  byId('domain-title').textContent = domain.name;
  byId('domain-panel').setAttribute('aria-labelledby', `tab-${id}`);
  byId('domain-status').textContent = `${domain.name}: findings and evidence will be added here.`;
}

function renderDomains() {
  const container = byId('domain-tabs');
  container.replaceChildren();
  domains.forEach((domain, index) => {
    const tab = document.createElement('button');
    tab.type = 'button';
    tab.id = `tab-${domain.id}`;
    tab.className = 'domain-tab';
    tab.dataset.domain = domain.id;
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', 'domain-panel');
    const number = document.createElement('span');
    number.className = 'tab-index';
    number.textContent = String(index + 1).padStart(2, '0');
    const label = document.createElement('span');
    label.textContent = domain.name;
    const arrow = document.createElement('span');
    arrow.className = 'tab-arrow';
    arrow.setAttribute('aria-hidden', 'true');
    arrow.textContent = '→';
    tab.append(number, label, arrow);
    tab.addEventListener('click', () => selectDomain(domain.id));
    tab.addEventListener('keydown', event => {
      const current = domains.findIndex(item => item.id === activeDomain);
      let next;
      if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = (current + 1) % domains.length;
      else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = (current - 1 + domains.length) % domains.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = domains.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        selectDomain(domains[next].id, true);
      }
    });
    container.append(tab);
  });
  selectDomain(domains[0].id);
}

function setFutureLink(id, url, label) {
  if (!url) return;
  const parsed = new URL(url);
  if (parsed.protocol !== 'https:') throw new Error('Project links must use HTTPS.');
  const link = byId(id);
  link.href = parsed.href;
  link.removeAttribute('aria-disabled');
  link.classList.remove('unavailable', 'muted');
  link.textContent = `${label} ↗`;
}

async function init() {
  try {
    const response = await fetch('project.json');
    if (!response.ok) throw new Error('Project configuration unavailable.');
    const project = await response.json();
    domains = project.domains;
    if (!Array.isArray(domains) || !domains.length) throw new Error('No domains configured.');
    renderDomains();
    setFutureLink('paper-action', project.arxiv_url, 'arXiv paper');
    setFutureLink('paper-resource', project.arxiv_url, 'Read the survey');
    setFutureLink('site-resource', project.website_url, 'Visit the research website');
    const narrow = window.matchMedia('(max-width: 760px)');
    const orientation = () => byId('domain-tabs').setAttribute('aria-orientation', narrow.matches ? 'horizontal' : 'vertical');
    orientation();
    narrow.addEventListener('change', orientation);
  } catch (error) {
    byId('load-error').hidden = false;
    console.error(error.message);
  }
}
init();

let collectionStats;
let chartView = 'monthly';
const monthName = key => new Date(`${key}-01T12:00:00Z`).toLocaleString('en-US', { month: 'short', timeZone: 'UTC' });
const svgElement = (tag, attributes, text) => {
  const element = document.createElementNS('http://www.w3.org/2000/svg', tag);
  Object.entries(attributes || {}).forEach(([key, value]) => element.setAttribute(key, value));
  if (text !== undefined) element.textContent = text;
  return element;
};

function renderPublicationChart() {
  if (!collectionStats) return;
  const year = byId('publication-year').value;
  const rows = collectionStats.timeline.filter(row => row.month.startsWith(year));
  const cumulative = chartView === 'cumulative';
  const countKey = cumulative ? 'cumulative' : 'papers';
  const panel = byId('publication-chart');
  const width = Math.max(260, panel.clientWidth);
  const height = 260, left = 34, right = 15, top = 31, bottom = 33;
  const plotHeight = height - top - bottom;
  const step = (width - left - right) / rows.length;
  const largest = Math.max(...rows.map(row => row[countKey]), 1);
  const tickSize = largest <= 8 ? 1 : largest <= 40 ? 5 : Math.ceil(largest / 40) * 10;
  const maximum = Math.ceil(largest / (tickSize * 4)) * tickSize * 4;
  const svg = svgElement('svg', { viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-labelledby': 'plot-title plot-description' });
  const heading = cumulative ? 'Cumulative papers by publication month' : 'Papers by publication month';
  svg.append(svgElement('title', { id: 'plot-title' }, `${heading}, ${year}`));
  svg.append(svgElement('desc', { id: 'plot-description' }, rows.map(row => `${row.month}: ${row[countKey]}${row.partial ? ', partial month' : ''}`).join('; ')));
  const group = svgElement('g', { 'font-family': 'Arial, sans-serif', 'font-size': 10, fill: '#6a796e' });
  for (let i = 0; i <= 4; i++) {
    const y = top + plotHeight * (1 - i / 4);
    group.append(svgElement('path', { d: `M${left} ${y}H${width-right}`, stroke: '#e1e6dc', fill: 'none' }));
    group.append(svgElement('text', { x: left - 10, y: y + 3, 'text-anchor': 'end' }, maximum * i / 4));
  }
  const points = rows.map((row, i) => ({ x: left + step * (i + .5), y: top + plotHeight * (1 - row[countKey] / maximum), row }));
  if (cumulative) {
    const path = points.map(point => `${point.x},${point.y}`).join(' ');
    group.append(svgElement('polygon', { points: `${points[0].x},${top+plotHeight} ${path} ${points.at(-1).x},${top+plotHeight}`, fill: '#eaf0e4' }));
    group.append(svgElement('polyline', { points: path, fill: 'none', stroke: '#2c614b', 'stroke-width': 2 }));
  }
  points.forEach(({ x, y, row }) => {
    const color = row.partial ? '#b27548' : '#2c614b';
    const mark = cumulative
      ? svgElement('circle', { cx: x, cy: y, r: 3.5, fill: color })
      : svgElement('rect', { x: x - step * .26, y, width: step * .52, height: top + plotHeight - y, rx: 2, fill: color });
    mark.append(svgElement('title', {}, `${row.month}: ${row[countKey]} papers${row.partial ? ' (partial month)' : ''}`));
    group.append(mark);
    group.append(svgElement('text', { x, y: y - 10, 'text-anchor': 'middle', fill: color }, row[countKey]));
    group.append(svgElement('text', { x, y: height - 10, 'text-anchor': 'middle', 'font-size': width < 400 ? 9 : 10 }, monthName(row.month) + (row.partial ? '*' : '')));
  });
  svg.append(group);
  panel.replaceChildren(svg);
  byId('chart-heading').textContent = heading;
  byId('chart-description').textContent = cumulative ? 'Known release months · includes papers from earlier years' : 'Included literature · monthly counts';
  byId('monthly-view').setAttribute('aria-pressed', String(!cumulative));
  byId('cumulative-view').setAttribute('aria-pressed', String(cumulative));
  byId('partial-note').textContent = rows.some(row => row.partial) ? `* Partial month · through ${collectionStats.search_cutoff}` : 'Full calendar months · collected literature only';
  const total = rows.reduce((sum, row) => sum + row.papers, 0);
  byId('chart-summary').textContent = cumulative ? `${year}: ${rows.at(-1).cumulative} dated papers cumulatively through ${rows.at(-1).month}, including earlier years.` : `${year}: ${total} collected papers across ${rows.length} publication months.`;
  byId('data-caption').textContent = `${year} · cumulative totals include earlier years`;
  const body = byId('monthly-values');
  body.replaceChildren();
  rows.forEach(row => {
    const tr = document.createElement('tr');
    [row.month + (row.partial ? ' (partial)' : ''), row.papers, row.cumulative].forEach((value, index) => {
      const cell = document.createElement(index === 0 ? 'th' : 'td');
      if (index === 0) cell.scope = 'row';
      cell.textContent = value;
      tr.append(cell);
    });
    body.append(tr);
  });
}

async function initStatistics() {
  try {
    const response = await fetch('stats.json');
    if (!response.ok) throw new Error('Collection statistics unavailable.');
    collectionStats = await response.json();
    const stats = collectionStats;
    const latestYear = stats.search_cutoff.slice(0, 4);
    byId('paper-count').textContent = stats.papers;
    byId('year-count').textContent = stats.timeline.filter(row => row.month.startsWith(latestYear)).reduce((sum, row) => sum + row.papers, 0);
    byId('year-count-label').textContent = `Published in ${latestYear} · known month`;
    byId('collection-updated').textContent = stats.updated_on;
    byId('search-cutoff').textContent = stats.search_cutoff;
    byId('search-cutoff').dateTime = stats.search_cutoff;
    byId('collection-scope').textContent = `Counts cover our survey collection, including related methods, surveys, and benchmarks; they are not a census of Harness RSI methods. ${stats.resources} official resources are tracked separately.`;
    byId('date-coverage').textContent = `${stats.monthly_coverage}/${stats.papers} papers have known release months. The other ${stats.papers - stats.monthly_coverage} remain in the collection total but are excluded from these charts. Dates use first arXiv submission where available, otherwise bibliographic publication dates.`;
    const yearSelect = byId('publication-year');
    yearSelect.replaceChildren();
    [...new Set(stats.timeline.map(row => row.month.slice(0, 4)))].reverse().forEach(year => {
      const option = document.createElement('option');
      option.value = year;
      option.textContent = year;
      yearSelect.append(option);
    });
    yearSelect.disabled = false;
    yearSelect.addEventListener('change', renderPublicationChart);
    ['monthly', 'cumulative'].forEach(view => byId(`${view}-view`).addEventListener('click', () => {
      chartView = view;
      renderPublicationChart();
    }));
    const updates = byId('collection-updates');
    updates.replaceChildren();
    stats.history.map((snapshot, index) => ({ ...snapshot, index })).slice(-3).reverse().forEach(snapshot => {
      const entry = document.createElement('p');
      const date = document.createElement('time');
      date.dateTime = snapshot.date;
      date.textContent = snapshot.date;
      const description = document.createElement('span');
      if (snapshot.index === 0) description.textContent = `Initial collection · ${snapshot.papers} papers · ${snapshot.resources} resources`;
      else {
        const delta = snapshot.papers - stats.history[snapshot.index - 1].papers;
        description.textContent = `${snapshot.papers} papers · net change ${delta >= 0 ? '+' : ''}${delta} · ${snapshot.resources} resources`;
      }
      entry.append(date, description);
      updates.append(entry);
    });
    renderPublicationChart();
    new ResizeObserver(renderPublicationChart).observe(byId('publication-chart'));
  } catch (error) {
    byId('stats-error').hidden = false;
    console.error(error.message);
  }
}
initStatistics();
