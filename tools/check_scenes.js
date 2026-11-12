#!/usr/bin/env node
// Static checks for the .dry scene files. No dependencies.
//
//   node tools/check_scenes.js
//
// Checks:
//   - every "- @scene" choice, go-to, call and set-jump target exists
//   - every "- #tag" choice has at least one scene with that tag
//   - every "[+ x : qdisplay +]" names an existing qdisplay
//   - every {! ... !} JavaScript block compiles
//   - [? ?], [+ +] and {! !} are balanced; no stray "[" (which Dendry
//     treats as a hidden block)
//   - variables that are read or incremented are initialised somewhere
//
// Exit code 1 if there are errors. Warnings don't fail the check.

'use strict';
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const sceneDir = path.join(root, 'source', 'scenes');
const qdisplayDir = path.join(root, 'source', 'qdisplays');

const errors = [];
const warnings = [];
const err = (where, msg) => errors.push(`${where}: ${msg}`);
const warn = (where, msg) => warnings.push(`${where}: ${msg}`);

function walk(dir) {
  let out = [];
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    if (fs.statSync(p).isDirectory()) {
      out = out.concat(walk(p));
    } else if (name.endsWith('.scene.dry')) {
      out.push(p);
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// Parse scene files into sections
// ---------------------------------------------------------------------------
const scenes = {};      // id -> {file, line, props, content: [{text, line}]}
const sceneFiles = walk(sceneDir);

for (const file of sceneFiles) {
  const base = path.basename(file).replace(/\.scene\.dry$/, '');
  const rel = path.relative(root, file);
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  let current = {id: base, file: rel, line: 1, props: {}, content: [], base};
  scenes[base] = current;
  let inProps = true;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const header = line.match(/^@(\S+)\s*$/);
    if (header) {
      if (header[1] === base) {
        err(`${rel}:${i + 1}`, `section can't use the file id "${base}"`);
      }
      const id = base + '.' + header[1];
      if (scenes[id]) {
        err(`${rel}:${i + 1}`, `duplicate section @${header[1]}`);
      }
      current = {id, file: rel, line: i + 1, props: {}, content: [], base};
      scenes[id] = current;
      inProps = true;
      continue;
    }
    if (inProps) {
      if (line.trim() === '') {
        inProps = false;
        continue;
      }
      const prop = line.match(/^([a-z][a-z-]*):\s*(.*)$/);
      if (prop) {
        let value = prop[2];
        if (value.startsWith('{!')) {
          // multi-line magic: read until a line that ends the block
          const start = i;
          const block = [value.slice(2)];
          while (!/!\}\s*$/.test(lines[i]) || (i === start && value.trim() === '{!')) {
            i++;
            if (i >= lines.length) {
              err(`${rel}:${start + 1}`, `unterminated {! block in ${prop[1]}`);
              break;
            }
            block.push(lines[i]);
          }
          let src = block.join('\n');
          src = src.replace(/!\}\s*$/, '');
          current.props[prop[1]] = {magic: src, line: start + 1};
        } else {
          current.props[prop[1]] = {text: value, line: i + 1};
        }
        continue;
      }
      // not a property: content begins without a blank line
      inProps = false;
    }
    current.content.push({text: line, line: i + 1});
  }
}

// ---------------------------------------------------------------------------
// Reference resolution
// ---------------------------------------------------------------------------
const SPECIAL = new Set(['jumpScene', 'backSpecialScene', 'prevScene', 'prevTopScene']);
function resolve(fromScene, ref) {
  if (SPECIAL.has(ref)) {
    return ref;
  }
  const local = fromScene.base + '.' + ref;
  if (scenes[local]) {
    return local;
  }
  if (scenes[ref]) {
    return ref;
  }
  return null;
}

const tags = {};
for (const s of Object.values(scenes)) {
  if (s.props.tags) {
    for (const t of s.props.tags.text.split(',').map(x => x.trim()).filter(Boolean)) {
      (tags[t] = tags[t] || []).push(s.id);
    }
  }
}

const qdisplays = new Set(fs.readdirSync(qdisplayDir)
  .filter(n => n.endsWith('.qdisplay.dry'))
  .map(n => n.replace(/\.qdisplay\.dry$/, '')));

function checkTargetList(s, propName) {
  const p = s.props[propName];
  if (!p || p.magic) {
    return;
  }
  for (const part of p.text.split(';')) {
    const target = part.trim().split(/\s+if\s+/)[0].trim();
    if (target && !resolve(s, target)) {
      err(`${s.file}:${p.line}`, `${propName} target "${target}" not found`);
    }
  }
}

