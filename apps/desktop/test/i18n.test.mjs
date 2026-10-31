import test from 'node:test';
import assert from 'node:assert/strict';
import { MESSAGES, resolveLanguage, translate } from '../src/i18n.mjs';

test('the shell starts in English and follows DeepTutor interface languages', () => {
  assert.equal(resolveLanguage(undefined), 'en');
  assert.equal(resolveLanguage('auto'), 'en');
  assert.equal(resolveLanguage('zh'), 'zh');
  assert.equal(resolveLanguage('zh-CN'), 'zh');
  assert.equal(translate('fr', 'retry'), 'Réessayer');
});

test('every language translates every shell string', () => {
  const keys = Object.keys(MESSAGES.en).sort();
  for (const [language, messages] of Object.entries(MESSAGES)) {
    assert.deepEqual(Object.keys(messages).sort(), keys, language);
  }
});

test('placeholders are filled and unknown ones are left visible', () => {
  assert.match(translate('en', 'workerExited', { code: 3 }), /\(3\)/);
  assert.match(translate('de', 'aboutDetail', { core: '1.7.0' }), /Kern 1\.7\.0\nBuild \{runtime\}/);
});
