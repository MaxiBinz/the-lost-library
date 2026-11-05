(function (global) {
  'use strict';

  const categoryNames = { A: 'Strong evidence', B: 'Plausible', C: 'Ambiguous', D: 'Rejected', E: 'Previously documented' };
  const state = { data: null, fragments: [], index: new Map(), selected: [], visible: 24, connectionsVisible: 12, filters: { search: '', collection: '', type: '', role: '', imagesOnly: true }, category: '' };

  function textOf(value) {
    if (value === undefined || value === null) return '';
    if (typeof value === 'object') return String(value.text || value.label || value.title || value.description || value.name || JSON.stringify(value));
    return String(value);
  }
  function esc(value) { return textOf(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
  function array(value) { return Array.isArray(value) ? value : value == null ? [] : [value]; }
  function safeUrl(value, allowRelative = false) {
    const url = textOf(value).trim();
    if (/^https?:\/\//i.test(url)) return url;
    if (allowRelative && url && !/^[a-z][a-z0-9+.-]*:/i.test(url) && !url.startsWith('//') && !url.includes('\\')) return url;
    return '';
  }
  function imageUrl(fragment, override) {
    const path = textOf(override || (fragment && fragment.image_path));
    if (!path) return '';
    if (/^https?:\/\//i.test(path)) return path;
    return safeUrl('../' + path.replace(/^\.\//, ''), true);
  }
  function fragmentType(fragment) { return textOf((fragment.normalized || {}).type || fragment.type || 'Type unrecorded'); }
  function fragmentTitle(fragment) { return textOf(fragment.shelfmark || fragment.id || 'Unidentified record'); }
  function normalizedSearch(fragment) {
    const n = fragment.normalized || {}, r = fragment.raw || {};
    return [fragment.id, fragment.shelfmark, fragment.institution, fragment.collection, fragment.role, n.type, n.contents, n.origin, n.script, n.notation, r.inhalt, r.entstehungsort].map(textOf).join(' ').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  }
  function filterFragments(fragments, filters) {
    const q = textOf(filters.search).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
    const terms = q.split(/\s+/).filter(Boolean);
    return fragments.filter(f => (!filters.imagesOnly || !!f.image_path) && (!filters.collection || textOf(f.collection) === filters.collection) && (!filters.type || fragmentType(f) === filters.type) && (!filters.role || textOf(f.role) === filters.role) && terms.every(t => normalizedSearch(f).includes(t)));
  }
  function normalizeComponents(reconstruction) {
    if (!reconstruction) return [];
    const components = array(reconstruction.components || reconstruction.groups || (reconstruction.sequence ? [{ title: 'Source-supported sequence', items: reconstruction.sequence }] : []));
    return components.map((component, i) => ({ ...component, title: component.title || component.label || `Component ${i + 1}`, items: array(component.items || component.sequence || component.fragments).map(item => typeof item === 'string' ? { fragment_id: item } : (item || { missing: true })) }));
  }
  function finite(value) { return value !== null && value !== '' && value !== undefined && Number.isFinite(Number(value)); }
  function number(value, digits = 3) { return finite(value) ? Number(value).toFixed(digits).replace(/0+$/, '').replace(/\.$/, '') : '—'; }
  function metricValue(object, keys) {
    for (const key of keys) if (finite(object && object[key])) return Number(object[key]);
    return null;
  }
  function selectedMethod(validation) { return textOf((validation.selection || {}).recommended_retrieval_method || validation.selected_method); }
  function validationFrame(validation) {
    const test = validation.results && validation.results.test;
    return test && (test.same_genre || test.all_genres) || null;
  }
  function normalizeValidation(validation) {
    const v = validation || {}, frame = validationFrame(v);
    const methods = (frame && frame.methods) || v.methods || v.method_results || (Array.isArray(v.results) ? v.results : []);
    const rows = Array.isArray(methods) ? methods : Object.entries(methods).map(([name, value]) => ({ name, ...value }));
    const chosen = selectedMethod(v);
    return rows.filter(row => row && typeof row === 'object').map(row => {
      const m = row.book_macro || row.metrics || row.test || row.macro || row;
      return { name: row.name || row.method || row.method_name || 'Unnamed method', precision1: metricValue(m, ['precision_at_1', 'precision@1', 'p_at_1', 'p1']), precision5: metricValue(m, ['precision_at_5', 'precision@5', 'p_at_5', 'p5']), recall5: metricValue(m, ['recall_at_5', 'recall@5', 'r_at_5', 'r5']), hit1: metricValue(m, ['hit_at_1', 'hit@1', 'hit1', 'top1']), hit5: metricValue(m, ['hit_at_5', 'hit@5', 'hit5', 'top5']), mrr: metricValue(m, ['mrr', 'mean_reciprocal_rank']), queries: row.query_count ?? m.queries ?? m.n_queries ?? row.queries ?? null, selected: !!row.selected || row.name === chosen || row.method === chosen };
    });
  }
  function rankLabel(record) {
    const interval = record.rank_interval;
    if (Array.isArray(interval) && interval.length >= 2 && finite(interval[0]) && finite(interval[1])) {
      return Number(interval[0]) === Number(interval[1]) ? `Rank ${Number(interval[0])}` : `Tie positions ${Number(interval[0])}–${Number(interval[1])}`;
    }
    return finite(record.rank) ? `Rank ${Number(record.rank)}` : '';
  }

  function mergeConnections(matches, suppliedDossiers) {
    const dossiers = array(suppliedDossiers), byPair = new Map();
    dossiers.forEach(d => { if (d.left_id && d.right_id) byPair.set([d.left_id, d.right_id].sort().join('|'), d); });
    const used = new Set(), records = [];
    array(matches).forEach(match => {
      const left = match.left_id || match.query_id || match.query, right = match.right_id || match.candidate_id || match.candidate;
      if (!left || !right || left === right) return;
      const key = [left, right].sort().join('|');
      if (used.has(key)) return;
      used.add(key);
      const d = byPair.get(key) || {};
      records.push({ ...match, ...d, left_id: d.left_id || left, right_id: d.right_id || right, rank_query_id: left, scores: match.scores || match.components || d.scores || {}, score: d.score ?? match.score });
    });
    dossiers.forEach(d => { const key = [d.left_id, d.right_id].sort().join('|'); if (d.left_id && d.right_id && !used.has(key)) { records.push(d); used.add(key); } });
    return records;
  }

  function captureOptions(fragment, override = {}) {
    const options = [], seen = new Set();
    function add(value) {
      if (!value || !value.path || seen.has(value.path)) return;
      seen.add(value.path);
      options.push({ ...value, label: value.label || `Source capture ${options.length + 1}` });
    }
    array(fragment.captures).forEach(add);
    if (fragment.image_path && !seen.has(fragment.image_path)) add({ path: fragment.image_path, ...(fragment.image || {}) });
    if (override.image_path && !seen.has(override.image_path)) add({ path: override.image_path, label: override.label || 'Sequence source capture', ...(override.image || {}) });
    return options;
  }

  function validRegion(observation) {
    const r = observation && observation.region, d = observation && observation.image_dimensions;
    return Array.isArray(r) && r.length === 4 && Array.isArray(d) && d.length === 2 &&
      [...r, ...d].every(x => typeof x === 'number' && Number.isFinite(x)) && r[0] >= 0 && r[1] >= 0 && r[2] > 0 && r[3] > 0 && r[0] + r[2] <= d[0] && r[1] + r[3] <= d[1];
  }
  function buildRecordIndex(fragments, comparisonSources) {
    const index = new Map();
    [...fragments, ...comparisonSources].forEach(record => {
      const id = textOf(record.id);
      if (!id || index.has(id)) throw new Error('Duplicate or colliding evidence source identifier.');
      index.set(id, record);
    });
    return index;
  }
  const pure = { escapeHTML: esc, safeUrl, imageUrl, filterFragments, normalizeComponents, normalizeValidation, normalizedSearch, mergeConnections, captureOptions, rankLabel, validRegion, buildRecordIndex };
  if (typeof module !== 'undefined' && module.exports) module.exports = pure;
  if (typeof document === 'undefined') return;

  const $ = selector => document.querySelector(selector);
  function link(url, label, className = '') { const u = safeUrl(url, true); return u ? `<a href="${esc(u)}" class="${esc(className)}"${/^https?:/i.test(u) ? ' target="_blank" rel="noopener noreferrer"' : ''}>${esc(label)}</a>` : esc(label); }
  function observationText(value) {
    if (value && typeof value === 'object' && value.signal) {
      const parts = [textOf(value.signal).replace(/_/g, ' ')];
      if (finite(value.compatibility)) parts.push(`compatibility ${number(value.compatibility)}`);
      if (finite(value.weight)) parts.push(`weight ${number(value.weight)}`);
      if (value.terms) parts.push(textOf(value.terms));
      return parts.join(' · ');
    }
    return textOf(value);
  }
  function list(items, emptyText) { const values = array(items).filter(x => textOf(x)); return values.length ? `<ul>${values.map(x => `<li>${esc(observationText(x))}</li>`).join('')}</ul>` : `<p>${esc(emptyText)}</p>`; }
  function statusTag(category, fallback = 'Not adjudicated') { const c = /^[A-E]$/.test(category) ? category : ''; return `<span class="status-tag ${c ? 'category-' + c.toLowerCase() : 'category-c'}">${c ? c + ' · ' + categoryNames[c] : fallback}</span>`; }
  function recordById(id) { return state.index.get(textOf(id)); }
  function lookupLabel(id) { const f = recordById(id); return f ? fragmentTitle(f) : textOf(id); }
  function dateLabel(f) {
    const n = f.normalized || {}, raw = (f.raw || {}).datierung;
    if (raw) return textOf(raw);
    return n.date_min && n.date_max ? `${n.date_min}–${n.date_max}` : textOf(f.date || 'Date unrecorded');
  }
  function unitLabel(f) { return textOf(f.image && (f.image.label || f.image.canvas_label) || f.capture_label || 'Source capture'); }

  function renderHero() {
    const project = state.data.project || {};
    if (project.description) $('#project-description').textContent = textOf(project.description);
    else if (project.research_target) $('#project-description').textContent = `Research target: ${textOf(project.research_target)}. ${project.reconstruction_target ? 'Demonstration: ' + textOf(project.reconstruction_target) + '.' : ''}`;
    if (project.edition || project.status) $('#edition-status').textContent = textOf(project.edition || project.status).toUpperCase();
    const preferred = project.hero_fragment_id && recordById(project.hero_fragment_id);
    const primary = preferred && preferred.image_path ? preferred : state.fragments.find(f => f.id === 'mpo-7957' && f.image_path) || state.fragments.find(f => f.image_path);
    if (!primary) return;
    const other = state.fragments.find(f => f.id === 'mpo-8994' && f.image_path && f.id !== primary.id) || state.fragments.find(f => f.image_path && f.id !== primary.id);
    $('#hero-manuscript').innerHTML = `${other ? `<div class="back-leaf" aria-hidden="true"><img src="${esc(imageUrl(other))}" alt=""></div>` : ''}<img src="${esc(imageUrl(primary))}" alt="Manuscript capture: ${esc(fragmentTitle(primary))}"><figcaption>${esc(fragmentTitle(primary))} · ${esc(primary.institution || primary.collection || 'SOURCE RECORD')}</figcaption>`;
  }
  function renderStats() {
    const s = state.data.stats || {};
    $('#stat-records').textContent = Number(s.imaged_fragments ?? new Set(state.fragments.filter(f => f.image_path).map(f => f.physical_object_id || f.id)).size).toLocaleString();
    $('#stat-images').textContent = Number(s.images ?? s.image_count ?? state.fragments.filter(f => f.image_path).length).toLocaleString();
    $('#stat-matches').textContent = Number(s.ranked_pairs ?? s.candidate_pairs ?? s.matches ?? array(state.data.matches).length).toLocaleString();
    $('#stat-components').textContent = Number(s.sequence_components ?? normalizeComponents(state.data.reconstruction).length).toLocaleString();
  }
  function fillOptions(selector, values, label) {
    const select = $(selector), previous = select.value;
    const unique = [...new Set(values.map(textOf).filter(Boolean))].sort((a, b) => a.localeCompare(b));
    select.innerHTML = `<option value="">${esc(label)}</option>` + unique.map(value => `<option value="${esc(value)}">${esc(value)}</option>`).join('');
    if (unique.includes(previous)) select.value = previous;
  }
  function renderFilters() {
    fillOptions('#collection-filter', state.fragments.map(f => f.collection), 'All collections');
    fillOptions('#type-filter', state.fragments.map(fragmentType), 'All manuscript types');
    fillOptions('#role-filter', state.fragments.map(f => f.role), 'All research roles');
  }
  function fragmentCard(f) {
    const n = f.normalized || {}, chosen = state.selected.includes(f.id), url = imageUrl(f), hasImage = !!url;
    return `<article class="fragment-card${chosen ? ' selected' : ''}" data-fragment-id="${esc(f.id)}"><button class="fragment-image-button" type="button" data-action="inspect" data-id="${esc(f.id)}" aria-label="Inspect ${esc(fragmentTitle(f))}">${hasImage ? `<img src="${esc(url)}" loading="lazy" alt="${esc(fragmentTitle(f))}, ${esc(unitLabel(f))}"><span class="capture-label">${esc(f.role || f.collection || 'SOURCE')}</span>` : '<span class="no-image">Image access<br>not established</span>'}</button><div class="fragment-card-body"><p class="collection-label">${esc(f.institution || f.collection)}</p><h3>${esc(fragmentTitle(f))}</h3><p class="fragment-type">${esc(fragmentType(f))} · ${esc(dateLabel(f))}</p><p class="fragment-contents">${esc(n.contents || (f.raw || {}).inhalt || 'Contents not recorded in the local metadata.')}</p></div><div class="fragment-card-actions"><button class="text-button" type="button" data-action="inspect" data-id="${esc(f.id)}">Inspect source ↗</button><button class="select-button" type="button" data-action="select" data-id="${esc(f.id)}" aria-pressed="${chosen}"><span class="select-square" aria-hidden="true">${chosen ? '✓' : ''}</span>${chosen ? 'Selected' : 'Compare'}</button></div></article>`;
  }
  function renderFragments() {
    const filtered = filterFragments(state.fragments, state.filters), shown = filtered.slice(0, state.visible);
    $('#fragment-grid').innerHTML = shown.length ? shown.map(fragmentCard).join('') : '<p class="empty-state">No records match these filters. Try another shelfmark or include records without images.</p>';
    $('#results-count').textContent = `${shown.length.toLocaleString()} of ${filtered.length.toLocaleString()} matching records · ${state.fragments.length.toLocaleString()} in the local sample`;
    $('#load-more').hidden = shown.length >= filtered.length;
    $('#load-more').textContent = `Show more records (${Math.min(24, filtered.length - shown.length)}) ↓`;
    renderTray();
  }
  function renderTray() {
    $('#compare-tray').hidden = !state.selected.length;
    $('#compare-selection').innerHTML = state.selected.map(id => { const f = recordById(id); return `<div class="selected-item">${f && f.image_path ? `<img src="${esc(imageUrl(f))}" alt="">` : ''}<span>${esc(f ? fragmentTitle(f) : id)}</span></div>`; }).join('<span aria-hidden="true">↔</span>') + (state.selected.length < 2 ? '<span class="selection-hint">Choose one more record</span>' : '');
    $('#open-compare').disabled = state.selected.length !== 2;
  }
  function toggleSelection(id) {
    if (!recordById(id)) return;
    if (state.selected.includes(id)) state.selected = state.selected.filter(x => x !== id);
    else state.selected = state.selected.length < 2 ? [...state.selected, id] : [state.selected[1], id];
    renderFragments();
  }
  function renderReconstruction() {
    const r = state.data.reconstruction || {}, components = normalizeComponents(r);
    if (r.title) $('#reconstruction-title').textContent = textOf(r.title);
    if (r.description || r.scope) $('#reconstruction-description').textContent = textOf(r.description || r.scope);
    if (r.note || r.uncertainty) $('#reconstruction-note p').textContent = textOf(r.note || r.uncertainty);
    $('#sequence-components').innerHTML = components.length ? components.map((c, ci) => {
      const pieces = c.items.map((item, i) => {
        if (item.missing || item.placeholder || item.kind === 'gap' || item.type === 'gap') return `<div class="sequence-page missing"><span class="missing-mark" aria-hidden="true">⋯</span><span class="sequence-label">${esc(item.label || 'Unpreserved or unknown')}</span><small>${esc(item.note || item.description || 'Position and extent are not established.')}</small></div>`;
        const f = recordById(item.fragment_id || item.id), url = imageUrl(f, item.image_path);
        const title = item.label || (f ? fragmentTitle(f) : item.fragment_id || item.id || 'Source record');
        const note = [item.side, item.representative_image ? 'Representative capture; exact side not verified' : '', item.note || item.description].filter(Boolean).map(textOf).join(' · ');
        return `<button class="sequence-page" type="button" data-action="sequence-inspect" data-component="${ci}" data-item="${i}"${!f ? ' disabled' : ''}>${url ? `<img src="${esc(url)}" loading="lazy" alt="${esc(title)}">` : '<span class="no-image">Source image unavailable</span>'}<span class="sequence-label">${esc(title)}</span><small>${esc(note || 'See the source record for image identity.')}</small></button>`;
      });
      let track = '';
      pieces.forEach((piece, i) => {
        if (i) { const previous = c.items[i - 1], current = c.items[i], isGap = previous.missing || previous.placeholder || current.missing || current.placeholder; track += `<div class="sequence-arrow" aria-hidden="true"><span>${isGap ? '⋯' : '→'}</span><small>${esc(isGap ? 'position unknown' : c.link_label || c.relationship || 'source-supported relation')}</small></div>`; }
        track += piece;
      });
      return `<article class="sequence-component"><div class="component-heading"><div><h3>${esc(c.title)}</h3>${c.description || c.note ? `<p>${esc(c.description || c.note)}</p>` : ''}</div>${statusTag(c.classification || (c.status === 'documented' ? 'E' : ''), textOf(c.status || 'Source-linked component'))}</div><div class="sequence-track">${track}</div>${c.source_url ? `<p class="matching-info">${link(c.source_url, c.source_label || 'Source for this component ↗')}</p>` : ''}</article>`;
    }).join('') : '<p class="empty-state">No defensible page sequence is supplied in this package. Explore the source records and candidate evidence below.</p>';
    renderMusic(r);
  }
  function renderMusic(reconstruction) {
    const m = reconstruction.music || reconstruction.audio || {};
    const audioUrl = safeUrl(m.audio_url || m.url, true);
    if (audioUrl && (m.verified === true || m.status === 'verified')) {
      $('#music-panel').innerHTML = `<div class="music-symbol" aria-hidden="true">𝄢</div><div><p class="eyebrow">THE MUSIC ON THE PAGE</p><h3>${esc(m.title || 'A source-linked musical transcription')}</h3><p>${esc(m.description || m.reason || '')}</p><audio controls preload="none" src="${esc(audioUrl)}">Your browser does not support audio playback.</audio>${m.source_url ? `<p class="source-links">${link(m.source_url, 'Transcription source and attribution ↗')}</p>` : ''}</div>`;
    } else if (m.reason || m.explanation || m.description) {
      $('#music-panel').innerHTML = `<div class="music-symbol" aria-hidden="true">𝄢</div><div><p class="eyebrow">THE MUSIC ON THE PAGE</p><h3>A score is also evidence.</h3><p>${esc(m.reason || m.explanation || m.description)}</p><span class="muted-label">No verified audio transcription supplied.</span></div>`;
    }
  }
  function connectionRecords() { return mergeConnections(state.data.matches, state.data.dossiers); }
  function sourceLinks(sources) {
    return array(sources).map((source, i) => { const url = typeof source === 'string' ? source : source.url || source.source_url || source.href; return url ? link(url, typeof source === 'string' ? `Source ${i + 1} ↗` : source.label || source.title || `Source ${i + 1} ↗`) : ''; }).filter(Boolean).join('');
  }
  function connectionCard(c) {
    const category = /^[A-E]$/.test(c.classification || c.category) ? (c.classification || c.category) : '';
    const supporting = c.supporting || c.evidence || c.supporting_evidence, against = c.against || c.contrary_evidence || c.cautions || c.warnings;
    const originality = textOf(c.originality || c.novelty || 'Originality not assessed');
    const signals = Object.entries(c.scores || {}).filter(([, value]) => finite(value));
    return `<article class="connection-card"><div class="connection-main"><div><div class="connection-names"><span>${esc(lookupLabel(c.left_id))}</span><span class="connection-link" aria-label="compared with">↔</span><span>${esc(lookupLabel(c.right_id))}</span></div><div class="connection-tags">${statusTag(category)}<span class="originality-label">${esc(originality)}</span>${rankLabel(c) ? `<span${Array.isArray(c.rank_interval) && c.rank_interval[1] > c.rank_interval[0] ? ' title="Equal compatibility scores; the displayed shortlist may cut off this tie."' : ''}>${esc(rankLabel(c))}${c.rank_query_id ? ' for ' + esc(lookupLabel(c.rank_query_id)) : ''}</span>` : ''}</div></div><div class="connection-actions"><div class="connection-score">${number(c.score)}<small>COMPATIBILITY · NOT PROBABILITY</small></div><button class="button secondary" type="button" data-action="compare-pair" data-left="${esc(c.left_id)}" data-right="${esc(c.right_id)}">Compare ↔</button></div></div><details><summary>${esc(c.title || 'Read the evidence and limitations')}</summary><div class="connection-evidence">${c.summary || c.description ? `<p>${esc(c.summary || c.description)}</p>` : ''}${signals.length ? `<div class="signal-bars">${signals.map(([key, value]) => `<div class="signal-bar"><span>${esc(key.replace(/_/g, ' '))}<b>${number(value, 2)}</b></span><i><b style="width:${Math.max(0, Math.min(100, Number(value) * 100))}%"></b></i></div>`).join('')}</div>` : ''}<div class="evidence-columns"><div><h4>Supporting observations</h4>${list(supporting, 'No independent supporting observations are recorded for this suggestion.')}</div><div><h4>Contrary evidence & limits</h4>${list(against, 'No contradiction is recorded here. That is not evidence that the pair belongs together.')}</div></div>${c.textual_musical_evidence ? `<div class="textual-evidence"><h4>Textual & musical evidence</h4>${c.textual_musical_evidence.left ? `<p><strong>${esc(lookupLabel(c.left_id))}:</strong> ${esc(c.textual_musical_evidence.left)}</p>` : ''}${c.textual_musical_evidence.right ? `<p><strong>${esc(lookupLabel(c.right_id))}:</strong> ${esc(c.textual_musical_evidence.right)}</p>` : ''}${c.textual_musical_evidence.interpretation ? `<p>${esc(c.textual_musical_evidence.interpretation)}</p>` : ''}</div>` : ''}${c.alternatives ? `<h4>Alternative explanations</h4>${list(c.alternatives, '')}` : ''}${c.expert_verification || c.expert_verification_needed || c.next_step ? `<p class="connection-explanation"><strong>Verification needed:</strong> ${esc(c.expert_verification || c.expert_verification_needed || c.next_step)}</p>` : ''}<div class="source-links">${sourceLinks(c.sources || c.source_urls)}</div></div></details></article>`;
  }
  function renderConnections() {
    const records = connectionRecords().filter(c => !state.category || (c.classification || c.category || 'C') === state.category), visible = records.slice(0, state.connectionsVisible);
    $('#connections-list').innerHTML = visible.length ? visible.map(connectionCard).join('') : '<p class="empty-state">No connection records match this category. An unreviewed retrieval suggestion is not a confirmed relationship.</p>';
    $('#more-connections').hidden = visible.length >= records.length;
    $('#more-connections').textContent = `Show more connections (${records.length - visible.length} remaining) ↓`;
  }
  function renderValidation() {
    const v = state.data.validation || {}, rows = normalizeValidation(v), frame = validationFrame(v), chosen = selectedMethod(v);
    const selected = rows.find(row => row.selected), selectedThreshold = (v.thresholds || {})[chosen] || {};
    const confusion = selectedThreshold.test_confusion_catalogue_labels;
    const summary = [];
    if (chosen) summary.push({ value: chosen.replace(/_/g, ' '), label: 'SELECTED RETRIEVAL METHOD' });
    const queryCount = selected && selected.queries || v.test_queries || v.query_count || v.queries;
    if (queryCount) summary.push({ value: queryCount, label: 'HELD-OUT TEST QUERIES' });
    const books = frame && (frame.reference_book_count || frame.book_count) || v.test_codices || v.book_count || v.codices;
    if (books) summary.push({ value: books, label: 'TEST REFERENCE BOOK GROUPS' });
    if (confusion && finite(confusion.fp) && finite(confusion.tn)) summary.push({ value: `${confusion.fp} / ${Number(confusion.fp) + Number(confusion.tn)}`, label: 'THRESHOLD FALSE ACCEPTS · CATALOGUE TEST PAIRS' });
    $('#validation-summary').innerHTML = summary.map(x => `<div><strong>${esc(x.value)}</strong><span>${esc(x.label)}</span></div>`).join('');
    if (rows.length) {
      const columns = [['Method', 'name'], ['P@1', 'precision1'], ['P@5', 'precision5'], ['Recall@5', 'recall5'], ['Hit@1', 'hit1'], ['Hit@5', 'hit5'], ['MRR', 'mrr'], ['Queries', 'queries']];
      $('#validation-table-wrap').innerHTML = `<table><caption class="sr-only">Measured held-out test retrieval, same-genre gallery where supplied, macro-averaged over catalogue book groups. Missing metrics are shown as a dash.</caption><thead><tr>${columns.map(([title]) => `<th scope="col">${title}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr${row.selected ? ' class="best-method"' : ''}>${columns.map(([, key], i) => `<${i ? 'td' : 'th'}${i ? '' : ' scope="row"'}>${i ? key === 'queries' ? esc(row[key] ?? '—') : number(row[key]) : esc(row[key]).replace(/_/g, ' ')}</${i ? 'td' : 'th'}>`).join('')}</tr>`).join('')}</tbody></table>`;
    } else $('#validation-table-wrap').innerHTML = '<p class="empty-state">No machine-readable benchmark table is supplied. No numerical accuracy is inferred from the manuscript images.</p>';
    const negatives = array(v.literature_controls).filter(c => c.label === 'negative' && c.evaluable), notes = [];
    if (frame) notes.push('Table scope: held-out book partition of an exploratory pilot, same-genre gallery, macro-average over reference book groups. This evaluation has already been inspected; it is not a new untouched confirmation. Rates are fractions: P@5 of 0.95 describes reference-labelled retrieval in this selected benchmark, not a 95% probability that an unknown pair belongs together.');
    if (confusion) notes.push(`Selected threshold ${number(selectedThreshold.threshold)}: ${confusion.tp} true accepts, ${confusion.fp} false accepts, ${confusion.fn} missed positives and ${confusion.tn} true rejects against provisional catalogue labels. Pair-threshold performance and top-k ranking measure different things.`);
    notes.push(...[v.description || v.scope, v.label_source || v.ground_truth_note, ...array(v.limitations), ...array(v.notes)].filter(Boolean));
    let warning = negatives.map(c => {
      const methods = Object.values(c.methods || {}), accepts = methods.filter(m => m.accepted_at_catalogue_calibration_threshold === true).length, test = (c.methods || {})[chosen] || {};
      return `<div class="validation-warning"><p class="eyebrow">THE IMPORTANT WRONG ANSWER</p><h3>${esc(lookupLabel(c.left_id))} ↔ ${esc(lookupLabel(c.right_id))}</h3><p>This published different-book comparison was ${test.accepted_at_catalogue_calibration_threshold ? '<strong>falsely accepted</strong>' : 'not accepted'} by the selected method at its catalogue-calibrated threshold. ${accepts} of ${methods.length} evaluated methods accepted it. Strong retrieval scores therefore do not justify a manuscript attribution.</p>${c.source ? `<p>${link(c.source, 'Read the published comparison ↗')}</p>` : ''}</div>`;
    }).join('');
    const strata = Object.entries(v.hard_negative_strata || {});
    if (strata.length) warning += `<details class="negative-strata"><summary>Inspect catalogue-derived difficult-negative strata</summary><table><thead><tr><th>Comparison stratum</th><th>Pairs</th><th>False accepts</th></tr></thead><tbody>${strata.map(([name, item]) => `<tr><th scope="row">${esc(name.replace(/_/g, ' '))}</th><td>${esc(item.pairs ?? '—')}</td><td>${esc(item.false_acceptances_at_selected_threshold ?? '—')}</td></tr>`).join('')}</tbody></table><p>Strata can overlap. Distinct catalogue book IDs are provisional references, not independently adjudicated book or scribe separation.</p></details>`;
    $('#validation-notes').innerHTML = warning + (notes.length ? notes.map(note => `<p>${esc(note)}</p>`).join('') : '<p><strong>Interpretation:</strong> a compatibility ranking is a research aid. It does not establish a book identity or the originality of a relationship.</p>');
  }
  function renderSources() {
    const project = state.data.project || {}, sources = array(state.data.sources);
    const story = project.story || state.data.story;
    if (story) $('#story').innerHTML = array(story).map(p => typeof p === 'object' ? `${p.title ? `<h4>${esc(p.title)}</h4>` : ''}<p>${esc(p.text || p.description || '')}</p>` : `<p>${esc(p)}</p>`).join('');
    $('#source-list').innerHTML = sources.map((source, i) => {
      const s = typeof source === 'string' ? { url: source, title: source } : source;
      return `<div class="source-item"><span class="source-number">${String(i + 1).padStart(2, '0')}</span><div>${link(s.url || s.source_url, s.title || s.label || s.name || 'Source record')}${s.description || s.license ? `<span>${esc(s.description || s.license)}</span>` : ''}</div></div>`;
    }).join('');
    const limitations = array(state.data.limitations).filter(Boolean);
    if (limitations.length) $('#limitations-list').innerHTML = limitations.map(x => `<li>${esc(x)}</li>`).join('');
    const institutions = [...new Set(state.fragments.map(f => f.institution || f.attribution).filter(Boolean))];
    $('#credits').textContent = `Images and catalogue evidence: ${institutions.join('; ') || 'see individual source records'}. Each record preserves its source link, credit and rights statement. Image rights and metadata licences may differ. Local analysis does not replace source catalogues or specialist judgment.`;
  }

  function renderEvidenceReview() {
    const bundle = state.data.evidence_review || {}, reviews = array(bundle.reviews), checks = array(bundle.context_checks);
    function regions(observations) {
      return `<div class="region-buttons">${array(observations).filter(validRegion).map(o => `<button class="button secondary" type="button" data-action="inspect-region" data-observation="${esc(o.id)}">Inspect region · ${esc(o.fragment_id)} · ${esc(o.id)}</button>`).join('')}</div>`;
    }
    function sources(urls) {
      return `<p class="review-sources">${array(urls).map((u, i) => {
        const path = textOf(u), local = /^(data|research)\//.test(path) || /^[^/?#]+\.md(?:[?#]|$)/i.test(path);
        return link(local ? '../' + path : path, `Source ${i + 1} ↗`);
      }).join(' · ')}</p>`;
    }
    const cases = reviews.length ? `<div class="review-intro"><p class="eyebrow">THE FROZEN RESEARCH QUEUE</p><h3>Ten comparisons. Every outcome visible.</h3><p>These are local AI-assisted source screens. No independent expert has adjudicated them. Known scholarly decisions are reference evidence; unresolved cases remain unresolved.</p><p>${link('../data/review_bundle.json', 'Download complete evidence JSON ↗')} · ${link('../EVIDENCE_DOSSIERS.md', 'Read all ten dossiers ↗')} · ${link('../LAST_SHOT_CHECKPOINT.md', 'Read the final research checkpoint ↗')}</p></div>` + reviews.map(r => `<article class="evidence-case"><details><summary><span>${esc(r.id)} · ${esc(lookupLabel(r.left_id))} ↔ ${esc(lookupLabel(r.right_id))}</span>${statusTag(r.classification)}</summary><div class="review-body"><p><strong>Question:</strong> ${esc(r.question)}</p><p><strong>Prior status:</strong> ${esc(r.prior_status)}</p><p><strong>Observations:</strong> ${esc(array(r.supporting).join(' '))}</p><p><strong>Against / alternatives:</strong> ${esc(array(r.against).join(' '))}</p><p><strong>Falsification:</strong> ${esc(r.falsification_test)}</p><p><strong>Outcome:</strong> ${esc(r.outcome)}</p><p><strong>Next evidence:</strong> ${esc(r.next_evidence_needed)}</p><p>${esc(r.originality)}. ${esc(r.review_state)}.</p>${regions(r.observations)}${sources(r.sources)}</div></details></article>`).join('') : '';
    const supporting = checks.length ? `<div class="review-intro"><p class="eyebrow">SUPPORTING SOURCE CHECKS</p><h3>Evidence about the sources and methods.</h3><p>These checks support the investigation. They are separate from the ten frozen comparisons and do not add new manuscript attributions.</p></div>` + checks.map(c => `<article class="evidence-case"><details><summary><span>${esc(c.id)} · ${esc(c.title)}</span></summary><div class="review-body"><p>${esc(c.summary)}</p><p><strong>Records:</strong> ${esc(array(c.record_ids).map(lookupLabel).join(' · '))}</p><p><strong>Outcome:</strong> ${esc(c.outcome)}</p><p><strong>Limits:</strong> ${esc(array(c.limits).join(' '))}</p>${regions(c.observations)}${sources(c.sources)}</div></details></article>`).join('') : '';
    $('#evidence-review').innerHTML = cases + supporting;
  }

  function regionFocus(observation, url) {
    if (!validRegion(observation)) return '';
    const [x, y, w, h] = observation.region, [iw, ih] = observation.image_dimensions;
    const reading = observation.reading;
    return `<div class="region-focus"><p class="eyebrow">SOURCE REGION · ${esc(observation.id)} · ${[x,y,w,h].join(', ')} PIXELS</p><div class="region-cutout" style="aspect-ratio:${w}/${h}"><img src="${esc(url)}" alt="Selected evidence region from ${esc(observation.fragment_id)}" style="width:${iw / w * 100}%;height:${ih / h * 100}%;left:${-x / w * 100}%;top:${-y / h * 100}%"></div><p>${esc(observation.body.value)}</p>${reading ? `<p><strong>Provisional reading:</strong> ${esc(reading.literal_candidate)}<br><strong>Normalized search:</strong> ${esc(reading.normalized_search_text)}${reading.cantus_candidate ? `<br><strong>Candidate Cantus ID:</strong> ${esc(reading.cantus_candidate.id)}` : ''}</p>` : ''}<p>${esc(observation.verification)}. This crop selects existing pixels; no detail is generated. The complete capture and provenance follow below.</p>${reading ? array(reading.external_references).map((u, i) => link(u, `Chant reference ${i+1} ↗`)).join(' · ') : ''}</div>`;
  }

  function metadataRows(f) {
    const n = f.normalized || {}, image = f.image || {};
    const dimensions = values => Array.isArray(values) && values.some(finite) ? values.map(v => finite(v) ? v : '?').join(' × ') + ' cm (catalogue)' : 'Not recorded';
    return [
      ['Shelfmark', esc(fragmentTitle(f))], ['Institution', esc(f.institution || 'Unverified')], ['Collection', esc(f.collection || 'Unrecorded')], ['Type / date', esc(fragmentType(f) + ' · ' + dateLabel(f))],
      ['Contents', esc(n.contents || (f.raw || {}).inhalt || 'Not recorded')], ['Origin / use', esc(n.origin || (f.raw || {}).entstehungsort || 'Uncertain or unrecorded')],
      ['Leaf / written space', esc(dimensions(n.leaf_cm) + ' / ' + dimensions(n.written_cm))], ['Script / notation', esc([n.script, n.notation].filter(Boolean).join(' · ') || 'Not recorded')],
      ['Image capture', esc([unitLabel(f), image.width && image.height ? `${image.width} × ${image.height} pixels` : ''].filter(Boolean).join(' · '))],
      ['Credit', esc(f.attribution || f.institution || 'See source record')], ['Usage rights', f.rights_url ? link(f.rights_url, f.rights_label || f.rights_url) : 'Rights statement unavailable — do not infer permission'],
      ['Source record', f.source_url ? link(f.source_url, 'Open institutional record ↗') : 'No verified URL supplied'], ['IIIF manifest', f.manifest_url ? link(f.manifest_url, 'Open source manifest ↗') : 'Not available / not verified'],
      ['Image provenance', image.url ? link(image.url, 'Original image endpoint ↗') : 'See source record'], ['SHA-256', esc(image.sha256 || 'Not supplied')]
    ];
  }
  function inspectionPane(f, index, override = {}) {
    const options = captureOptions(f, override), preferred = override.image_path || f.image_path;
    const selectedIndex = Math.max(0, options.findIndex(c => c.path === preferred)), capture = options[selectedIndex];
    const view = capture ? { ...f, image_path: capture.path, image: capture, rights_url: capture.rights_url || f.rights_url } : f;
    const url = imageUrl(view), warnings = [...array(f.warnings), ...(override.representative_image ? ['Representative capture: its exact side is not verified. Do not read this displayed capture as the named sequence side.'] : []), ...(override.note ? [override.note] : [])];
    return `<section class="inspect-pane" data-pane="${index}" data-record-id="${esc(f.id)}"><h3 class="inspect-heading">${esc(override.label || fragmentTitle(f))}</h3><p class="inspect-origin">${esc(f.institution || f.collection)}${override.side ? ' · ' + esc(override.side) : ''}</p><div class="image-tools">${options.length > 1 ? `<label class="capture-picker"><span>Capture</span><select data-action="capture-select" data-pane="${index}" aria-label="Choose source capture for ${esc(fragmentTitle(f))}">${options.map((c, i) => `<option value="${i}"${i === selectedIndex ? ' selected' : ''}>${esc(c.label)}</option>`).join('')}</select></label>` : ''}<button type="button" data-action="zoom-out" data-pane="${index}" aria-label="Zoom out ${esc(fragmentTitle(f))}">−</button><span class="zoom-level" data-zoom-level="${index}">100%</span><button type="button" data-action="zoom-in" data-pane="${index}" aria-label="Zoom in ${esc(fragmentTitle(f))}">+</button><button type="button" data-action="rotate" data-pane="${index}">Rotate ↻</button><button type="button" data-action="reset-image" data-pane="${index}">Reset view</button><span data-capture-link="${index}">${url ? link(url, 'Open capture ↗') : ''}</span></div><p class="capture-note">Capture ordinals identify source photographs, not medieval folio sides or page order.</p><div class="image-viewport" data-viewport="${index}" tabindex="0" aria-label="Manuscript image; scroll to inspect when zoomed">${url ? `<div class="image-stage"><img src="${esc(url)}" alt="${esc(override.label || fragmentTitle(f))}, ${esc(capture ? capture.label : 'source capture')}" data-zoom="1" data-rotation="0"></div>` : '<p class="no-image">No image has been verified for this record.</p>'}</div>${warnings.length ? `<div class="record-warnings">${warnings.map(x => `<p>${esc(x)}</p>`).join('')}</div>` : ''}<table class="metadata-table"><caption class="sr-only">Source and provenance for ${esc(fragmentTitle(f))}</caption><tbody>${metadataRows(view).map(([label, value]) => `<tr><th scope="row">${label}</th><td>${value}</td></tr>`).join('')}</tbody></table></section>`;
  }
  function selectCapture(select) {
    const pane = select.closest('.inspect-pane'), f = pane && recordById(pane.dataset.recordId);
    if (!f) return;
    const capture = (pane._captureOptions || captureOptions(f))[Number(select.value)];
    if (!capture) return;
    const focusedRegion = pane.querySelector('.region-focus');
    if (focusedRegion) focusedRegion.remove();
    const view = { ...f, image_path: capture.path, image: capture, rights_url: capture.rights_url || f.rights_url };
    const img = pane.querySelector('.image-viewport img');
    if (!img) return;
    img.dataset.zoom = '1'; img.dataset.rotation = '0';
    img.src = imageUrl(view); img.alt = `${fragmentTitle(f)}, ${capture.label}`;
    const zoomLabel = pane.querySelector('.zoom-level');
    if (zoomLabel) zoomLabel.textContent = '100%';
    pane.querySelector('.metadata-table tbody').innerHTML = metadataRows(view).map(([label, value]) => `<tr><th scope="row">${label}</th><td>${value}</td></tr>`).join('');
    pane.querySelector('[data-capture-link]').innerHTML = link(imageUrl(view), 'Open capture ↗');
    requestAnimationFrame(() => updateImageView(img));
  }
  function openRecords(ids, overrides = []) {
    const records = ids.map(recordById).filter(Boolean);
    if (!records.length) return;
    const dialog = $('#image-dialog');
    $('#dialog-title').textContent = records.length > 1 ? 'Read the pages side by side.' : 'Inspect the source.';
    $('#dialog-eyebrow').textContent = records.length > 1 ? 'COMPARE ACTUAL MANUSCRIPT CAPTURES' : 'MANUSCRIPT CAPTURE & PROVENANCE';
    $('#dialog-content').innerHTML = `<div class="inspect-grid${records.length > 1 ? ' compare' : ''}">${records.map((f, i) => inspectionPane(f, i, overrides[i] || {})).join('')}</div>`;
    overrides.forEach((override, i) => {
      if (!override.observation) return;
      const pane = dialog.querySelectorAll('.inspect-pane')[i];
      if (pane) pane.querySelector('.image-tools').insertAdjacentHTML('beforebegin', regionFocus(override.observation, imageUrl(records[i], override.image_path)));
    });
    dialog.querySelectorAll('.inspect-pane').forEach((pane, i) => { pane._captureOptions = captureOptions(records[i], overrides[i] || {}); });
    if (!dialog.open) dialog.showModal();
    requestAnimationFrame(() => dialog.querySelectorAll('.image-stage img').forEach(img => updateImageView(img)));
  }
  function updateImageView(img) {
    if (!img.naturalWidth || !img.naturalHeight) return;
    const viewport = img.closest('.image-viewport'), stage = img.parentElement;
    if (!viewport || !stage) return;
    const zoom = Number(img.dataset.zoom || 1), rotation = Number(img.dataset.rotation || 0);
    const width = viewport.clientWidth, height = viewport.clientHeight;
    const ratio = Math.min(Math.max(1, width - 28) / img.naturalWidth, Math.max(1, height - 28) / img.naturalHeight);
    const baseWidth = img.naturalWidth * ratio, baseHeight = img.naturalHeight * ratio;
    const turned = rotation % 180 !== 0;
    stage.style.width = Math.max(width, (turned ? baseHeight : baseWidth) * zoom + 28) + 'px';
    stage.style.height = Math.max(height, (turned ? baseWidth : baseHeight) * zoom + 28) + 'px';
    img.style.width = baseWidth + 'px';
    img.style.height = baseHeight + 'px';
    img.style.transform = `translate(-50%, -50%) rotate(${rotation}deg) scale(${zoom})`;
    viewport.scrollLeft = (stage.offsetWidth - width) / 2;
    viewport.scrollTop = (stage.offsetHeight - height) / 2;
  }
  function imageTool(action, pane) {
    const viewport = document.querySelector(`[data-viewport="${Number(pane)}"]`), img = viewport && viewport.querySelector('img');
    if (!img) return;
    let zoom = Number(img.dataset.zoom || 1), rotation = Number(img.dataset.rotation || 0);
    if (action === 'zoom-in') zoom = Math.min(4, zoom + .25);
    if (action === 'zoom-out') zoom = Math.max(.5, zoom - .25);
    if (action === 'rotate') rotation = (rotation + 90) % 360;
    if (action === 'reset-image') { zoom = 1; rotation = 0; }
    img.dataset.zoom = String(zoom); img.dataset.rotation = String(rotation);
    updateImageView(img);
    const label = document.querySelector(`[data-zoom-level="${Number(pane)}"]`);
    if (label) label.textContent = `${Math.round(zoom * 100)}%`;
  }
  function setData(data) {
    if (!data || typeof data !== 'object') throw new Error('Research data must be a JSON object.');
    state.data = data;
    state.fragments = array(data.fragments).filter(f => f && typeof f === 'object' && f.id);
    const comparisonSources = array(data.comparison_sources).filter(f => f && typeof f === 'object' && f.id);
    state.index = buildRecordIndex(state.fragments, comparisonSources);
    state.selected = state.selected.filter(id => state.index.has(id));
    renderHero(); renderStats(); renderFilters(); renderReconstruction(); renderFragments(); renderConnections(); renderValidation(); renderSources(); renderEvidenceReview();
    $('#load-status').className = 'load-status loaded';
    $('#load-status').textContent = `${state.fragments.length} source records loaded.`;
  }
  function readFilters() {
    state.filters = { search: $('#search').value, collection: $('#collection-filter').value, type: $('#type-filter').value, role: $('#role-filter').value, imagesOnly: $('#images-only').checked };
    state.visible = 24; renderFragments();
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-action]');
    if (!button) return;
    const action = button.dataset.action;
    if (action === 'inspect') openRecords([button.dataset.id]);
    if (action === 'inspect-region') {
      const observation = array((state.data.evidence_review || {}).observations).find(o => o.id === button.dataset.observation);
      if (observation) openRecords([observation.fragment_id], [{ image_path: observation.target.source, observation, note: 'Evidence region is an AI observation, not independent expert verification.' }]);
    }
    if (action === 'select') toggleSelection(button.dataset.id);
    if (action === 'compare-pair') openRecords([button.dataset.left, button.dataset.right]);
    if (action === 'sequence-inspect') {
      const component = normalizeComponents(state.data.reconstruction)[Number(button.dataset.component)], item = component && component.items[Number(button.dataset.item)];
      if (item) openRecords([item.fragment_id || item.id], [item]);
    }
    if (['zoom-in', 'zoom-out', 'rotate', 'reset-image'].includes(action)) imageTool(action, button.dataset.pane);
  });
  $('#image-dialog').addEventListener('change', event => { if (event.target.matches('[data-action="capture-select"]')) selectCapture(event.target); });
  $('#filters').addEventListener('submit', event => event.preventDefault());
  $('#filters').addEventListener('input', readFilters);
  $('#filters').addEventListener('change', readFilters);
  $('#filters').addEventListener('reset', () => setTimeout(readFilters, 0));
  $('#load-more').addEventListener('click', () => { state.visible += 24; renderFragments(); });
  $('#more-connections').addEventListener('click', () => { state.connectionsVisible += 12; renderConnections(); });
  $('#evidence-filter').addEventListener('change', event => { state.category = event.target.value; state.connectionsVisible = 12; renderConnections(); });
  $('#clear-compare').addEventListener('click', () => { state.selected = []; renderFragments(); });
  $('#open-compare').addEventListener('click', () => openRecords(state.selected));
  $('.dialog-close').addEventListener('click', () => $('#image-dialog').close());
  $('#image-dialog').addEventListener('click', event => { if (event.target === $('#image-dialog')) { const bounds = event.target.getBoundingClientRect(); if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) event.target.close(); } });
  document.addEventListener('load', event => { if (event.target.tagName === 'IMG' && event.target.closest('.image-stage')) updateImageView(event.target); }, true);
  global.addEventListener('resize', () => { if ($('#image-dialog').open) $('#image-dialog').querySelectorAll('.image-stage img').forEach(img => updateImageView(img)); });
  document.addEventListener('error', event => { if (event.target.tagName === 'IMG') { event.target.alt = 'Image unavailable locally — inspect the source record for access details.'; event.target.classList.add('failed-image'); } }, true);
  if ('IntersectionObserver' in global) {
    const observer = new IntersectionObserver(entries => { const visible = entries.filter(e => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0]; if (visible) document.querySelectorAll('.nav-link').forEach(a => a.classList.toggle('active', a.hash === '#' + visible.target.id)); }, { rootMargin: '-10% 0px -50% 0px', threshold: [0, .1, .3, .5] });
    document.querySelectorAll('main section[id]').forEach(section => observer.observe(section));
  }
  global.LostLibrary = { ...pure, setData, openRecords, getState: () => ({ loaded: !!state.data, records: state.fragments.length, selected: [...state.selected], filters: { ...state.filters }, components: state.data ? normalizeComponents(state.data.reconstruction).length : 0, connections: state.data ? connectionRecords().length : 0 }) };
  fetch('../data/site.json', { cache: 'no-cache' }).then(response => { if (!response.ok) throw new Error(`Research data request returned HTTP ${response.status}.`); return response.json(); }).then(setData).catch(error => { $('#load-status').className = 'load-status error'; $('#load-status').textContent = `${error.message} Run the local research pipeline/export, then refresh this page. This viewer must be served over localhost rather than opened as a file.`; });
})(typeof window !== 'undefined' ? window : globalThis);
