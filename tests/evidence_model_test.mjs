import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {selectRecords,selectPatterns,sourceCount} from '../docs/evidence-model.mjs';
const data=JSON.parse(readFileSync(new URL('../docs/evidence.json',import.meta.url)));
let views=0;
for (const domain of new Set(data.records.map(r=>r.domain))) {
  for (const category of ['all',...new Set(selectRecords(data,domain).map(r=>r.category_id))]) {
    const rows=selectRecords(data,domain,category);
    for (const benchmark of ['all',...new Set(rows.flatMap(r=>r.benchmarks.map(b=>b.id)))]) {
      const selected=selectRecords(data,domain,category,benchmark);
      assert(selected.length>0);
      assert.equal(new Set(selected.map(r=>r.id)).size,selected.length);
      assert(sourceCount(selected)<=selected.length);
      for (const pattern of selectPatterns(data,selected,benchmark)) {
        for (const item of pattern.cases) {
          assert(selected.some(r=>r.id===item.record));
          if (benchmark!=='all' && item.benchmarks) assert(item.benchmarks.includes(benchmark));
        }
      }
      views++;
    }
  }
}
const tb=selectRecords(data,'coding','all','terminal-bench-2-0');
assert(!selectPatterns(data,tb,'terminal-bench-2-0').some(p=>p.cases.some(c=>c.record.endsWith('--modularrsi2026'))));
const go=selectRecords(data,'coding','all','go-repair-modularrsi-case');
assert.equal(sourceCount(go),1);
assert.equal(selectPatterns(data,go,'go-repair-modularrsi-case').length,1);
const balatro=selectRecords(data,'interactive','all','balatro');
assert.equal(selectPatterns(data,balatro,'balatro').length,0); // Liar's Dice details are not Balatro discoveries.
assert.equal(sourceCount(selectRecords(data,'reasoning','all','locomo')),2);
console.log(`Validated ${views} domain/category/benchmark views and cross-setting attribution boundaries.`);
