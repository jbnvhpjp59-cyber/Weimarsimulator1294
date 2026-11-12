#!/usr/bin/env node
// Runs after `dendrynexus make-html`: puts the compiled game and d3 next to
// index.html so that out/html/ is a complete, self-contained website.
'use strict';
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const html = path.join(root, 'out', 'html');
const copies = [
  [path.join(root, 'out', 'game.json'), path.join(html, 'game.json')],
  [path.join(root, 'node_modules', 'd3', 'dist', 'd3.min.js'), path.join(html, 'd3.v7.min.js')],
];
for (const [from, to] of copies) {
  fs.copyFileSync(from, to);
  console.log(`copied ${path.relative(root, from)} -> ${path.relative(root, to)}`);
}
