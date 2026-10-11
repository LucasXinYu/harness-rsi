'use strict';
// The landing page reuses the survey's curated evidence, not a second set of counts.
(() => {
  const $ = id => document.getElementById(id);
  const el = (tag, className, text) => {
    const n = document.createElement(tag);
    if (className) n.className = className;
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const surfaces = {
    tools: ['Preserve a multiline edit as a file payload instead of dispatching its contents to the shell.', 'coding-route-edits'],
    context: ['Replace whole-file views with local reads and bound long tool returns before the context fills up.', 'coding-bounded-context'],
    memory: ['Retrieve competing-label challengers as well as similar examples to distinguish plausible answers.', 'reasoning-discriminating-evidence'],
    control: ['Distinguish an empty patch, a failing test and a missing dependency before choosing the next action.', 'coding-typed-recovery']
  };
  const surfaceTabs = [...document.querySelectorAll('[data-surface]')];
  function surface(index, focus = false) {
    surfaceTabs.forEach((t,i) => {t.setAttribute('aria-selected',String(i===index));t.tabIndex=i===index?0:-1;});
    const tab=surfaceTabs[index], [description,target]=surfaces[tab.dataset.surface];
    $('surface-panel').setAttribute('aria-labelledby',tab.id);
    $('surface-description').textContent=description;
    $('surface-source').href=`#finding-${target}`;
    document.querySelector('.hero-art').dataset.surface=tab.dataset.surface;
    document.dispatchEvent(new CustomEvent('harness-surface', {detail:tab.dataset.surface}));
    if(focus) tab.focus();
  }
  function tabKeys(event,index,length,select) {
    const next={ArrowRight:(index+1)%length,ArrowLeft:(index+length-1)%length,Home:0,End:length-1}[event.key];
    if(next!==undefined){event.preventDefault();select(next,true);}
  }
  surfaceTabs.forEach((t,i)=>{t.addEventListener('click',()=>surface(i));t.addEventListener('keydown',e=>tabKeys(e,i,surfaceTabs.length,surface));});

  const roles = [
    {label:'Propose',title:'Turn execution evidence into a candidate edit.',object:'READ / Code + traces + prior trials',text:'A proposer diagnoses a failure and constructs a candidate within the allowed edit boundary. The evidence may be supplied as a diagnostic report or inspected on demand.',contrast:'AHE supplies structured diagnostic reports. Meta-Harness lets the editing role inspect code, scores and raw traces through filesystem tools.',sources:[['AHE','https://arxiv.org/abs/2604.25850v4'],['Meta-Harness','https://openreview.net/forum?id=tmbOUyFx3R']]},
    {label:'Edit',title:'Change a bounded part of the harness.',object:'WRITE / Reusable software, skills or configuration',text:'The editable layer can include prompts, tool implementations, middleware, skills and memory procedures. Evaluation and other trusted components may remain fixed.',contrast:'AHE exposes seven edit modules. Meta-Harness edits a bounded Python program. The edit boundary determines which failures the loop can address.',sources:[['AHE','https://arxiv.org/abs/2604.25850v4'],['Meta-Harness','https://openreview.net/forum?id=tmbOUyFx3R']]},
    {label:'Execute',title:'Run the target model through the changed harness.',object:'PRODUCE / Actions, observations + task trajectory',text:'The target agent combines a model with a candidate harness to perform tasks. A working task solution and a reusable improvement to its solver are different artifacts.',contrast:'Meta-Harness performs separate searches for classification, mathematics and coding. Multi-Task Self-Harness instead optimizes one shared harness across benchmark mixtures.',sources:[['Meta-Harness','https://openreview.net/forum?id=tmbOUyFx3R'],['Multi-Task Self-Harness','https://arxiv.org/abs/2609.38372v1']]},
    {label:'Evaluate',title:'Ask whether the edit ran—and whether it helped.',object:'MEASURE / Activation, outcomes + costs',text:'Task rewards, preferences and proxies can guide selection. A mechanism activating, a proxy improving and a task succeeding support different conclusions.',contrast:'HarnessBank checks mechanism activation as part of gated verification. Evaluation records should remain tied to the executable candidate and its original setting.',sources:[['HarnessBank','https://arxiv.org/abs/2607.13683v2'],['Meta-Harness','https://openreview.net/forum?id=tmbOUyFx3R']]},
    {label:'Retain & reuse',title:'Choose what survives into the next trial.',object:'UPDATE / Parent versions + optimization history',text:'A controller selects parents, accepts or rejects candidates and updates retained versions and history. The target agent’s task memory is distinct from the proposer’s optimization history.',contrast:'DGM can revisit alternative archived parents. RRSI preserves rejected edits as negative evidence: a candidate can inform later proposals without becoming a future parent.',sources:[['DGM','https://proceedings.iclr.cc/paper_files/paper/2026/file/aa5f5e6eb6f613ec412f1d948dfa21a5-Paper-Conference.pdf'],['RRSI · analyzed version','https://arxiv.org/abs/2609.24972v2']]}
  ];
  function selectRole(index,focus=false){
    [...$('workflow-tabs').children].forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;if(focus&&i===index)tab.focus();});
    const role=roles[index],panel=$('workflow-panel');
    panel.setAttribute('aria-labelledby',`workflow-tab-${index}`);
    const summary=el('div','workflow-summary');
    summary.append(el('span','workflow-object',role.object),el('h3','',role.title),el('p','',role.text));
    const comparison=el('div','workflow-comparison');
    comparison.append(el('span','eyebrow','DESIGN CHOICES IN THE LITERATURE'),el('p','',role.contrast));
    const links=el('div','workflow-sources');
    role.sources.forEach(([name,url])=>{const a=el('a','',`${name} ↗`);a.href=url;links.append(a);});
    comparison.append(links);panel.replaceChildren(summary,comparison);
  }
  roles.forEach((role,index)=>{
    const t=el('button','workflow-tab');t.id=`workflow-tab-${index}`;t.type='button';t.setAttribute('role','tab');t.setAttribute('aria-controls','workflow-panel');
    t.append(el('span','',`0${index+1}`),el('strong','',role.label));
    t.addEventListener('click',()=>selectRole(index));t.addEventListener('keydown',e=>tabKeys(e,index,roles.length,selectRole));$('workflow-tabs').append(t);
  });
  selectRole(0);
  const cases=[
    {domain:'coding',finding:'route-edits',value:'36 → 25',unit:'mean interaction steps',label:'A tool call reaches the right destination.',setting:'ModularRSI · external Go repair case',description:'Route multiline writes by command name and preserve the code payload.',limit:'Case comparison; concurrent edits prevent isolating dispatch alone.'},
    {domain:'interactive',finding:'physical-recovery',value:'64% → 84%',unit:'mean task success',label:'Recovery survives a change of task.',setting:'Zetta · three related manipulation tasks',description:'An unchanged cumulative stack is tested on related placement tasks.',limit:'Transfer of the full stack; individual recovery branches are not isolated.'},
    {domain:'visual',finding:'composition-selection',value:'7.37 vs 6.93',unit:'held-out average score',label:'How drafts are selected matters.',setting:'AutoRef · fixed three-image budget',description:'The average falls when the combined failure-aware selector is replaced.',limit:'Combined-component ablation; it does not isolate order swapping.'}
  ];
  fetch('project.json').then(r=>{if(!r.ok)throw Error('Project data unavailable');return r.json();}).then(project=>{
    const portalLabels={coding:['⌘','Coding','Programs · patches · experiments'],reasoning:['∴','Reasoning','Proofs · retrieval · decisions'],interactive:['↗','Interactive','Browsers · services · robotics'],visual:['◈','Visual','Images · video · generation']};
    $('domain-portals').replaceChildren(...project.domains.map(domain=>{
      const [icon,label,description]=portalLabels[domain.id],a=el('a','domain-portal');
      a.dataset.domain=domain.id;a.href=`#benchmarks?domain=${domain.id}&category=all&setting=all`;
      a.append(el('span','portal-icon',icon));const copy=el('div','portal-copy');
      copy.append(el('strong','',label),el('span','',description),el('small','',`${domain.records} evidence records · ${domain.subcategories} subcategories`));
      a.append(copy,el('span','portal-arrow','↗'));return a;
    }));
    $('hero-records').textContent=project.evidence.records;$('hero-cutoff').textContent=project.evidence.cutoff;$('hero-cutoff').dateTime=project.evidence.cutoff;
    $('result-cards').replaceChildren(...cases.map((item,index)=>{
      const finding=project.domains.find(d=>d.id===item.domain)?.findings.find(f=>f.id===item.finding);
      if(!finding)throw Error('Featured result has no evidence record');
      const card=el('article','result-card');card.dataset.domain=item.domain;
      const top=el('div','result-meta');top.append(el('span','',`CASE / 0${index+1}`),el('span','',finding.evidence_type));
      const link=el('a','result-link','Trace this result ↗');link.href=`#finding-${item.domain}-${item.finding}`;
      const metric=el('div','result-metric');metric.append(el('strong','',item.value),el('span','',item.unit));
      card.append(top,metric,el('h3','',item.label),el('p','result-description',item.description),el('p','result-setting',item.setting),el('p','result-limit',item.limit),link);return card;
    }));
  }).catch(error=>{$('result-cards').textContent='Featured results could not be loaded. The full evidence remains available in the downloadable data.';console.error(error);});
  fetch('stats.json').then(r=>{if(!r.ok)throw Error('Statistics unavailable');return r.json();}).then(stats=>{$('hero-papers').textContent=stats.papers;}).catch(console.error);
  // Sticky navigation reflects the reading position without moving keyboard focus.
  const navLinks=[...document.querySelectorAll('nav a[href^="#"]')];
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting)navLinks.forEach(link=>{if(link.hash===`#${entry.target.id}`)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});});},{rootMargin:'-15% 0px -55% 0px'});
    navLinks.forEach(link=>{const target=document.querySelector(link.hash);if(target)observer.observe(target);});
  }
})();
