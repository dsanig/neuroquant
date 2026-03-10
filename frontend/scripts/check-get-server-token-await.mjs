import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const root = join(process.cwd(), 'app');
const offenders = [];

function walk(dir) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      walk(full);
      continue;
    }

    if (!full.endsWith('.ts') && !full.endsWith('.tsx')) continue;

    const text = readFileSync(full, 'utf8');
    const lines = text.split(/\r?\n/);

    lines.forEach((line, idx) => {
      if (!line.includes('getServerToken(')) return;
      if (line.includes('await getServerToken(')) return;
      offenders.push(`${relative(process.cwd(), full)}:${idx + 1}: ${line.trim()}`);
    });
  }
}

walk(root);

if (offenders.length) {
  console.error('Found getServerToken() calls without await:');
  for (const entry of offenders) console.error(`- ${entry}`);
  process.exit(1);
}

console.log('All getServerToken() usages are awaited.');
