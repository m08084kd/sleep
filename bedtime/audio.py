"""音声まわりの共通処理（wav 読み書き・ffmpeg の場所）。"""

from __future__ import annotations

import shutil
import wave
from pathlib import Path

import numpy as np

SR = 48000


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("ffmpeg が見つかりません。`pip install imageio-ffmpeg` するか ffmpeg を入れてください。") from e


def write_wav(path: Path, x: np.ndarray, sr: int = SR) -> None:
    """float32 のモノラル / ステレオ (N, 2) 配列を 16bit wav で保存する。"""
    x = np.clip(x, -1, 1)
    ch = 1 if x.ndim == 1 else x.shape[1]
    with wave.open(str(path), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767
        if w.getnchannels() > 1:
            data = data.reshape(-1, w.getnchannels()).mean(axis=1)
    return data