for (const s of Object.values(scenes)) {
  checkTargetList(s, 'go-to');
  checkTargetList(s, 'call');
  checkTargetList(s, 'set-jump');
  for (const {text, line} of s.content) {
    const choice = text.match(/^-\s*@([A-Za-z0-9_.]+)/);
    if (choice && !resolve(s, choice[1])) {
      err(`${s.file}:${line}`, `choice target "@${choice[1]}" not found`);
    }
    const tagChoice = text.match(/^-\s*#([A-Za-z0-9_]+)/);
    if (tagChoice && !tags[tagChoice[1]]) {
      err(`${s.file}:${line}`, `no scene is tagged "${tagChoice[1]}"`);
    }
  }
}

// ---------------------------------------------------------------------------
// Content: inserts, qdisplays, bracket balance
// ---------------------------------------------------------------------------
for (const s of Object.values(scenes)) {
  let inMagic = false;
  for (const {text, line} of s.content) {
    if (/^#/.test(text)) {
      continue; // comment
    }
    // strip {! ... !} raw html on this line
    let t = text;
    if (inMagic) {
      const end = t.indexOf('!}');
      if (end < 0) {
        continue;
      }
      t = t.slice(end + 2);
      inMagic = false;
    }
    for (const m of t.matchAll(/\{!(.*?)!\}/g)) {
      if (/\[[+?]/.test(m[1])) {
        err(`${s.file}:${line}`, 'insert or conditional inside {! !} is not evaluated; close the raw HTML around it');
      }
    }
    t = t.replace(/\{!.*?!\}/g, '');
    if (t.includes('{!')) {
      inMagic = true;
      t = t.slice(0, t.indexOf('{!'));
    }
    const opensC = (t.match(/\[\?/g) || []).length;
    const closesC = (t.match(/\?\]/g) || []).length;
    const opensI = (t.match(/\[\+/g) || []).length;
    const closesI = (t.match(/\+\]/g) || []).length;
    if (opensC !== closesC) {
      err(`${s.file}:${line}`, `unbalanced [? ?] (${opensC} vs ${closesC})`);
    }
    // Dendry ends a conditional at the first "?]", so [? ... [? ... ?] ... ?] breaks
    let depth = 0;
    for (const tok of t.match(/\[\?|\?\]/g) || []) {
      depth += tok === '[?' ? 1 : -1;
      if (depth > 1) {
        err(`${s.file}:${line}`, 'nested [? ?] conditional; write separate conditionals instead');
        break;
      }
    }
    if (opensI !== closesI) {
      err(`${s.file}:${line}`, `unbalanced [+ +] (${opensI} vs ${closesI})`);
    }
    const stray = t.replace(/\[[?+]/g, '').replace(/[?+]\]/g, '');
    if (/[[\]]/.test(stray)) {
      err(`${s.file}:${line}`, 'stray "[" or "]" (Dendry treats [ ] as a hidden block)');
    }
    for (const m of t.matchAll(/\[\+([^+]*)\+\]/g)) {
      const parts = m[1].split(':');
      if (parts.length > 1) {
        const qd = parts[1].trim();
        if (!qdisplays.has(qd)) {
          err(`${s.file}:${line}`, `unknown qdisplay "${qd}"`);
        }
      }
    }
  }
  if (inMagic) {
    err(`${s.file}:${s.line}`, 'unterminated {! in content');
  }
}

// ---------------------------------------------------------------------------
// JavaScript blocks compile
// ---------------------------------------------------------------------------
for (const s of Object.values(scenes)) {
  for (const [name, p] of Object.entries(s.props)) {
    if (p.magic !== undefined) {
      try {
        // eslint-disable-next-line no-new-func
        new Function('state', 'Q', p.magic);
      } catch (e) {
        err(`${s.file}:${p.line}`, `${name} JavaScript does not compile: ${e.message}`);
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Variables
// ---------------------------------------------------------------------------
const KEYWORDS = new Set(['and', 'or', 'not', 'if', 'true', 'false']);
const initialised = new Set(['started', 'month', 'year', 'time']);
const read = new Map();         // name -> first location
const incremented = new Map();  // name -> first location

function identifiers(expr) {
  const noStrings = expr.replace(/"[^"]*"|'[^']*'/g, '');
  return (noStrings.match(/[A-Za-z_][A-Za-z0-9_]*/g) || [])
    .filter(x => !KEYWORDS.has(x) && !/^\d/.test(x));
}
function noteRead(name, where) {
  if (!read.has(name)) {
    read.set(name, where);
  }
}

// assignments from JS blocks: Q.name = / Q.name +=
for (const s of Object.values(scenes)) {
  for (const p of Object.values(s.props)) {
    if (p.magic !== undefined) {
      for (const m of p.magic.matchAll(/Q\.([A-Za-z_][A-Za-z0-9_]*)\s*(=(?!=)|\+=|-=|\*=)/g)) {
        initialised.add(m[1]);
      }
    }
  }
}

// names generated dynamically in root / election_algorithm / post_event
const rootStart = scenes['root.start'] && scenes['root.start'].props['on-arrival'];
function arrayLiteral(name) {
  const m = rootStart && rootStart.magic.match(new RegExp(`Q\\.${name}\\s*=\\s*\\[([\\s\\S]*?)\\]`));
  return m ? (m[1].match(/'([^']+)'/g) || []).map(x => x.slice(1, -1)) : [];
}
const classes = arrayLiteral('classes');
const parties = arrayLiteral('parties');
const factions = arrayLiteral('factions');
const timers = arrayLiteral('timers');
for (const c of classes) {
  for (const p of parties) {
    for (const suffix of ['', '_normalized', '_display']) {
      initialised.add(`${c}_${p}${suffix}`);
    }
  }
}
for (const f of factions) {
  initialised.add(`${f}_strength`);
  initialised.add(`${f}_dissent`);
}
for (const t of timers) {
  initialised.add(`${t}_timer`);
}
for (const p of ['con', 'lab', 'lib', 'snp', 'pc', 'other']) {
  initialised.add(`${p}_votes`);
  initialised.add(`${p}_seats`);
}

// short-syntax actions and predicates
for (const s of Object.values(scenes)) {
  const where = s.file;
  for (const [name, p] of Object.entries(s.props)) {
    if (p.magic !== undefined || p.text === undefined) {
      continue;
    }
    const loc = `${where}:${p.line}`;
    if (name === 'on-arrival' || name === 'on-departure') {
      for (const stmt of p.text.split(';')) {
        const m = stmt.trim().match(/^([A-Za-z_][A-Za-z0-9_]*)\s*(\+=|-=|\*=|=)\s*(.*)$/);
        if (!m) {
          if (stmt.trim()) {
            err(loc, `can't parse action "${stmt.trim()}"`);
          }
          continue;
        }
        const [, target, op, rest] = m;
        if (op === '=') {
          initialised.add(target);
        } else if (!incremented.has(target)) {
          incremented.set(target, loc);
        }
        for (const id of identifiers(rest)) {
          noteRead(id, loc);
        }
      }
    } else if (['view-if', 'choose-if'].includes(name)) {
      for (const id of identifiers(p.text)) {
        noteRead(id, loc);
      }
    } else if (name === 'go-to') {
      for (const part of p.text.split(';')) {
        const cond = part.split(/\s+if\s+/)[1];
        if (cond) {
          for (const id of identifiers(cond)) {
            noteRead(id, loc);
          }
        }
      }
    }
  }
  for (const {text, line} of s.content) {
    const loc = `${where}:${line}`;
    const stripped = text.replace(/\{!.*?!\}/g, '');
    for (const m of stripped.matchAll(/\[\?\s*if\s*([^:]+):/g)) {
      for (const id of identifiers(m[1])) {
        noteRead(id, loc);
      }
    }
    for (const m of stripped.matchAll(/\[\+([^+:]*)(:[^+]*)?\+\]/g)) {
      for (const id of identifiers(m[1])) {
        noteRead(id, loc);
      }
    }
  }
}

for (const [name, loc] of read) {
  if (!initialised.has(name) && !name.startsWith('achievement_') && !name.startsWith('game_achievement_')) {
    warn(loc, `"${name}" is read but never assigned`);
  }
}
for (const [name, loc] of incremented) {
  if (!initialised.has(name)) {
    err(loc, `"${name}" is incremented but never initialised (would become NaN)`);
  }
}

// ---------------------------------------------------------------------------
console.log(`Checked ${sceneFiles.length} scene files, ${Object.keys(scenes).length} scenes and sections, ${qdisplays.size} qdisplays.`);
for (const w of warnings) {
  console.log('warning: ' + w);
}
for (const e of errors) {
  console.log('error:   ' + e);
}
console.log(`${errors.length} error(s), ${warnings.length} warning(s).`);
process.exit(errors.length ? 1 : 0);
