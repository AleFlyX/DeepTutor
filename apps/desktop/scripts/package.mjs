import { packager } from '@electron/packager';
import { cp, mkdir, rm, readFile, writeFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

// The app is versioned with the DeepTutor core it ships: Open DeepTutor MacOS v<core>.
const seed = JSON.parse(await readFile('.local/seed/runtime.json', 'utf8'));
const version = seed.coreVersion;
const stage = path.resolve('.local/app');
await rm(stage, { recursive: true, force: true });
await mkdir(stage, { recursive: true });
for (const name of ['src', 'assets', 'README.md']) {
  await cp(name, path.join(stage, name), { recursive: true });
}
const pkg = JSON.parse(await readFile('package.json', 'utf8'));
await writeFile(path.join(stage, 'package.json'), JSON.stringify({ ...pkg, version }, null, 2));
await cp('../../LICENSE', path.join(stage, 'LICENSE'));

// With APPLE_SIGNING_IDENTITY ("Developer ID Application: …") the app gets a
// hardened-runtime Developer ID signature; otherwise it is signed ad hoc.
const identity = process.env.APPLE_SIGNING_IDENTITY;
const entitlements = path.resolve('assets/entitlements.mac.plist');
const outputs = await packager({
  dir: stage, name: 'Open DeepTutor', appBundleId: 'org.deeptutor.open-desktop',
  appVersion: version, buildVersion: version, electronVersion: pkg.devDependencies.electron,
  platform: 'darwin', arch: process.arch, out: 'out', overwrite: true,
  asar: false, prune: false, icon: path.resolve('assets/icon.icns'),
  extraResource: [path.resolve('.local/seed')],
  appCategoryType: 'public.app-category.education',
  extendInfo: {
    NSMicrophoneUsageDescription: 'Open DeepTutor uses the microphone when you speak to your tutor.',
    NSCameraUsageDescription: 'Open DeepTutor uses the camera when you capture learning material.',
    NSLocalNetworkUsageDescription: 'Open DeepTutor runs its learning services on this Mac.',
  },
  ...(identity ? { osxSign: { identity, optionsForFile: () => ({ hardenedRuntime: true, entitlements }) } } : {}),
});
for (const output of outputs) {
  const bundle = path.join(output, 'Open DeepTutor.app');
  if (!identity) execFileSync('/usr/bin/codesign', ['--force', '--deep', '--sign', '-', bundle], { stdio: 'inherit' });
  execFileSync('/usr/bin/codesign', ['--verify', '--deep', '--strict', bundle], { stdio: 'inherit' });
  console.log(bundle);
}
