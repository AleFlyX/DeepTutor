import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { createWriteStream } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import { installBundle, bundleConfig } from '../src/bundles.mjs';
import { SourceRuntime } from '../src/runtime.mjs';
import { probe } from '../src/processes.mjs';

const home = await mkdtemp(path.join(os.tmpdir(), 'Open DeepTutor smoke '));
const log = createWriteStream('.local/smoke.log');
const runtime = new SourceRuntime({ log: chunk => log.write(chunk) });
runtime.on('status', state => console.log(`${state.phase}: ${state.step ?? state.message}`));
try {
  const installed = await installBundle(path.resolve('.local/seed/runtime.json'), home, await readFile('assets/runtime-public.pem', 'utf8'), console.log);
  // Deliberately hide developer toolchains. Only bundled Python/Node are used.
  process.env.PATH = '/usr/bin:/bin:/usr/sbin:/sbin';
  await runtime.start(bundleConfig(installed.destination, path.join(home, 'workspace'), installed.manifest.runtimeId), path.join(home, 'cache'));
  assert.equal(runtime.state.phase, 'ready', runtime.state.message);
  const { url, backendURL } = runtime.state;
  assert.equal(await probe(`${backendURL}/health/ready`), true);
  const page = await fetch(url);
  assert.equal(page.status, 200);
  assert.match(await page.text(), /DeepTutor/);
  const response = await fetch(`${url}/api/settings/ui`);
  assert.equal(response.status, 200, await response.text());
  await runtime.stop();
  assert.equal(await probe(url), false);
  assert.equal(await probe(backendURL), false);
  await writeFile('.local/smoke-result.json', JSON.stringify({ core: installed.manifest.runtimeId, frontend: 'passed', backend: 'passed', proxy: 'passed', shutdown: 'passed', developerPATH: 'absent' }, null, 2));
  console.log('PASS: bundled runtime boots, serves UI/API, and cleans up with no developer tools on PATH.');
} finally {
  await runtime.stop();
  log.end();
  await rm(home, { recursive: true, force: true });
}
