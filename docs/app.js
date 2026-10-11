'use strict';
const byId = id => document.getElementById(id);
let domains = [];
let activeDomain = '';

function element(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}

function selectDomain(id, focus = false) {
  const domain = domains.find(item => item.id === id);
  if (!domain) return;
  activeDomain = id;
  document.querySelectorAll('#domain-tabs [role="tab"]').forEach(tab => {
    const selected = tab.dataset.domain === id;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (selected && focus) tab.focus();
  });
  byId('domain-title').textContent = domain.name;
  byId('domain-panel').setAttribute('aria-labelledby', `tab-${id}`);
  byId('domain-subtitle').textContent = domain.subtitle;
  byId('domain-overline').textContent = `${domain.records} CATEGORY–SOURCE RECORDS · ${domain.subcategories} SUBCATEGORIES`;
  byId('domain-scope').replaceChildren(...domain.scope.map(label => element('span', '', label)));
  byId('domain-findings').replaceChildren(...domain.findings.map((finding, index) => {
    const card = element('article', 'finding-card');
    card.id = `finding-${domain.id}-${finding.id}`;
    const top = element('div', 'finding-top');
    top.append(element('span', 'finding-index', `OBSERVATION ${String(index+1).padStart(2,'0')}`), element('h4', '', finding.title), element('p', 'finding-tasks', finding.tasks));
    const pair = element('div', 'change-pair');
    ['before', 'after'].forEach((phase, index) => {
      if (index) pair.append(element('div', 'change-arrow', '↓'));
      const state = element('div', `change-state ${phase}`);
      state.append(element('span', '', phase.toUpperCase()), element('p', '', finding[phase]));
      pair.append(state);
    });
    const observation = element('div', 'finding-observation');
    observation.append(element('span', 'evidence-badge', finding.evidence_type), element('p', '', finding.result));
    const evidence = element('details', 'finding-evidence');
    evidence.append(element('summary', '', `${finding.sources.length} source${finding.sources.length > 1 ? 's' : ''} · evidence & limits`), element('p', '', finding.limit));
    const sources = element('ul');
    finding.sources.forEach(source => {
      const li = element('li');
      const link = element('a', '', `${source.name} ↗`);
      if (new URL(source.url).protocol !== 'https:') throw new Error('Expected a primary HTTPS source.');
      link.href = source.url;
      li.append(link, element('small', '', source.locator));
      sources.append(li);
    });
    evidence.append(sources);
    card.append(top, pair, observation, evidence);
    return card;
  }));
  byId('domain-status').textContent = `${domain.name}: ${domain.findings.length} selected findings displayed.`;
}

function showFinding(domainId, findingId, scroll = true) {
  selectDomain(domainId);
  const card = byId(`finding-${domainId}-${findingId}`);
  if (!card) return;
  card.querySelector('details').open = true;
  if (scroll) {
    card.scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block:'start'});
    card.tabIndex = -1;
    card.focus({preventScroll: true});
  }
}

function renderInsights(insights) {
  const labels = ['Interfaces', 'Decision evidence', 'Recovery'];
  const tabs = byId('insight-tabs');
  function select(index, focus = false) {
    [...tabs.children].forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      if (focus && i === index) tab.focus();
    });
    const insight = insights[index];
    const panel = byId('insight-panel');
    panel.setAttribute('aria-labelledby', `insight-tab-${insight.id}`);
    const heading = element('div', 'insight-heading');
    heading.append(element('h3', '', insight.title), element('p', '', insight.summary));
    const grid = element('div', 'comparison-grid');
    insight.cells.forEach(cell => {
      const domain = domains.find(d => d.id === cell.domain);
      const link = element('a', 'comparison-cell');
      link.href = `#finding-${cell.domain}-${cell.finding}`;
      link.append(element('span', 'cell-domain', domain.name.toUpperCase()), element('strong', '', cell.label), element('p', '', cell.detail), element('span', 'cell-link', 'Explore the evidence ↗'));
      link.addEventListener('click', event => {
        event.preventDefault();
        history.replaceState(null, '', link.hash);
        showFinding(cell.domain, cell.finding);
      });
      grid.append(link);
    });
    panel.replaceChildren(heading, element('p', 'comparison-question', insight.question), grid);
  }
  insights.forEach((insight, index) => {
    const tab = element('button', 'insight-tab');
    tab.type = 'button'; tab.id = `insight-tab-${insight.id}`;
    tab.setAttribute('role','tab'); tab.setAttribute('aria-controls','insight-panel');
    tab.append(element('span', '', `0${index+1}`), document.createTextNode(labels[index]));
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', event => {
      const next = {'ArrowRight': (index+1)%insights.length, 'ArrowLeft': (index+insights.length-1)%insights.length, 'Home':0, 'End':insights.length-1}[event.key];
      if (next !== undefined) { event.preventDefault(); select(next, true); }
    });
    tabs.append(tab);
  });
  select(0);
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
    const e = project.evidence;
    byId('evidence-numbers').replaceChildren(...[[e.records,'category–source records'],[e.papers,'research papers'],[e.subcategories,'task subcategories'],[domains.length,'domains']].map(([value,label]) => {
      const item = element('div'); item.append(element('strong','',value),element('span','',label)); return item;
    }));
    byId('evidence-scope').textContent = `Domain evidence cutoff: ${e.cutoff} · Plus ${e.resources} benchmark resource. Records can share a source and include reporting gaps; they are not independent effects. The larger literature collection below has a later search horizon.`;
    renderInsights(project.insights);
    const restoreFinding = () => {
      const match = location.hash.match(/^#finding-([^-]+)-(.+)$/);
      if (match) showFinding(match[1], match[2]);
    };
    restoreFinding();
    window.addEventListener('hashchange', restoreFinding);
    renderContributors(project.contributors || []);
    setFutureLink('paper-action', project.arxiv_url, 'arXiv paper');
    setFutureLink('paper-resource', project.arxiv_url, 'Read the survey');

    const narrow = window.matchMedia('(max-width: 760px)');
    const orientation = () => byId('domain-tabs').setAttribute('aria-orientation', 'horizontal');
    orientation();
    narrow.addEventListener('change', orientation);
  } catch (error) {
    byId('load-error').hidden = false;
    console.error(error.message);
  }
}
init();

