"""オリジナルの子守歌 BGM を合成する（著作権フリー）。

オルゴール風のメロディ + やわらかいパッド + うすい「さーっ」というノイズ。
テンポはゆっくり（1 分間に 54 拍、3 拍子）で、赤ちゃんの心拍より遅めにしている。
"""

from __future__ import annotations

import numpy as np

from .audio import SR

# F メジャーの 8 小節のメロディ（MIDI ノート, 拍数）。 None は休符。
MELODY = [
    (72, 1), (69, 1), (72, 1), (74, 2), (72, 1),
    (69, 2), (65, 1), (67, 3),
    (69, 1), (72, 1), (77, 1), (76, 2), (74, 1),
    (72, 3), (None, 3),
    (74, 1), (72, 1), (69, 1), (70, 2), (69, 1),
    (67, 2), (64, 1), (65, 3),
    (69, 1), (67, 1), (65, 1), (67, 2), (64, 1),
    (65, 3), (None, 3),
]
# 1 小節ごとのコード（ルート付き）
CHORDS = [
    [53, 57, 60], [50, 57, 62], [46, 58, 62], [48, 55, 64],
    [53, 57, 60], [46, 58, 62], [48, 55, 60], [53, 57, 60],
]


def _hz(n: int) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


def _music_box(freq: float, dur: float) -> np.ndarray:
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 2.6) * (1 - np.exp(-t * 400))
    tone = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t * 5)
            + 0.15 * np.sin(2 * np.pi * freq * 5.4 * t) * np.exp(-t * 9))
    return (tone * env).astype(np.float32)


def _pad(freqs: list[float], dur: float) -> np.ndarray:
    t = np.arange(int(dur * SR)) / SR
    atk = np.minimum(1, t / 1.5)
    rel = np.minimum(1, (dur - t) / 1.5).clip(0)
    out = np.zeros_like(t)
    for f in freqs:
        for det in (-0.6, 0.6):
            out += np.sin(2 * np.pi * (f + det) * t) + 0.2 * np.sin(4 * np.pi * (f + det) * t)
    return (out * atk * rel / (len(freqs) * 2)).astype(np.float32)


def _reverb(x: np.ndarray, mix: float = 0.35) -> np.ndarray:
    """とても簡単なコム・フィルタ式リバーブ（ステレオ化も兼ねる）。"""
    outs = []
    for delays in ((1557, 1617, 1491, 1422), (1277, 1356, 1188, 1116)):
        wet = np.zeros_like(x)
        for d in delays:
            d = d * 3
            y = x.copy()
            # フィードバック付き遅延をブロック単位で計算
            for start in range(d, len(y), d):
                end = min(len(y), start + d)
                y[start:end] += 0.72 * y[start - d:end - d]
            wet += y
        wet /= len(delays)
        outs.append((1 - mix) * x + mix * wet)
    return np.stack(outs, axis=1)


def _pink_noise(n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    white = rng.standard_normal(n)
    spec = np.fft.rfft(white)
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = 1
    spec /= np.sqrt(f)
    spec[f > 1800] *= 0.2
    x = np.fft.irfft(spec, n)
    return (x / (np.abs(x).max() + 1e-9)).astype(np.float32)


def make_bgm(duration: float, bpm: float = 54, volume_db: float = -30.0, noise_db: float = -44.0,
             fade_in: float = 4.0, fade_out: float = 12.0) -> np.ndarray:
    """duration 秒の BGM（ステレオ, float32）を作る。メロディはくり返す。"""
    beat = 60.0 / bpm
    loop_beats = sum(b for _, b in MELODY)
    loop_len = loop_beats * beat
    n_total = int(duration * SR)

    # 1 ループぶんを作ってから並べる
    loop = np.zeros(int((loop_len + 4) * SR), dtype=np.float32)
    pos = 0.0
    for note, beats in MELODY:
        if note is not None:
            s = int(pos * SR)
            tone = _music_box(_hz(note), min(4.0, beats * beat + 2.5)) * 0.5
            loop[s:s + len(tone)] += tone[: len(loop) - s]
        pos += beats * beat
    bar = 3 * beat
    for i, ch in enumerate(CHORDS):
        s = int(i * bar * SR)
        p = _pad([_hz(n) for n in ch], bar + 1.5) * 0.22
        loop[s:s + len(p)] += p[: len(loop) - s]
    # ループの継ぎ目の余韻を先頭に足す
    head = int(loop_len * SR)
    tail = loop[head:].copy()
    loop = loop[:head]
    loop[: len(tail)] += tail

    reps = int(np.ceil(n_total / len(loop))) + 1
    mono = np.tile(loop, reps)[:n_total]
    st = _reverb(mono)
    st /= np.abs(st).max() + 1e-9
    st *= 10 ** (volume_db / 20) * 4  # ピークではなく体感音量に近づけるための係数
    if noise_db is not None:
        nz = _pink_noise(n_total)
        st += (nz * 10 ** (noise_db / 20) * 3)[:, None]

    t = np.arange(n_total) / SR
    env = np.minimum(1, t / max(fade_in, 1e-3)) * np.clip((duration - t) / max(fade_out, 1e-3), 0, 1)
    return (st * env[:, None]).astype(np.float32)
