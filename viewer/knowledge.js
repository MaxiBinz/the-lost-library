'use strict';

function localPath(path) {
  if (typeof path !== 'string' || !path || /[\\?#:\x00-\x1f]/.test(path)) return '';
  const parts = path.split('/');
  if (parts.some(p => !p || p === '.' || p === '..')) return '';
  return '../' + parts.map(encodeURIComponent).join('/');
}
function sourceLink(value) {
  if (typeof value !== 'string') return '';
  try {
    const url = new URL(value);
    return ['https:', 'http:'].includes(url.protocol) ? url.href : '';
  } catch { return localPath(value); }
}
function filterLeads(leads, query, state) {
  const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  return leads.filter(l => {
    const identifier = l.id.startsWith('pair-') && !query.trim().startsWith('pair-') ? '' : l.id;
    const text = JSON.stringify([identifier,l.title,l.subjects,l.relationship_type,l.exact_claim,l.already_published,l.supporting,l.contradicting]).toLowerCase();
    return (!state || l.decision_state === state) && terms.every(t => text.includes(t));
  });
}

if (typeof module !== 'undefined') module.exports = { localPath, sourceLink, filterLeads };
if (typeof document !== 'undefined') {
  const $ = id => document.getElementById(id);
  const el = (tag, value) => { const node = document.createElement(tag); if (value != null) node.textContent = value; return node; };
  const textValue = v => typeof v === 'string' ? v : JSON.stringify(v, null, 2);
  const list = (parent, title, values) => {
    parent.append(el('h3', title));
    if (!values?.length) { parent.append(el('p', 'No additional item recorded.')); return; }
    const ul = el('ul'); values.forEach(v => ul.append(el('li', textValue(v)))); parent.append(ul);
  };
  const raw = (parent, value, title = 'Full structured record') => {
    const details = el('details'); details.append(el('summary', title), el('pre', JSON.stringify(value, null, 2))); parent.append(details);
  };
  const link = (parent, value, label) => {
    const href = sourceLink(value); if (!href) return;
    const a = el('a', label || value); a.href = href; parent.append(a, el('br'));
  };
  Promise.all(['../data/knowledge.v1.json', '../data/lead_register.v1.json'].map(async path => {
    const response = await fetch(path); if (!response.ok) throw new Error(`${path}: ${response.status}`); return response.json();
  })).then(([graph, register]) => {
    const entities = new Map(graph.entities.map(e => [e.id, e]));
    $('knowledge-status').textContent = `${register.leads.length} lead/question entries; ${register.coverage.all_pair_leads} physical-pair leads; ${graph.evidence.length} image regions. Topic entries can describe the same objects. No state count is an independent evidence count.`;
    function showLead(lead) {
      const detail = $('lead-detail'); detail.replaceChildren(el('h3', lead.title), el('p', `${lead.decision_state} · ${lead.relationship_type}`), el('p', lead.exact_claim), el('p', 'Work performed: ' + lead.test_execution));
      list(detail, 'Already published or catalogued', lead.already_published);
      list(detail, 'Supporting observations / arguments', lead.supporting);
      list(detail, 'Counterevidence / limits', lead.contradicting);
      detail.append(el('h3', 'Strongest next test'), el('p', lead.strongest_feasible_test), el('h3', 'What would change the status?'), el('p', lead.what_changes_state));
      list(detail, 'Missing inputs', (lead.required_inputs.dependencies || []).map(id => graph.dependencies.find(d => d.id === id) || id));
      list(detail, 'Local work still possible', lead.required_inputs.local_tasks || []);
      detail.append(el('h3', 'Subjects'));
      lead.subjects.forEach(id => { const b = el('button', entities.get(id)?.label || id); b.onclick = () => { $('entity-search').value = id; renderEntities(); $('entities').scrollIntoView(); }; detail.append(b, el('br')); });
      detail.append(el('h3', 'Source records'));
      lead.origins.forEach(o => link(detail, o.path, `${o.path} ${o.id || o.row || ''}`));
      lead.already_published.forEach(p => (p.sources || []).forEach(s => link(detail, typeof s === 'string' ? s : s.url)));
      raw(detail, lead);
    }
    function renderLeads() {
      const shown = filterLeads(register.leads, $('lead-search').value, $('lead-state').value);
      $('lead-count').textContent = `${shown.length} of ${register.leads.length} entries`;
      $('lead-rows').replaceChildren();
      shown.forEach(l => {
        const row = el('tr'), cell = el('td'), button = el('button', l.title); button.onclick = () => showLead(l); cell.append(button); row.append(cell, el('td', l.relationship_type), el('td', l.decision_state), el('td', l.test_execution)); $('lead-rows').append(row);
      });
    }
    $('lead-search').addEventListener('input', renderLeads); $('lead-state').addEventListener('change', renderLeads); renderLeads();
    graph.evidence.forEach(e => { const option = el('option', e.annotation_id); option.value = e.id; $('region-select').append(option); });
    function showRegion() {
      const evidence = graph.evidence.find(e => e.id === $('region-select').value), detail = $('region-detail');
      if (!evidence) return;
      detail.replaceChildren(el('h3', evidence.annotation_id), el('p', evidence.observation));
      if (evidence.literal_candidate) detail.append(el('p', 'Literal candidate: ' + evidence.literal_candidate));
      if (evidence.normalized_candidate) detail.append(el('p', 'Normalized identification: ' + evidence.normalized_candidate));
      link(detail, evidence.source_url, 'Institutional source image'); link(detail, evidence.target.source, 'Open retained original file');
      detail.append(el('p', 'SHA-256: ' + evidence.sha256));
      const image = entities.get(evidence.image), match = /^xywh=(\d+),(\d+),(\d+),(\d+)$/.exec(evidence.target.selector.value);
      if (image && match && localPath(image.path)) {
        const stage = el('div'), img = el('img'), box = el('span'); stage.className = 'region-stage'; img.src = localPath(image.path); img.alt = `Original manuscript photograph for ${evidence.annotation_id}; red box marks the cited region.`;
        const [x,y,w,h] = match.slice(1).map(Number), [iw,ih] = evidence.original_annotation.image_dimensions || [image.width,image.height];
        if (iw > 0 && ih > 0 && x+w <= iw && y+h <= ih) { box.className = 'region-box'; box.style.left = `${100*x/iw}%`; box.style.top = `${100*y/ih}%`; box.style.width = `${100*w/iw}%`; box.style.height = `${100*h/ih}%`; }
        stage.append(img, box); detail.append(stage);
      }
      raw(detail, evidence);
    }
    $('region-select').addEventListener('change', showRegion); showRegion();
    function showEntity() {
      const entity = entities.get($('entity-select').value), detail = $('entity-detail'); if (!entity) { detail.replaceChildren(el('p', 'No matching entity.')); return; }
      detail.replaceChildren(el('h3', `${entity.label} · ${entity.type}`)); raw(detail, entity, 'Entity and source-record mapping');
      const claims = graph.claims.filter(c => c.subject === entity.id || c.object === entity.id);
      detail.append(el('p', `${claims.length} related claims. These are attributed assertions and interpretations; no identity closure is performed.`));
      claims.forEach(c => { const d = el('details'); d.append(el('summary', `${c.predicate} · ${c.polarity} · ${c.status} · ${c.basis}`), el('pre', JSON.stringify(c,null,2))); c.provenance.forEach(p => link(d, entities.get(p.source)?.location, 'Claim source')); detail.append(d); });
    }
    function renderEntities() {
      const term = $('entity-search').value.toLowerCase(); $('entity-select').replaceChildren();
      graph.entities.filter(e => `${e.id} ${e.label}`.toLowerCase().includes(term)).forEach(e => { const o = el('option', `${e.type} · ${e.label} (${e.id})`); o.value = e.id; $('entity-select').append(o); }); showEntity();
    }
    $('entity-search').addEventListener('input', renderEntities); $('entity-select').addEventListener('change', showEntity); renderEntities();
    const preferred = register.leads.find(l => l.id === 'E33-numbering-conflict'); if (preferred) showLead(preferred);
  }).catch(error => { $('knowledge-status').textContent = 'Could not load the research overlay. Serve the project locally and build knowledge first. ' + error.message; });
}
