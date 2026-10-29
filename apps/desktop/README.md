# Open DeepTutor for macOS

A double-clickable macOS app for DeepTutor. On first launch it installs its
bundled runtime, starts the Python and Node services on loopback, and opens
the complete DeepTutor web UI in its window. Users need no terminal, Python,
Node, npm, Git or source checkout.

This is an Apple Silicon preview. Models and providers are configured in
DeepTutor's normal Settings; no credentials or user data ship with the app.
Optional external tools (Manim/LaTeX, partner CLIs, remote services) keep
their usual requirements.

## Versions and language

- The app version is the DeepTutor version it bundles. Packaging reads it from
  `deeptutor/__version__.py` via the sealed runtime, so `package.json` stays at
  `0.0.0`. The app shows itself as **Open DeepTutor MacOS v1.7.0**; the web UI
  in a browser shows **Open DeepTutor Web v1.7.0**. The web UI recognises the
  app by the `OpenDeepTutor/<version> (macOS)` user-agent marker.
- The shell (start screen, menus, dialogs) starts in English and then follows
  the interface language and theme chosen in DeepTutor's Settings
  (`data/user/settings/interface.json`), including live changes. Copy lives in
  `src/i18n.mjs` for every language the web UI ships.

## Components

- **Shell**: Electron window, native menus, downloads, runtime supervision.
- **Core bundle**: Python source and modules, the production Next.js standalone
  build, Python 3.12.13 and Node 22.23.4, built from a committed revision.
- **Protocol 1**: the shell only manages startup, readiness, shutdown and core
  artifacts. No business API or React components are copied into the shell.
- **Data**: `~/Library/Application Support/Open DeepTutor/workspace/data`.
- **Runtimes**: `~/Library/Application Support/Open DeepTutor/runtimes/<runtime-id>`.
- **Logs**: `~/Library/Application Support/Open DeepTutor/logs/runtime.log`.

Quitting stops the services this app started. It does not stop a separately
running `deeptutor start`. Web content has no preload, Node integration or
desktop IPC privileges; only the private shell page owns the native bridge.

## Build

Prerequisites (developers only): Apple Silicon macOS, Node/npm and `uv`.

```sh
cd apps/desktop
npm ci
npm run check && npm test
npm run build:runtime     # snapshots this checkout's committed HEAD
npm run smoke             # boots the bundled core with no developer tools on PATH
npm run package:mac       # out/Open DeepTutor-darwin-arm64/Open DeepTutor.app
npm run package:dmg       # out/Open-DeepTutor-MacOS-v<version>-arm64.dmg
```

`build:runtime` uses `git archive HEAD`, so commit first; uncommitted changes
are not bundled. Set `DEEPTUTOR_SOURCE` to build another checkout.
`npm start` runs the shell against the same bundled core. `npm run icon`
regenerates `assets/icon.icns` from `assets/mark.png`.

## Signing

- **Core bundles** are signed with an Ed25519 key. The private key is
  `.local/signing-private.pem` (ignored) or the `OPEN_DEEPTUTOR_SIGNING_KEY`
  environment variable; only `assets/runtime-public.pem` ships. Sealing refuses
  a key that does not match the public key. Keep a secure backup: losing it
  means shipped apps can no longer accept core updates.
  `node scripts/seal-runtime.mjs --new-key` deliberately starts a new identity.
- **The app** is signed ad hoc by default. Set `APPLE_SIGNING_IDENTITY` to a
  Developer ID Application identity for a hardened-runtime signature
  (`assets/entitlements.mac.plist`), then notarize the DMG.

## Releases

`.github/workflows/desktop-release.yml` runs when a DeepTutor GitHub Release is
published. It verifies the tag matches `deeptutor/__version__.py`, builds and
smoke-tests the runtime, packages the app and attaches
`Open-DeepTutor-MacOS-v<version>-arm64.dmg` to the release. It needs the
`DESKTOP_RUNTIME_SIGNING_KEY` secret; Developer ID signing and notarization run
when the Apple secrets listed in the workflow are present.

## Core updates

The shell never `git pull`s or mutates a running Python environment. **Core →
Install Core Update…** accepts a signed `runtime.json` beside its `.tar.gz`.
The app verifies the signature, SHA-256, architecture and protocol, installs
into a new version directory, backs up the desktop workspace, then starts the
candidate. A failed or interrupted trial restores the previous runtime and
workspace. Backups are kept. Automatic update discovery is not connected yet.

## Verification

`npm test` covers language resolution, config validation, signature rejection,
process shutdown, cancellation and local service behaviour. `npm run smoke`
boots the real bundled core in a fresh temporary workspace, checks backend,
frontend and API proxy, then verifies both ports close. It does not call a paid
model or test optional external renderers. `OPEN_DEEPTUTOR_TEST_HOME` selects a
disposable desktop home for UI checks.
