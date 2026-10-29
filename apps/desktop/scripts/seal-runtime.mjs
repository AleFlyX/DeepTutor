import { createPrivateKey, createPublicKey, generateKeyPairSync, sign } from 'node:crypto';
import { mkdir, readFile, writeFile, access } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { canonicalManifest, sha256 } from '../src/bundles.mjs';

const keyFile = '.local/signing-private.pem';
await mkdir('.local/seed', { recursive: true });
if (process.env.OPEN_DEEPTUTOR_SIGNING_KEY) {
  await writeFile(keyFile, process.env.OPEN_DEEPTUTOR_SIGNING_KEY, { mode: 0o600 });
}
try { await access(keyFile); }
catch {
  // A new key orphans every shell already shipped, so it is never implicit.
  if (!process.argv.includes('--new-key')) {
    throw new Error(`Missing ${keyFile}. Restore the release signing key, set OPEN_DEEPTUTOR_SIGNING_KEY, or pass --new-key to start a new signing identity.`);
  }
  const keys = generateKeyPairSync('ed25519');
  await writeFile(keyFile, keys.privateKey.export({ type: 'pkcs8', format: 'pem' }), { mode: 0o600 });
  await writeFile('assets/runtime-public.pem', keys.publicKey.export({ type: 'spki', format: 'pem' }));
}
const privateKey = createPrivateKey(await readFile(keyFile));
const derived = createPublicKey(privateKey).export({ type: 'spki', format: 'pem' }).trim();
if (derived !== (await readFile('assets/runtime-public.pem', 'utf8')).trim()) {
  throw new Error('The signing key does not match assets/runtime-public.pem; the shipped app would reject this core.');
}
const coreVersion = /__version__\s*=\s*['"]([^'"]+)/.exec(await readFile('.local/runtime/core/deeptutor/__version__.py', 'utf8'))[1];
const commit = (await readFile('.local/runtime/BUILD_COMMIT', 'utf8')).trim();
const runtimeId = `${coreVersion}-${commit.slice(0, 9)}-${process.arch}`;
const archive = `open-deeptutor-core-${runtimeId}.tar.gz`;
execFileSync('/usr/bin/tar', ['-czf', `.local/seed/${archive}`, '-C', '.local/runtime', '.'], { stdio: 'inherit', env: { ...process.env, COPYFILE_DISABLE: '1' } });
const manifest = {
  formatVersion: 1, protocolVersion: 1, platform: 'darwin', arch: process.arch,
  runtimeId, coreVersion, commit, archive, sha256: await sha256(`.local/seed/${archive}`),
};
manifest.signature = sign(null, Buffer.from(canonicalManifest(manifest)), privateKey).toString('base64');
await writeFile('.local/seed/runtime.json', JSON.stringify(manifest, null, 2) + '\n');
console.log(`Sealed runtime ${runtimeId}`);
