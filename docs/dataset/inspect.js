const node=(tag,text,className)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(className)e.className=className;return e;};
async function main(){
  const pr=await fetch('latest.json');if(!pr.ok)throw new Error('No release pointer');const pointer=await pr.json();
  const base=`v${pointer.version}/`;const res=await fetch(base+'dataset.json');if(!res.ok)throw new Error('Dataset unavailable');
  const data=await res.json();const m=data.metadata;
  document.getElementById('version').textContent=`v${m.version} · ${m.status.replaceAll('_',' ')} · prepared ${m.prepared_on}`;
  document.getElementById('coverage').textContent=`${m.record_count} records · ${m.distinct_source_count} works · ${m.primary_checked_record_count} primary checks · ${m.legacy_record_count} inherited records · ${m.signal_count} scoped signals`;
  for(const [name,file] of [['Dataset card','DATASET_CARD.md'],['Protocol','PROTOCOL.md'],['License scope','LICENSE-DATA.md'],['All records','records.jsonl'],['Primary-checked subset','primary-checked.records.jsonl'],['Records CSV','records.csv'],['Signals CSV','signals.csv'],['Quality report','quality-report.json'],['Corrections','corrections.json'],['Review queue','review-queue.csv']]){const a=node('a',name);a.href=base+file;document.getElementById('downloads').append(a);}
  const review=document.getElementById('review'),query=document.getElementById('query');
  function render(){
    const q=query.value.trim().toLowerCase();const rows=data.records.filter(r=>(review.value==='all'||r.review.status===review.value)&&(!q||JSON.stringify(r).toLowerCase().includes(q)));
    const cards=rows.map(r=>{
      const card=node('article',undefined,'data-card');card.id=r.id;
      card.append(node('p',`${r.domain} / ${r.category} · ${r.review.status.replaceAll('_',' ')}`,'status'),node('h2',r.title));
      const detail=node('details');detail.open=location.hash.slice(1)===r.id;
      detail.append(node('summary',`${r.signals.length} scoped signals · inspect mechanism, protocol and sources`));
      for(const s of r.sections)detail.append(node('h3',s.label),node('p',s.text));
      detail.append(node('p',`Selection: ${r.selection_protocol??'Not assessed in this pass.'}`),node('p',`Weight boundary: ${r.weight_update_boundary}. Transfer: ${r.transfer_regime}.`));
      for(const s of r.signals){detail.append(node('h3',`${s.outcome.replaceAll('_',' ')} · ${s.attribution.replaceAll('_',' ')}`),node('p',s.summary),node('p',s.scope,'muted'));const a=node('a',`Primary source — ${s.primary_support.locator}`);a.href=s.primary_support.url;detail.append(a);}
      detail.append(node('p',`Review: ${r.review.scope} Human review: ${r.review.human_review_status}.`,'muted'));
      for(const s of r.sources){const a=node('a',`${s.name} — ${s.locator}`);a.href=s.url;detail.append(node('p',`${s.source_version??'Version not recorded'} · first release ${s.first_release_date??'unknown'} · version date ${s.source_version_date??'unknown'}`,'muted'),a);}
      card.append(detail);return card;
    });document.getElementById('records').replaceChildren(...cards);document.getElementById('count').textContent=`${rows.length} records shown`;
  }
  review.addEventListener('change',render);query.addEventListener('input',render);render();
  if(location.hash){const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));target?.scrollIntoView();}
}
main().catch(error=>{console.error(error);document.getElementById('error').hidden=false;});
