"""story.yaml から寝かしつけ朗読動画を作るコマンド。

    python -m bedtime.build stories/popo_moon_boat.yaml
    python -m bedtime.build stories/popo_moon_boat.yaml --preview      # 低画質で すばやく確認
    python -m bedtime.build stories/popo_moon_boat.yaml --stills-only  # 絵だけ書き出す

出力（build/<story名>/）:
    <story名>.mp4        完成動画
    <story名>.srt        YouTube にアップロードできる字幕ファイル
    thumbnail.png        サムネイル (1280x720)
    description.txt      概要欄のひな形（クレジット表記つき）
    stills/*.png         場面ごとの絵
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import cairosvg
import numpy as np
import yaml

from .audio import SR, ffmpeg_exe, write_wav
from .bgm import make_bgm
from .scenes import render_scene
from .subtitles import srt_time, subtitle_svg, thumbnail_svg
from .tts import Synthesizer

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_TIMING = {
    "line_pause": 1.8,      # 文と文のあいだの間（秒）
    "scene_pause": 2.5,     # 場面の最後の間
    "crossfade": 2.0,       # 場面が切り替わるときのフェード
    "intro": 3.0,           # 最初の語りが始まるまで
    "outro": 40.0,          # 語りが終わってから、しずかな星空と音楽だけの時間
    "fade_out": 12.0,       # 最後に画面と音を ゆっくり暗くする長さ
}
MOTIONS = ["in", "right", "out", "left"]


@dataclass
class Line:
    text: str
    audio: np.ndarray
    start: float = 0.0          # 場面内の開始時刻
    pause: float = 0.0
    subtitle: bool = True

    @property
    def dur(self) -> float:
        return len(self.audio) / SR


@dataclass
class Scene:
    idx: int
    art: str
    art_opts: dict
    motion: str
    lines: list[Line] = field(default_factory=list)
    start: float = 0.0          # 動画全体での開始時刻
    dur: float = 0.0


# ---------------------------------------------------------------- 準備
def load_story(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        story = yaml.safe_load(f)
    story.setdefault("timing", {})
    story["timing"] = {**DEFAULT_TIMING, **story["timing"]}
    return story


def plan(story: dict, synth: Synthesizer, log=print) -> list[Scene]:
    t = story["timing"]
    scenes: list[Scene] = []
    total_lines = sum(len(s.get("lines", [])) for s in story["scenes"])
    done = 0
    for i, sd in enumerate(story["scenes"]):
        opts = dict(sd.get("art_options", {}))
        if sd["art"] == "title":
            opts.setdefault("title", story.get("title", ""))
            opts.setdefault("subtitle", story.get("subtitle", ""))
        sc = Scene(i, sd["art"], opts, sd.get("motion", MOTIONS[i % len(MOTIONS)]))
        cur = (t["intro"] if i == 0 else t["crossfade"] + 1.0) + float(sd.get("lead", 0))
        for ld in sd.get("lines", []):
            if isinstance(ld, str):
                ld = {"text": ld}
            audio = synth(ld.get("say", ld["text"]))
            done += 1
            log(f"  音声 {done}/{total_lines}: {ld['text'][:24]}")
            line = Line(ld["text"], audio, cur, float(ld.get("pause", t["line_pause"])),
                        ld.get("subtitle", True))
            scenes_line_end = cur + line.dur + line.pause
            sc.lines.append(line)
            cur = scenes_line_end
        sc.dur = max(cur - (sc.lines[-1].pause if sc.lines else 0) + float(sd.get("tail", t["scene_pause"])),
                     float(sd.get("min_duration", 0)), t["crossfade"] * 2 + 1)
        scenes.append(sc)
    scenes[-1].dur += t["outro"]
    pos = 0.0
    for sc in scenes:
        sc.start = pos
        pos += sc.dur - t["crossfade"]
    return scenes


def total_duration(scenes: list[Scene]) -> float:
    return scenes[-1].start + scenes[-1].dur


# ---------------------------------------------------------------- 音声
def mix_audio(story: dict, scenes: list[Scene], out: Path) -> None:
    dur = total_duration(scenes)
    n = int(dur * SR) + SR
    voice = np.zeros(n, dtype=np.float32)
    for sc in scenes:
        for ln in sc.lines:
            s = int((sc.start + ln.start) * SR)
            voice[s:s + len(ln.audio)] += ln.audio
    bcfg = story.get("bgm", {})
    if bcfg.get("enabled", True):
        music = make_bgm(n / SR, bpm=bcfg.get("bpm", 54), volume_db=bcfg.get("volume_db", -30),
                         noise_db=bcfg.get("noise_db", -44), fade_out=story["timing"]["fade_out"] + 1.0)
    else:
        music = np.zeros((n, 2), dtype=np.float32)
    mix = music + voice[:, None] * float(story.get("voice", {}).get("gain", 1.0))
    # 最後はゆっくり音を小さく
    fo = story["timing"]["fade_out"]
    tt = np.arange(n) / SR
    mix *= np.clip((dur - tt) / fo, 0, 1)[:, None]
    peak = np.abs(mix).max()
    if peak > 0.95:
        mix *= 0.95 / peak
    write_wav(out, mix)


# ---------------------------------------------------------------- 絵と字幕
def render_png(svg: str, path: Path, w: int, h: int) -> None:
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(path), output_width=w, output_height=h)


def write_srt(scenes: list[Scene], path: Path, timing: dict) -> None:
    out, n = [], 0
    for sc in scenes:
        for ln in sc.lines:
            if not ln.subtitle:
                continue
            n += 1
            a = sc.start + ln.start - 0.2
            b = sc.start + ln.start + ln.dur + min(ln.pause, 1.2)
            out.append(f"{n}\n{srt_time(max(0, a))} --> {srt_time(b)}\n{ln.text}\n")
    path.write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------- 動画
def _zoompan(motion: str, frames: int, w: int, h: int, fps: int, amount: float = 0.07) -> str:
    p = f"(on/{max(frames - 1, 1)})"
    if motion == "in":
        z, x, y = f"1+{amount}*{p}", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    elif motion == "out":
        z, x, y = f"1+{amount}*(1-{p})", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    elif motion == "left":
        z, x, y = f"{1 + amount}", f"(iw-iw/zoom)*(1-{p})", "(ih-ih/zoom)/2"
    elif motion == "right":
        z, x, y = f"{1 + amount}", f"(iw-iw/zoom)*{p}", "(ih-ih/zoom)/2"
    else:  # still
        z, x, y = "1", "0", "0"
    return f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={w}x{h}:fps={fps}"


def render_scene_clip(sc: Scene, bg: Path, subs: list[tuple[Path, float, float]], out: Path,
                      w: int, h: int, fps: int, crf: int = 14) -> None:
    frames = int(round(sc.dur * fps))
    cmd = [ffmpeg_exe(), "-y", "-v", "error", "-i", str(bg)]
    for path, _, d in subs:
        cmd += ["-loop", "1", "-framerate", str(fps), "-t", f"{d:.3f}", "-i", str(path)]
    fc = [f"[0:v]{_zoompan(sc.motion, frames, w, h, fps)},format=rgb24[v0]"]
    last = "v0"
    for j, (_, a, d) in enumerate(subs, start=1):
        f = min(0.7, d / 3)
        fc.append(f"[{j}:v]format=rgba,fade=t=in:st=0:d={f:.2f}:alpha=1,"
                  f"fade=t=out:st={d - f:.2f}:d={f:.2f}:alpha=1,setpts=PTS-STARTPTS+{a:.3f}/TB[s{j}]")
        fc.append(f"[{last}][s{j}]overlay=0:0:eof_action=pass[v{j}]")
        last = f"v{j}"
    fc.append(f"[{last}]format=yuv420p[out]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[out]", "-frames:v", str(frames),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-r", str(fps), str(out)]
    subprocess.run(cmd, check=True)


def assemble(clips: list[Path], scenes: list[Scene], audio: Path, out: Path, timing: dict, fps: int,
             crf: int = 21, grain: int = 0) -> None:
    cfd = timing["crossfade"]
    dur = total_duration(scenes)
    cmd = [ffmpeg_exe(), "-y", "-v", "error"]
    for c in clips:
        cmd += ["-i", str(c)]
    cmd += ["-i", str(audio)]
    fc, last = [], "0:v"
    for i in range(1, len(clips)):
        fc.append(f"[{last}][{i}:v]xfade=transition=fade:duration={cfd}:offset={scenes[i].start:.3f}[x{i}]")
        last = f"x{i}"
    fo = timing["fade_out"]
    fc.append(f"[{last}]fade=t=in:st=0:d=2,fade=t=out:st={dur - fo:.3f}:d={fo:.3f},"
              + (f"noise=alls={grain}:allf=t," if grain else "") + "format=yuv420p[v]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", f"{len(clips)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-tune", "stillimage",
            "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}",
            "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------------- メイン
def description(story: dict, voice_cfg: dict) -> str:
    credits = ["イラスト・BGM: オリジナル（このプロジェクトで生成）",
               "フォント: Zen Maru Gothic（SIL Open Font License 1.1）"]
    backend = voice_cfg.get("backend", "openjtalk")
    if backend == "openjtalk":
        credits.append("音声合成: Open JTalk / HTS voice tohoku-f01 "
                       "(© Intelligent Communication Network Laboratory, Tohoku University, CC BY 4.0)")
    elif backend == "voicevox":
        credits.append(f"音声: VOICEVOX:{voice_cfg.get('credit_name', '（キャラクター名を記入）')}")
    else:
        credits.append("音声合成: Microsoft Edge 読み上げ（利用規約を確認してください）")
    return (
        f"{story.get('title', '')}\n\n"
        f"{story.get('description', '').strip()}\n\n"
        "3さい〜6さいの おともだちむけの、ねむる まえの よみきかせです。\n"
        "おへやを くらくして、ゆっくり きいてね。 おやすみなさい。\n\n"
        "――\n" + "\n".join(credits) + "\n\n#寝かしつけ #読み聞かせ #絵本 #子守唄 #おやすみ\n"
    )


def build(story_path: Path, out_dir: Path | None, preview: bool, stills_only: bool, jobs: int,
          voice_backend: str | None) -> Path:
    t0 = time.time()
    story = load_story(story_path)
    name = story_path.stem
    out_dir = out_dir or ROOT / "build" / name
    work = out_dir / "work"
    stills = out_dir / "stills"
    for d in (work, stills):
        d.mkdir(parents=True, exist_ok=True)
    vid = story.get("video", {})
    w, h = (1280, 720) if preview else (int(vid.get("width", 1920)), int(vid.get("height", 1080)))
    fps = 24 if preview else int(vid.get("fps", 30))
    use_subs = bool(story.get("subtitles", True))

    print(f"■ 絵をかいています（{len(story['scenes'])} 場面）")
    art_paths = []
    for i, sd in enumerate(story["scenes"]):
        opts = dict(sd.get("art_options", {}))
        if sd["art"] == "title":
            opts.setdefault("title", story.get("title", ""))
            opts.setdefault("subtitle", story.get("subtitle", ""))
        svg = render_scene(sd["art"], **opts)
        render_png(svg, stills / f"{i:02d}_{sd['art']}.png", 1920, 1080)
        p = work / f"bg_{i:02d}.png"
        render_png(svg, p, w * 2, h * 2)  # ズーム用に 2 倍の大きさで
        art_paths.append(p)
    render_png(thumbnail_svg(story.get("title", ""), story.get("thumbnail_badge", "ねむれる おはなし")),
               out_dir / "thumbnail.png", 1280, 720)
    if stills_only:
        print(f"✓ 絵を書き出しました: {stills}")
        return stills

    voice_cfg = dict(story.get("voice", {}))
    if voice_backend:
        voice_cfg["backend"] = voice_backend
    synth = Synthesizer(voice_cfg, ROOT / "build" / ".tts_cache")
    print(f"■ 朗読の音声を作っています（{voice_cfg.get('backend', 'openjtalk')}）")
    scenes = plan(story, synth)
    dur = total_duration(scenes)
    print(f"  → 動画の長さ: {int(dur // 60)} 分 {int(dur % 60)} 秒")

    print("■ 音楽と声をまぜています")
    audio = work / "mix.wav"
    mix_audio(story, scenes, audio)
    write_srt(scenes, out_dir / f"{name}.srt", story["timing"])
    (out_dir / "description.txt").write_text(description(story, voice_cfg), encoding="utf-8")

    print("■ 場面ごとの動画を作っています")
    jobs_list = []
    for sc, bg in zip(scenes, art_paths):
        subs = []
        if use_subs:
            for j, ln in enumerate(sc.lines):
                if not ln.subtitle:
                    continue
                p = work / f"sub_{sc.idx:02d}_{j:02d}.png"
                render_png(subtitle_svg(ln.text), p, w, h)
                a = max(0.0, ln.start - 0.3)
                subs.append((p, a, ln.dur + min(ln.pause, 1.2) + 0.3))
        jobs_list.append((sc, bg, subs, work / f"clip_{sc.idx:02d}.mp4"))
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(render_scene_clip, sc, bg, subs, out, w, h, fps): sc for sc, bg, subs, out in jobs_list}
        for f in cf.as_completed(futs):
            f.result()
            print(f"  場面 {futs[f].idx + 1}/{len(scenes)} できました")

    print("■ ひとつの動画にまとめています")
    final = out_dir / (f"{name}_preview.mp4" if preview else f"{name}.mp4")
    assemble([j[3] for j in jobs_list], scenes, audio, final, story["timing"], fps,
             crf=int(vid.get("crf", 21)), grain=int(vid.get("grain", 0)))
    print(f"✓ 完成: {final}（{time.time() - t0:.0f} 秒かかりました）")
    return final


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="寝かしつけ朗読動画を作ります")
    ap.add_argument("story", type=Path, help="物語の YAML ファイル")
    ap.add_argument("-o", "--out", type=Path, help="出力フォルダ（省略時は build/<物語名>）")
    ap.add_argument("--preview", action="store_true", help="720p / 24fps ですばやく確認用を作る")
    ap.add_argument("--stills-only", action="store_true", help="絵とサムネイルだけ書き出す")
    ap.add_argument("--voice", choices=["openjtalk", "voicevox", "edge"], help="音声合成の方法を上書き")
    ap.add_argument("-j", "--jobs", type=int, default=2, help="同時にレンダリングする場面の数")
    a = ap.parse_args(argv)
    try:
        build(a.story, a.out, a.preview, a.stills_only, a.jobs, a.voice)
    except subprocess.CalledProcessError as e:
        sys.exit(f"ffmpeg でエラーが起きました: {e}")


if __name__ == "__main__":
    main()
