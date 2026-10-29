import { cp, mkdir, rm, readFile, writeFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sha256 } from '../src/bundles.mjs';

if (process.platform !== 'darwin' || process.arch !== 'arm64') throw new Error('Building the macOS app currently requires an Apple Silicon Mac');
// Builds from the committed HEAD of the DeepTutor checkout this app lives in.
const source = path.resolve(process.env.DEEPTUTOR_SOURCE || fileURLToPath(new URL('../../..', import.meta.url)));
const build = path.resolve('.local/build');
const runtime = path.resolve('.local/runtime');
const pythonDirectory = path.resolve('.local/python-downloads/cpython-3.12.13-macos-aarch64-none');
const python = path.join(pythonDirectory, 'bin/python3.12');
const run = (command, args, options = {}) => execFileSync(command, args, { stdio: 'inherit', ...options });
const assembleOnly = process.argv.includes('--assemble');

await mkdir('.local', { recursive: true });
if (!assembleOnly) {
  const commit = execFileSync('git', ['-C', source, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  await rm(build, { recursive: true, force: true });
  await mkdir(build, { recursive: true });
  run('git', ['-C', source, 'archive', '--output', path.resolve('.local/source.tar'), commit]);
  run('/usr/bin/tar', ['-xf', path.resolve('.local/source.tar'), '-C', build]);
  await writeFile(path.join(build, 'BUILD_COMMIT'), commit + '\n');
  run('uv', ['python', 'install', '3.12.13', '--install-dir', path.resolve('.local/python-downloads'), '--no-bin']);
  run('uv', ['pip', 'install', '--break-system-packages', '--python', python, '-r', path.join(build, 'requirements/full.txt')]);
  run('npm', ['ci', '--legacy-peer-deps'], { cwd: path.join(build, 'web') });
  run('npm', ['run', 'build'], { cwd: path.join(build, 'web'), env: {
    ...process.env, NEXT_PUBLIC_API_BASE: '__NEXT_PUBLIC_API_BASE_PLACEHOLDER__',
    NEXT_PUBLIC_AUTH_ENABLED: '__NEXT_PUBLIC_AUTH_ENABLED_PLACEHOLDER__', NEXT_TELEMETRY_DISABLED: '1',
  } });
  run('/usr/bin/curl', ['-fL', 'https://nodejs.org/dist/v22.23.4/node-v22.23.4-darwin-arm64.tar.gz', '-o', '.local/node.tar.gz']);
}
if (await sha256('.local/node.tar.gz') !== 'c9e1dbc748b33ed2d14f42445191ecaf14c56259c7a9a26d0042c49ec2b66428') throw new Error('Node runtime checksum mismatch');
await rm(runtime, { recursive: true, force: true });
await mkdir(path.join(runtime, 'core'), { recursive: true });
for (const name of ['deeptutor', 'deeptutor_cli', 'assets', 'scripts', 'requirements', 'pyproject.toml', 'build_metadata.py', 'build_support.py', 'setup.py', 'LICENSE', 'THIRD_PARTY_NOTICES.md']) {
  await cp(path.join(build, name), path.join(runtime, 'core', name), {
    recursive: true, filter: file => !file.split(path.sep).includes('__pycache__'),
  });
}
await cp(pythonDirectory, path.join(runtime, 'python'), { recursive: true, verbatimSymlinks: true });
// Wheel-generated console scripts otherwise retain the builder's absolute path.
for (const entry of await readdir(path.join(runtime, 'python/bin'), { withFileTypes: true })) {
  if (!entry.isFile()) continue;
  const file = path.join(runtime, 'python/bin', entry.name);
  const bytes = await readFile(file);
  if (bytes.subarray(0, 2).toString() !== '#!') continue;
  const text = bytes.toString('utf8');
  if (!/^#![^\n]*python[^\n]*\n/.test(text)) continue;
  const launcher = '#!/bin/sh\n\'\'\'exec\' "$(dirname "$0")/python3.12" "$0" "$@"\n\' \'\'\'\n';
  await writeFile(file, text.replace(/^#![^\n]*\n/, launcher));
}
await mkdir(path.join(runtime, 'node'));
run('/usr/bin/tar', ['-xzf', '.local/node.tar.gz', '-C', path.join(runtime, 'node'), '--strip-components', '1']);
await cp(path.join(build, 'web/.next/standalone'), path.join(runtime, 'web'), { recursive: true, verbatimSymlinks: true });
await cp(path.join(build, 'BUILD_COMMIT'), path.join(runtime, 'BUILD_COMMIT'));
const freeze = execFileSync('uv', ['pip', 'freeze', '--python', python], { encoding: 'utf8' });
await writeFile(path.join(runtime, 'PYTHON_DEPENDENCIES.txt'), freeze);
await writeFile(path.join(runtime, 'BUILD_INFO.json'), JSON.stringify({
  coreCommit: (await readFile(path.join(build, 'BUILD_COMMIT'), 'utf8')).trim(),
  python: '3.12.13', node: '22.23.4', arch: process.arch,
}, null, 2));
run(process.execPath, ['scripts/seal-runtime.mjs']);
