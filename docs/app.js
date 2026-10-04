'use strict';
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let catalog, topic = 'all', limit = 20;

function chart() {
  const stats = catalog.stats, year = +$('year').value, quarterly = $('group').value === 'quarter';
  const cutoff = catalog.config.search_cutoff, maxMonth = year === +cutoff.slice(0,4) ? +cutoff.slice(5,7) : 12;
  const n = quarterly ? Math.ceil(maxMonth/3) : maxMonth;
  const rows = Array.from({length:n}, (_, i) => {
    const m = Math.min(quarterly ? (i+1)*3 : i+1, maxMonth);
    const bound = `${year}-${String(m).padStart(2,'0')}`;
    const sum = series => Object.entries(series).reduce((a,[k,v]) => a+(k<=bound?v:0),0);
    return {label: quarterly ? `Q${i+1}` : new Date(year,i,1).toLocaleString('en',{month:'short'}), all:sum(stats.monthly),focus:sum(stats.focus_monthly)};
  });
  const W=700,H=280,L=40,R=25,T=34,B=36,pw=W-L-R,ph=H-T-B,max=Math.max(20,Math.ceil(Math.max(...rows.map(r=>r.all))/40)*40);
  const x=i=>L+pw*(n===1?.5:i/(n-1)),y=v=>T+ph-v/max*ph;
  let svg=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Cumulative included papers by release month, ${year}</title><desc id="chart-desc">${rows.map(r=>`${r.label}: ${r.all} all dated papers, ${r.focus} Harness Optimization and Search papers`).join('; ')}</desc><g font-family="Arial,sans-serif" font-size="11" fill="#6a7a6e">`;
  for(let i=0;i<=4;i++){const v=max*i/4;svg+=`<path d="M${L} ${y(v)}H${W-R}" stroke="#e1e5dc"/><text x="${L-10}" y="${y(v)+4}" text-anchor="end">${v}</text>`;}
  rows.forEach((r,i)=>{svg+=`<text x="${x(i)}" y="${H-12}" text-anchor="middle">${r.label}</text>`;});
  for(const [key,color] of [['all','#235f48'],['focus','#bb683d']]){
    const points=rows.map((r,i)=>`${x(i)},${y(r[key])}`).join(' ');
    svg+=`<polyline points="${points}" fill="none" stroke="${color}" stroke-width="2.5"/>`;
    rows.forEach((r,i)=>{svg+=`<circle cx="${x(i)}" cy="${y(r[key])}" r="3.5" fill="${color}"><title>${r.label}: ${r[key]}</title></circle><text x="${x(i)}" y="${y(r[key])-11}" fill="${color}" text-anchor="middle" font-size="10">${r[key]}</text>`;});
  }
  $('publication-chart').innerHTML=svg+'</g></svg>';
  $('publication-table').innerHTML='<caption>Cumulative totals, including earlier years</caption><thead><tr><th>Period</th><th>All dated papers</th><th>Harness optimization & search</th></tr></thead><tbody>'+rows.map(r=>`<tr><td>${year} ${r.label}</td><td>${r.all}</td><td>${r.focus}</td></tr>`).join('')+'</tbody>';
  $('date-note').textContent=`${stats.monthly_coverage} of ${stats.papers} papers have a known release month. Earlier years are included in cumulative totals. The final period ends at the ${cutoff} search cutoff. This is publication history, not collection history.`;
}

function collectionChart(){
  const history=catalog.stats.history,first=history[0],last=history[history.length-1];
  if(history.length===1){
    $('collection-chart').innerHTML=`<div class="baseline-number">${first.papers}<span>papers</span></div><div class="baseline-stem"></div><div class="baseline-label">${first.date} · INITIAL IMPORT</div>`;
    $('baseline-note').textContent='One snapshot so far. New collection points will appear when papers are added or removed; no earlier growth has been inferred.';
  }else{
    const W=300,H=130,max=Math.max(...history.map(h=>h.papers),1),start=Date.parse(first.date),span=Date.parse(last.date)-start;
    const pts=history.map(h=>[15+(Date.parse(h.date)-start)/span*270,110-h.papers/max*90]);
    $('collection-chart').innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Collection history from ${first.date} to ${last.date}"><polyline points="${pts.map(p=>p.join(',')).join(' ')}" fill="none" stroke="#235f48" stroke-width="2"/>${pts.map(([x,y],i)=>`<circle cx="${x}" cy="${y}" r="3" fill="#235f48"><title>${history[i].date}: ${history[i].papers} papers</title></circle>`).join('')}</svg>`;
    $('baseline-note').textContent=`${last.papers-first.papers>=0?'+':''}${last.papers-first.papers} papers since the ${first.date} baseline. Counts reflect additions and removals.`;
  }
  $('snapshot-list').innerHTML=history.slice(-5).reverse().map(h=>`<p><span>${h.date}</span><span>${h.papers} papers / ${h.resources} resources</span></p>`).join('');
}

