import { cp, mkdir, readFile, rm, symlink } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const { coreVersion } = JSON.parse(await readFile('.local/seed/runtime.json', 'utf8'));
const built = path.resolve(`out/Open DeepTutor-darwin-${process.arch}`);
const stage = path.resolve('.local/dmg');
const dmg = path.resolve(`out/Open-DeepTutor-MacOS-v${coreVersion}-${process.arch}.dmg`);
await rm(stage, { recursive: true, force: true });
await mkdir(stage, { recursive: true });
await cp(path.join(built, 'Open DeepTutor.app'), path.join(stage, 'Open DeepTutor.app'), { recursive: true, verbatimSymlinks: true });
await cp(path.join(built, 'LICENSES.chromium.html'), path.join(stage, 'LICENSES.chromium.html'));
await symlink('/Applications', path.join(stage, 'Applications'));
await rm(dmg, { force: true });
execFileSync('/usr/bin/hdiutil', ['create', '-volname', 'Open DeepTutor', '-srcfolder', stage, '-fs', 'APFS', '-format', 'ULFO', dmg], { stdio: 'inherit' });
await rm(stage, { recursive: true, force: true });
console.log(dmg);
