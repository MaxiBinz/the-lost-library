'use strict';
const assert = require('node:assert/strict');
const { escapeHTML, safeUrl, imageUrl, filterFragments, normalizeComponents, normalizeValidation, mergeConnections, captureOptions, rankLabel, buildRecordIndex } = require('../viewer/app.js');

assert.equal(escapeHTML('<script>"&'), '&lt;script&gt;&quot;&amp;');
assert.equal(safeUrl('javascript:alert(1)', true), '');
assert.equal(safeUrl('//example.org/image', true), '');
assert.equal(safeUrl('../data/images/a.jpg', true), '../data/images/a.jpg');
assert.equal(imageUrl({ image_path: 'data/images/a.jpg' }), '../data/images/a.jpg');
assert.equal(imageUrl({ image_path: 'data/images/a.jpg' }, 'data/images/b.jpg'), '../data/images/b.jpg');

const fragments = [
  { id: 'mpo-1', shelfmark: 'Fr 1', institution: 'Riksarkivet', collection: 'MPO', image_path: 'a.jpg', role: 'target', normalized: { type: 'Antiphonarium', contents: 'Mariae', origin: 'Åbo' } },
  { id: 'mpo-2', shelfmark: 'Fr 2', collection: 'MPO', image_path: null, role: 'control', normalized: { type: 'Graduale' } },
  { id: 'fm-1', shelfmark: 'F.m.IV.173', collection: 'Fragmenta', image_path: 'c.jpg', role: 'target', normalized: { type: 'Antiphonarium', contents: 'Te Deum' } }
];
assert.deepEqual(filterFragments(fragments, { imagesOnly: true }).map(f => f.id), ['mpo-1', 'fm-1']);
assert.deepEqual(filterFragments(fragments, { search: 'abo mariae', imagesOnly: true }).map(f => f.id), ['mpo-1']);
assert.deepEqual(filterFragments(fragments, { collection: 'MPO', role: 'control', imagesOnly: false }).map(f => f.id), ['mpo-2']);
assert.equal(filterFragments(fragments, { type: 'Graduale', imagesOnly: true }).length, 0);

const components = normalizeComponents({ components: [{ title: 'First continuity', items: [{ fragment_id: 'a', representative_image: true }, { missing: true }] }, { title: 'Other continuity', items: ['b'] }] });
assert.equal(components.length, 2);
assert.equal(components[0].items[1].missing, true);
assert.equal(components[1].items[0].fragment_id, 'b');
assert.equal(components[0].items[0].representative_image, true);
assert.deepEqual(normalizeComponents(null), []);

const validation = normalizeValidation({ selected_method: 'metadata', methods: [{ name: 'metadata', metrics: { precision_at_1: .5, recall_at_5: .8, mrr: .7, queries: 12 } }, { name: 'vision', metrics: { mrr: .6 } }] });
assert.equal(validation[0].selected, true);
assert.equal(validation[0].precision1, .5);
assert.equal(validation[0].queries, 12);
assert.equal(validation[1].precision1, null);
assert.equal(normalizeValidation({ methods: { simple: { hit_at_1: .25 } } })[0].hit1, .25);
console.log('Viewer data/escaping/filter/reconstruction/validation checks passed.');

const merged = mergeConnections([{ left_id: 'a', right_id: 'b', rank: 2, score: .8 }, { left_id: 'b', right_id: 'a', rank: 1, score: .8 }], [{ left_id: 'b', right_id: 'a', classification: 'C', textual_musical_evidence: { left: 'B contents', right: 'A contents' } }]);
assert.equal(merged.length, 1);
assert.equal(merged[0].left_id, 'b');
assert.equal(merged[0].textual_musical_evidence.left, 'B contents');
assert.equal(merged[0].rank_query_id, 'a');
console.log('Reciprocal-pair dossier orientation and rank-query check passed.');

const captureRecord = { image_path: 'a.jpg', image: { sha256: 'primary-hash' }, captures: [{ path: 'a.jpg', label: 'Image 1' }, { path: 'b.jpg', label: 'Manifest image 2', sha256: 'second-hash', capture_index: 1 }] };
assert.equal(captureOptions(captureRecord).length, 2);
assert.equal(captureOptions(captureRecord)[1].sha256, 'second-hash');
assert.equal(captureOptions(captureRecord, { image_path: 'verified.jpg', label: 'Verified source capture' })[2].path, 'verified.jpg');
assert.equal(captureOptions({ image_path: null }).length, 0);
console.log('Source-capture selection and provenance option checks passed.');

const comparisonSources = [{ id: 'uub-c23-0144', shelfmark: 'Uppsala C23, image144', image_path: 'data/comparison-images/c23-0144.jpg' }];
const sourceIndex = buildRecordIndex(fragments, comparisonSources);
assert.equal(sourceIndex.get('uub-c23-0144'), comparisonSources[0]);
assert.equal(sourceIndex.size, fragments.length + 1);
assert.equal(fragments.length, 3);
assert.equal(filterFragments(fragments, { search: 'Uppsala', imagesOnly: true }).length, 0);
assert.throws(() => buildRecordIndex(fragments, [{ id: 'mpo-1', image_path: 'unrelated.jpg' }]), /colliding/);
console.log('Separate comparison-source indexing and core-gallery isolation checks passed.');

const nestedValidation = { selection: { recommended_retrieval_method: 'metadata' }, results: { development: {}, test: { same_genre: { methods: { metadata: { book_macro: { 'precision@1': 1, 'precision@5': .95, 'recall@5': .95, 'mrr': 1 }, query_count: 24 }, embedding: { book_macro: { 'precision@5': .76, 'mrr': .97 }, query_count: 24 } } } } } };
const nestedRows = normalizeValidation(nestedValidation);
assert.equal(nestedRows.length, 2);
assert.equal(nestedRows[0].name, 'metadata');
assert.equal(nestedRows[0].precision5, .95);
assert.equal(nestedRows[0].queries, 24);
assert.equal(nestedRows[0].selected, true);
assert.equal(nestedRows[1].mrr, .97);
assert.equal(rankLabel({ rank: 1, rank_interval: [1, 40] }), 'Tie positions 1–40');
assert.equal(rankLabel({ rank: 1, rank_interval: [4, 4] }), 'Rank 4');
assert.equal(rankLabel({ rank: null }), '');
console.log('Nested real benchmark schema and tie-aware ranking checks passed.');

const { validRegion } = require('../viewer/app.js');
assert.equal(validRegion({region:[10,20,30,40],image_dimensions:[100,80]}),true);
assert.equal(validRegion({region:[90,20,30,40],image_dimensions:[100,80]}),false);
assert.equal(validRegion({region:[0,0,-1,10],image_dimensions:[100,80]}),false);
assert.equal(validRegion({region:['10',20,30,40],image_dimensions:[100,80]}),false);
const reviewBundle = require('../data/review_bundle.json');
assert.equal(reviewBundle.reviews.length,10);
assert.ok(reviewBundle.observations.every(validRegion));
assert.ok(reviewBundle.reviews.every(r=>r.new_discovery===false));
console.log('Frozen queue and source-region bounds checks passed.');
