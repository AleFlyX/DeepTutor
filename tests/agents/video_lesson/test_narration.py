"""Narration timing and the generated voice module, without calling the TTS service."""

from __future__ import annotations

import asyncio

from deeptutor.agents.video_lesson import narration
from deeptutor.agents.video_lesson.narration import Clip, NarrationLine, estimate, voice_module


def test_estimate_spaces_captions_by_sentence() -> None:
    clip = estimate("先看结论。再看为什么！", "zh")
    assert [text for _, text in clip.captions] == ["先看结论。", "再看为什么！"]
    assert clip.captions[0][0] == 0 < clip.captions[1][0] < clip.frames
    assert clip.audio is None


def test_narrate_falls_back_to_captions_when_speech_fails(monkeypatch) -> None:
    async def broken(text: str, voice: str) -> Clip:
        raise RuntimeError("offline")

    monkeypatch.setattr(narration, "speak", broken)
    cache: dict = {}
    clips = asyncio.run(narration.narrate([NarrationLine("s1", "一句话。")], "zh", cache))
    assert clips["s1"].audio is None and clips["s1"].captions
    assert "一句话。" in cache


def test_voice_module_inlines_audio() -> None:
    module = voice_module(
        {"s1": Clip("a。", 30, [(0, "a。")], b"ID3"), "s2": estimate("b。", "zh")}
    )
    assert module.startswith("export const VOICE = ")
    assert '"src": "data:audio/mpeg;base64,SUQz"' in module
    assert module.count('"src"') == 1


def _tts(monkeypatch, **config) -> None:
    from types import SimpleNamespace

    from deeptutor.services.config import provider_runtime

    monkeypatch.setattr(
        provider_runtime, "resolve_tts_runtime_config", lambda: SimpleNamespace(**config)
    )


def test_settings_edge_voice_is_used_for_its_language(monkeypatch) -> None:
    _tts(monkeypatch, provider_name="edge", voice="en-US-AndrewMultilingualNeural")
    assert narration._configured_voice("en") == "en-US-AndrewMultilingualNeural"
    assert narration._configured_voice("zh") is None


def test_non_edge_tts_settings_keep_the_default_voice(monkeypatch) -> None:
    _tts(monkeypatch, provider_name="openai", voice="alloy")
    assert narration._configured_voice("en") is None
