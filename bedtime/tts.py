"""朗読音声の合成。

バックエンド:
  - openjtalk : オフラインで動く。東北大学の女性話者 tohoku-f01 を使用（CC-BY 4.0）。
  - voicevox  : ローカルで起動した VOICEVOX ENGINE (http://127.0.0.1:50021) を使う。
                いちばん自然でやさしい声になるのでおすすめ。
  - edge      : Microsoft Edge の読み上げ（ja-JP-NanamiNeural など）。ネット接続が必要。

どのバックエンドも 48kHz / モノラル / float32 の numpy 配列を返す。
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

from .audio import SR, ffmpeg_exe, read_wav, write_wav

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HTSVOICE = ROOT / "assets" / "voices" / "tohoku-f01-neutral.htsvoice"


def speech_text(text: str) -> str:
    """字幕用の文章を読み上げ用に整える（分かち書きの空白や記号を取る）。"""
    t = text.replace("\n", "").replace("　", " ")
    t = re.sub(r"\s+", "", t)
    t = t.replace("〜", "ー").replace("…", "、")
    return t


class Synthesizer:
    def __init__(self, cfg: dict, cache_dir: Path):
        self.cfg = dict(cfg or {})
        self.backend = self.cfg.get("backend", "openjtalk")
        self.cache_dir = cache_dir
        cache_dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, text: str) -> np.ndarray:
        key = hashlib.sha1(json.dumps([self.cfg, text], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
        path = self.cache_dir / f"{self.backend}_{key}.wav"
        if path.exists():
            return read_wav(path)
        fn = {"openjtalk": self._openjtalk, "voicevox": self._voicevox, "edge": self._edge}.get(self.backend)
        if fn is None:
            raise ValueError(f"未知の voice.backend です: {self.backend}")
        audio = fn(speech_text(text))
        audio = _normalize(_trim_silence(audio), self.cfg.get("loudness", -20.0))
        write_wav(path, audio)
        return audio

    # ---------------------------------------------------------------- Open JTalk
    def _openjtalk(self, text: str) -> np.ndarray:
        import pyopenjtalk
        from pyopenjtalk.htsengine import HTSEngine

        voice = Path(self.cfg.get("htsvoice", DEFAULT_HTSVOICE))
        if not voice.is_absolute():
            voice = ROOT / voice
        if not voice.exists():
            raise FileNotFoundError(f"{voice} がありません。scripts/setup_assets.sh を実行してください。")
        eng = HTSEngine(str(voice).encode())
        eng.set_speed(float(self.cfg.get("speed", 0.82)))
        eng.add_half_tone(float(self.cfg.get("half_tone", 0.0)))
        labels = pyopenjtalk.extract_fullcontext(text)
        x = eng.synthesize(labels) / 32768.0
        sr = eng.get_sampling_frequency()
        return _resample(x.astype(np.float32), sr, SR)

    # ---------------------------------------------------------------- VOICEVOX
    def _voicevox(self, text: str) -> np.ndarray:
        host = self.cfg.get("host", "http://127.0.0.1:50021")
        speaker = int(self.cfg.get("speaker", 8))  # 8 = 春日部つむぎ（ノーマル）
        q = urllib.parse.urlencode({"text": text, "speaker": speaker})
        with urllib.request.urlopen(urllib.request.Request(f"{host}/audio_query?{q}", method="POST"), timeout=60) as r:
            query = json.load(r)
        query["speedScale"] = float(self.cfg.get("speed", 0.85))
        query["pitchScale"] = float(self.cfg.get("pitch", -0.02))
        query["intonationScale"] = float(self.cfg.get("intonation", 0.9))
        query["volumeScale"] = 1.0
        query["prePhonemeLength"] = 0.1
        query["postPhonemeLength"] = 0.2
        query["outputSamplingRate"] = SR
        query["outputStereo"] = False
        req = urllib.request.Request(
            f"{host}/synthesis?speaker={speaker}", data=json.dumps(query).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            with urllib.request.urlopen(req, timeout=120) as r:
                f.write(r.read())
            f.flush()
            return _decode(Path(f.name))

    # ---------------------------------------------------------------- Edge
    def _edge(self, text: str) -> np.ndarray:
        import asyncio

        import edge_tts

        voice = self.cfg.get("voice", "ja-JP-NanamiNeural")
        rate = self.cfg.get("rate", "-25%")
        pitch = self.cfg.get("pitch", "-5Hz")
        with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
            asyncio.run(edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(f.name))
            return _decode(Path(f.name))


# ---------------------------------------------------------------- helpers
def _decode(path: Path) -> np.ndarray:
    raw = subprocess.run(
        [ffmpeg_exe(), "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def _resample(x: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    if sr_in == sr_out:
        return x
    n = int(round(len(x) * sr_out / sr_in))
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def _trim_silence(x: np.ndarray, thresh: float = 0.004) -> np.ndarray:
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(0.05 * SR))
    b = min(len(x), idx[-1] + int(0.15 * SR))
    return x[a:b]


def _normalize(x: np.ndarray, target_db: float) -> np.ndarray:
    rms = float(np.sqrt(np.mean(x ** 2)) + 1e-9)
    y = x * (10 ** (target_db / 20) / rms)
    peak = float(np.max(np.abs(y)) + 1e-9)
    if peak > 0.9:
        y *= 0.9 / peak
    return y.astype(np.float32)