let collectionStats;
let chartView = 'cumulative';
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
  const height = width > 650 ? 310 : 260, left = 34, right = 15, top = 31, bottom = 33;
  const plotHeight = height - top - bottom;
  const step = (width - left - right) / rows.length;
  const largest = Math.max(...rows.map(row => row[countKey]), 1);
  const tickSize = largest <= 8 ? 1 : largest <= 40 ? 5 : Math.ceil(largest / 40) * 10;
  const maximum = Math.ceil(largest / (tickSize * 4)) * tickSize * 4;
  const svg = svgElement('svg', { viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-labelledby': 'plot-title plot-description' });
  const heading = cumulative ? 'Cumulative papers by publication month' : 'Papers by publication month';
  svg.append(svgElement('title', { id: 'plot-title' }, `${heading}, ${year}`));
  svg.append(svgElement('desc', { id: 'plot-description' }, rows.map(row => `${row.month}: ${row[countKey]}${row.partial ? ', partial month' : ''}`).join('; ')));
  const group = svgElement('g', { 'font-family': 'Manrope, Arial, sans-serif', 'font-size': 10, fill: '#94a9bb' });
  for (let i = 0; i <= 4; i++) {
    const y = top + plotHeight * (1 - i / 4);
    group.append(svgElement('path', { d: `M${left} ${y}H${width-right}`, stroke: '#243345', fill: 'none' }));
    group.append(svgElement('text', { x: left - 10, y: y + 3, 'text-anchor': 'end' }, maximum * i / 4));
  }
  const points = rows.map((row, i) => ({ x: left + step * (i + .5), y: top + plotHeight * (1 - row[countKey] / maximum), row }));
  if (cumulative) {
    const path = points.map(point => `${point.x},${point.y}`).join(' ');
    group.append(svgElement('polygon', { points: `${points[0].x},${top+plotHeight} ${path} ${points.at(-1).x},${top+plotHeight}`, fill: '#0f343c' }));
    group.append(svgElement('polyline', { points: path, fill: 'none', stroke: '#79ead3', 'stroke-width': 2 }));
  }
  points.forEach(({ x, y, row }) => {
    const color = row.partial ? '#ffc080' : '#79ead3';
    const mark = cumulative
      ? svgElement('circle', { cx: x, cy: y, r: 3.5, fill: color })
      : svgElement('rect', { x: x - step * .26, y, width: step * .52, height: top + plotHeight - y, rx: 2, fill: color });
    mark.append(svgElement('title', {}, `${row.month}: ${row[countKey]} papers${row.partial ? ' (partial month)' : ''}`));
    group.append(mark);
    group.append(svgElement('text', { x, y: y - 10, 'text-anchor': 'middle', fill: color }, row[countKey]));
    group.append(svgElement('text', { x, y: height - 10, 'text-anchor': 'middle', 'font-size': width < 400 ? 9 : 10 }, monthName(row.month) + (row.partial ? '*' : '')));
  });
  const tooltip = document.createElement('div');
  tooltip.className = 'chart-tooltip';
  tooltip.hidden = true;
  tooltip.setAttribute('aria-hidden', 'true');
  points.forEach(({ x, row }) => {
    const hit = svgElement('rect', { x: x - step / 2, y: top - 18, width: step, height: plotHeight + 18, fill: 'transparent', class: 'chart-hit', tabindex: 0, role: 'img', 'aria-label': `${row.month}: ${row[countKey]} ${cumulative ? 'cumulative papers' : 'papers'}${row.partial ? ', partial month' : ''}` });
    const show = () => {
      tooltip.replaceChildren();
      const date = document.createElement('span');
      date.textContent = `${monthName(row.month)} ${year}${row.partial ? ' · partial' : ''}`;
      const value = document.createElement('strong');
      value.textContent = `${row[countKey]} ${cumulative ? 'cumulative' : 'papers'}`;
      tooltip.append(date, value);
      tooltip.hidden = false;
      tooltip.style.left = `${Math.max(0, Math.min(width - tooltip.offsetWidth, x - tooltip.offsetWidth / 2))}px`;
    };
    hit.addEventListener('pointerenter', show);
    hit.addEventListener('focus', show);
    hit.addEventListener('pointerleave', () => { tooltip.hidden = true; });
    hit.addEventListener('blur', () => { tooltip.hidden = true; });
    hit.addEventListener('keydown', event => { if (event.key === 'Escape') tooltip.hidden = true; });
    group.append(hit);
  });
  svg.append(group);
  panel.replaceChildren(svg, tooltip);
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


// Contributors describe project assistance, not scholarly authorship.
function renderContributors(contributors) {
  const grid = byId('contributor-grid');
  grid.replaceChildren();
  contributors.forEach(person => {
    const card = document.createElement('article');
    card.className = 'contributor-card';
    card.dataset.kind = person.kind;
    const avatar = document.createElement('div');
    avatar.className = 'contributor-avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = person.kind === 'ai' ? '⌘' : 'LY';
    const copy = document.createElement('div');
    const name = document.createElement('h3');
    if (person.url && new URL(person.url).protocol === 'https:') {
      const link = document.createElement('a');
      link.href = person.url;
      link.textContent = `${person.name} ↗`;
      name.append(link);
    } else name.textContent = person.name;
    const role = document.createElement('p');
    role.className = 'contributor-role';
    role.textContent = person.role;
    const description = document.createElement('p');
    description.className = 'contributor-description';
    description.textContent = person.description;
    copy.append(name, role, description);
    card.append(avatar, copy);
    grid.append(card);
  });
}

function figureAsset(path) {
  if (typeof path !== 'string' || !path.startsWith('assets/') || path.split('/').includes('..') || !/\.(svg|png|jpe?g|webp|avif)$/i.test(path)) {
    throw new Error('Figures must use local image assets in assets/.');
  }
  return path;
}

function openFigure(figure) {
  const source = figureAsset(figure.src);
  const viewer = byId('figure-viewer');
  byId('viewer-title').textContent = figure.title;
  byId('viewer-caption').textContent = figure.caption;
  byId('viewer-image').src = source;
  byId('viewer-image').alt = figure.alt;
  byId('download-figure').href = source;
  byId('download-figure').download = source.split('/').at(-1);
  byId('viewer-stage').classList.remove('zoomed');
  byId('zoom-figure').setAttribute('aria-pressed', 'false');
  byId('zoom-figure').textContent = 'Zoom in +';
  viewer.showModal();
  document.body.style.overflow = 'hidden';
  byId('viewer-stage').scrollTop = 0;
  byId('viewer-stage').scrollLeft = 0;
}

byId('expand-lens')?.addEventListener('click', () => openFigure({
  src: 'assets/recursive-loop.svg', title: 'The recursive loop',
  caption: 'Original Harness RSI project artwork. A continuous ribbon represents repetition, transformation, and a return to the improvement process.',
  alt: 'An original violet ribbon looping through a continuous three-dimensional form.'
}));
byId('close-viewer').addEventListener('click', () => byId('figure-viewer').close());
byId('figure-viewer').addEventListener('close', () => { document.body.style.overflow = ''; });
byId('figure-viewer').addEventListener('click', event => {
  if (event.target !== byId('figure-viewer')) return;
  const bounds = byId('figure-viewer').getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) byId('figure-viewer').close();
});
byId('zoom-figure').addEventListener('click', () => {
  const zoomed = byId('viewer-stage').classList.toggle('zoomed');
  byId('zoom-figure').setAttribute('aria-pressed', String(zoomed));
  byId('zoom-figure').textContent = zoomed ? 'Fit to view −' : 'Zoom in +';
});
