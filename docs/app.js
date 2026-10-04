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