function renderTopics(){
  $('topic-list').innerHTML=[['all','All topics',catalog.records.length],...Object.entries(catalog.stats.categories).map(([k,n])=>[k,k,n])].map(([key,label,count])=>`<button class="topic" data-topic="${esc(key)}" aria-pressed="${topic===key}"><span>${esc(label)}</span><span>${count}</span></button>`).join('');
  $('topic-list').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{topic=b.dataset.topic;limit=20;renderTopics();renderPapers();}));
}

function renderPapers(){
  const query=$('search').value.toLowerCase().trim(),kind=$('kind').value,sort=$('sort').value;
  const records=catalog.records.filter(r=>(topic==='all'||r.category===topic)&&(kind==='all'||r.kind===kind)&&(!query||[r.title,r.authors,r.summary,r.category,r.id].join(' ').toLowerCase().includes(query)));
  records.sort((a,b)=>{
    if(sort==='title')return a.title.localeCompare(b.title);
    if(sort==='added')return b.added_on.localeCompare(a.added_on)||a.title.localeCompare(b.title);
    // Unknown dates remain last under either date ordering.
    const da=a.release.value,db=b.release.value;
    if(!da)return db?1:a.title.localeCompare(b.title);if(!db)return -1;
    return (sort==='oldest'?da.localeCompare(db):db.localeCompare(da))||a.title.localeCompare(b.title);
  });
  const shown=records.slice(0,limit);
  $('result-count').textContent=`${records.length} records${records.length>limit?` · showing ${shown.length}`:''}`;
  $('papers').innerHTML=shown.map(r=>`<article class="paper-card"><div class="paper-meta"><span>${esc(r.release.value||'Date not recorded')}</span><span class="paper-tag">${r.kind==='paper'?'Paper / manuscript':'Official resource'}</span><span>${esc(r.category)}</span></div><h3><a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.title)} ↗</a></h3><p class="authors">${esc(r.authors)}</p><p class="summary">${esc(r.summary)}</p><div class="paper-footer"><details><summary>Source & date details</summary><div>${esc(r.venue)}<br>Citation key: ${esc(r.id)}<br>Date precision: ${esc(r.release.precision)} · ${esc(r.release.basis)}<br>Added to this repository: ${esc(r.added_on)}${r.doi?`<br>DOI: ${esc(r.doi)}`:''}<br><a href="${esc(r.release.source)}" target="_blank" rel="noopener noreferrer">Date source ↗</a></div></details><a class="source-link" href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">Primary source ↗</a></div></article>`).join('')||'<p class="empty">No matching records. Try another term or topic.</p>';
  $('load-more').hidden=limit>=records.length;
}

async function init(){
  try{
    const response=await fetch('catalog.json');if(!response.ok)throw new Error(`HTTP ${response.status}`);
    catalog=await response.json();
    $('paper-count').textContent=catalog.stats.papers;$('category-count').textContent=Object.keys(catalog.stats.categories).length;$('resource-count').textContent=catalog.stats.resources;
    $('cutoff').textContent=catalog.config.search_cutoff;$('updated').textContent=`Collection updated ${catalog.config.updated_on}`;
    const years=[...new Set(Object.keys(catalog.stats.monthly).map(m=>m.slice(0,4)))].sort().reverse();
    $('year').innerHTML=years.map(y=>`<option value="${y}">${y}</option>`).join('');
    ['year','group'].forEach(id=>$(id).addEventListener('change',chart));
    ['search','kind','sort'].forEach(id=>$(id).addEventListener(id==='search'?'input':'change',()=>{limit=20;renderPapers();}));
    $('reset').addEventListener('click',()=>{topic='all';limit=20;$('search').value='';$('kind').value='all';$('sort').value='newest';renderTopics();renderPapers();});
    $('load-more').addEventListener('click',()=>{limit+=20;renderPapers();});
    chart();collectionChart();renderTopics();renderPapers();
  }catch(error){$('error').hidden=false;$('error').textContent='The catalog could not be loaded. Serve this folder over HTTP or read the GitHub README. '+error.message;}
}
init();
