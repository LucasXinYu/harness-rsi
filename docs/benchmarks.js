import {selectRecords, selectPatterns, sourceCount} from './evidence-model.mjs';

const $ = id => document.getElementById(id);
const node = (tag, className = '', text) => {
  const item = document.createElement(tag);
  item.className = className;
  if (text !== undefined) item.textContent = text;
  return item;
};
const domainNames = {coding:'Coding', reasoning:'Reasoning & information', interactive:'Interactive & embodied', visual:'Visual understanding & generation'};
const roleNames = {study:'Study setting', transfer:'Transfer evaluation', evaluation:'Evaluation setting', case:'Illustrative case', setting:'Study-specific setting'};

async function loadJSON(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Could not load ${path}`);
  return response.json();
}

async function initBenchmarks() {
  const data = await loadJSON('evidence.json');
  const recordById = new Map(data.records.map(record => [record.id, record]));
  const benchmarkById = new Map(data.benchmarks.map(benchmark => [benchmark.id, benchmark]));
  const domain = $('bench-domain'), category = $('bench-category'), benchmark = $('bench-setting');
  function options(select, values, chosen) {
    select.replaceChildren(...values.map(([value, label]) => {
      const option = node('option', '', label); option.value = value; return option;
    }));
    select.value = values.some(item => item[0] === chosen) ? chosen : values[0][0];
  }
  options(domain, Object.entries(domainNames), 'coding');
  function updateCategories(chosen = 'all') {
    const categories = new Map(selectRecords(data, domain.value).map(r => [r.category_id, r.category]));
    options(category, [['all','All subcategories'],...categories], chosen);
  }
  function updateBenchmarks(chosen = 'all') {
    const ids = new Set(selectRecords(data, domain.value, category.value).flatMap(r => r.benchmarks.map(b => b.id)));
    const values = [...ids].map(id => [id,benchmarkById.get(id).name]).sort((a,b)=>a[1].localeCompare(b[1]));
    options(benchmark, [['all','Compare all settings'],...values], chosen);
  }
  function openRecord(id) {
    const record = $(`record-${id}`);
    if (!record) return;
    record.open = true;
    record.scrollIntoView({block:'nearest', behavior:'smooth'});
    record.querySelector('summary').focus({preventScroll:true});
  }
  function render() {
    const rows = selectRecords(data, domain.value, category.value, benchmark.value);
    const patterns = selectPatterns(data, rows, benchmark.value);
    const name = benchmark.value === 'all'
      ? (category.value === 'all' ? domainNames[domain.value] : rows[0].category)
      : benchmarkById.get(benchmark.value).name;
    $('benchmark-heading').textContent = name;
    $('benchmark-count').textContent = `${rows.length} category–source record${rows.length === 1 ? '' : 's'} · ${sourceCount(rows)} distinct source${sourceCount(rows) === 1 ? '' : 's'}`;
    $('benchmark-scope').textContent = benchmark.value === 'all'
      ? 'Compare within the selected task family. These studies use different models, splits and budgets; their scores are not a shared leaderboard.'
      : 'Records may span several settings. The detailed case and reported gain belong only to the setting named in the record; transfer tests are not new discoveries.';
    $('benchmark-patterns').replaceChildren(...patterns.map((pattern,index) => {
      const card = node('article','benchmark-pattern');
      const papers = new Set(pattern.cases.map(item=>recordById.get(item.record).key)).size;
      const top = node('div','pattern-meta');
      top.append(node('span','',String(index+1).padStart(2,'0')),node('span','',papers > 1 ? `Comparison · ${papers} sources in this view` : 'One source in this view'));
      card.append(top,node('h4','',pattern.title));
      const cases = node('ul','pattern-cases');
      pattern.cases.forEach(item => {
        const li = node('li');
        li.append(node('p','',item.change_by_benchmark?.[benchmark.value] || item.change));
        const button = node('button','evidence-jump','Read the study record ↗');
        button.type = 'button'; button.addEventListener('click',()=>openRecord(item.record));
        li.append(button); cases.append(li);
      });
      card.append(cases,node('p','pattern-lesson',pattern.lesson));
      return card;
    }));
    if (!patterns.length) {
      const empty = node('div','evidence-gap');
      empty.append(node('span','eyebrow','A VISIBLE EVIDENCE GAP'),node('h4','','Coverage is not yet a common pattern.'),node('p','','The records here document an experiment, an update procedure or a case in a different setting. We have not extracted a sufficiently specific benchmark-level comparison to promote into a pattern. Read the source records for what is established.'));
      $('benchmark-patterns').append(empty);
    }
    $('benchmark-records').replaceChildren(...rows.map((record,index) => {
      const details = node('details','benchmark-record'); details.id = `record-${record.id}`;
      const summary = node('summary');
      const heading = node('span','record-title',record.title);
      const selectedSetting = record.benchmarks.find(item=>item.id === benchmark.value);
      if (selectedSetting && selectedSetting.role !== 'study') heading.append(node('small','record-role',roleNames[selectedSetting.role]));
      summary.append(node('span','record-index',String(index+1).padStart(2,'0')),heading,node('span','record-plus','+'));
      details.append(summary);
      const content = node('div','record-content');
      content.append(node('span','record-status',record.evidence_status));
      const settings = node('div','record-settings');
      record.benchmarks.forEach(item=>{
        const button = node('button', item.id === benchmark.value ? 'active' : '', benchmarkById.get(item.id).name + (item.role === 'study' ? '' : ` · ${roleNames[item.role]}`));
        button.type='button';
        button.addEventListener('click',()=>{benchmark.value=item.id; render(); updateHash();});
        settings.append(button);
      });
      content.append(settings);
      record.sections.forEach(field=>{
        const section=node('div','record-field');
        section.append(node('h5','',field.label),node('p','',field.text));
        content.append(section);
      });
      const sources = node('div','record-sources');
      sources.append(node('h5','','Primary sources & locators'));
      record.sources.forEach(source=>{
        const link=node('a','',`${source.name} ↗`); link.href=source.url;
        sources.append(link,node('p','',source.locator));
      });
      content.append(sources);
      const related = data.records.filter(item=>item.key === record.key && item.id !== record.id);
      if (related.length) {
        const links = node('div','record-related');
        links.append(node('h5','','Other contexts from this study'));
        related.forEach(item=>{
          const button=node('button','',`${item.category} ↗`);button.type='button';
          button.addEventListener('click',()=>{
            domain.value=item.domain;updateCategories(item.category_id);updateBenchmarks();render();updateHash();openRecord(item.id);
          });
          links.append(button);
        });
        content.append(links);
      }
      details.append(content); return details;
    }));
    $('benchmark-status').textContent = `${name}: ${rows.length} records and ${patterns.length} comparison lenses shown.`;
  }
  function updateHash() {
    const params = new URLSearchParams({domain:domain.value,category:category.value,setting:benchmark.value});
    history.replaceState(null,'',`#benchmarks?${params}`);
  }
  function restoreHash() {
    if (!location.hash.startsWith('#benchmarks?')) return false;
    const p = new URLSearchParams(location.hash.split('?')[1]);
    if (domainNames[p.get('domain')]) domain.value=p.get('domain');
    updateCategories(p.get('category')); updateBenchmarks(p.get('setting')); render();
    // Dynamic fragment parameters are not element IDs; scroll to the actual section.
    $('benchmarks').scrollIntoView({block:'start'});
    return true;
  }
  domain.addEventListener('change',()=>{updateCategories();updateBenchmarks();render();updateHash();});
  category.addEventListener('change',()=>{updateBenchmarks();render();updateHash();});
  benchmark.addEventListener('change',()=>{render();updateHash();});
  $('benchmark-reset').addEventListener('click',()=>{updateCategories();updateBenchmarks();render();updateHash();});
  $('domain-evidence-link').addEventListener('click',()=>{
    const selected=document.querySelector('#domain-tabs [aria-selected=true]');
    if (selected) domain.value=selected.dataset.domain;
    updateCategories();updateBenchmarks();render();updateHash();$('benchmarks').scrollIntoView({block:'start'});
  });
  $('expand-records').addEventListener('click',()=>{
    const items=[...document.querySelectorAll('.benchmark-record')];
    const open = !items.every(item=>item.open);
    items.forEach(item=>{item.open=open;});
  });
  $('benchmark-coverage').textContent=`${data.records.length} records · ${new Set(data.records.map(r=>r.category_id)).size} subcategories · ${data.benchmarks.length} benchmark / setting labels`;
  $('benchmark-version').textContent=`Evidence release ${data.updated_on} · survey cutoff ${data.cutoff}`;
  $('evidence-download').href='evidence.json';
  updateCategories('repository-level-software-engineering');updateBenchmarks('swe-bench-verified');render();
  restoreHash();window.addEventListener('hashchange',restoreHash);
}

async function initMaintenance() {
  const updates=await loadJSON('updates.json');
  $('maintenance-commitment').textContent=updates.commitment;
  $('maintenance-cadence').textContent=updates.cadence;
  $('maintenance-steps').replaceChildren(...updates.steps.map((step,index)=>{
    const item=node('article');item.append(node('span','',`0${index+1}`),node('h3','',step.title),node('p','',step.text));return item;
  }));
  $('evidence-releases').replaceChildren(...updates.releases.map(release=>{
    const item=node('article','evidence-release');
    const date=node('time','',release.date);date.dateTime=release.date;
    item.append(date,node('h3','',release.title));
    const list=node('ul');release.changes.forEach(change=>list.append(node('li','',change)));
    item.append(list);return item;
  }));
}

initBenchmarks().catch(error=>{console.error(error);$('benchmark-error').hidden=false;});
initMaintenance().catch(error=>{console.error(error);$('maintenance-error').hidden=false;});
