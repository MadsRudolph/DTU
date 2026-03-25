"""
Lecture Recorder & Transcriber for Obsidian
Records audio via ffmpeg, transcribes with Whisper, and saves as Obsidian-formatted markdown.
Supports slide markers during recording for slide-synced transcripts.
"""

import subprocess
import sys
import os
import json
import re
import threading
import time
import tempfile
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
from pathlib import Path

OBSIDIAN_COURSES = Path(r"C:\Users\Mads2\DTU\Obsidian\Courses")
RECORDINGS_DIR = Path(r"C:\Users\Mads2\DTU\lecture-recorder\recordings")
DEFAULT_MICROPHONE = "Analogue 1 + 2 (Focusrite USB Audio)"

# Common ffmpeg install locations on Windows
FFMPEG_SEARCH_PATHS = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe",
    Path(r"C:\ffmpeg\bin\ffmpeg.exe"),
    Path(r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"),
    Path(os.environ.get("USERPROFILE", "")) / "scoop" / "shims" / "ffmpeg.exe",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "ffmpeg" / "bin" / "ffmpeg.exe",
]

_ffmpeg_cache: str | None = None


def _find_ffmpeg() -> str:
    """Find ffmpeg binary — check PATH first, then common Windows install locations."""
    global _ffmpeg_cache
    if _ffmpeg_cache:
        return _ffmpeg_cache

    # 1. Check PATH
    path = shutil.which("ffmpeg")
    if path:
        _ffmpeg_cache = path
        return path

    # 2. Check known static paths
    for p in FFMPEG_SEARCH_PATHS:
        if p.exists():
            _ffmpeg_cache = str(p)
            return _ffmpeg_cache

    # 3. Search winget packages directory (where Gyan.FFmpeg installs)
    winget_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    if winget_dir.exists():
        for ffmpeg_exe in winget_dir.rglob("ffmpeg.exe"):
            _ffmpeg_cache = str(ffmpeg_exe)
            return _ffmpeg_cache

    return "ffmpeg"  # fall back to bare name, let Popen raise FileNotFoundError
LOOPBACK_KEYWORDS = ["stereo mix", "virtual", "cable", "voicemeeter", "loopback", "what u hear", "wave out"]
MIC_KEYWORDS = ["microphone", "mic", "realtek", "headset", "focusrite", "scarlett", "usb audio"]


def list_audio_devices() -> list[str]:
    """List audio input devices using sounddevice (PortAudio), with ffmpeg fallback."""
    devices = _list_devices_sounddevice()
    if not devices:
        devices = _list_devices_ffmpeg()
    return devices or [DEFAULT_MICROPHONE]


def _list_devices_sounddevice() -> list[str]:
    """List audio input devices via sounddevice (PortAudio) — most reliable on Windows."""
    try:
        import sounddevice as sd  # noqa: requires `pip install sounddevice`
        seen_full = set()  # exact name dedup
        devices = []
        for d in sd.query_devices():
            if d["max_input_channels"] > 0:
                name = d["name"]
                # Skip system mappers, garbled names, and generic inputs
                if ("sound mapper" in name.lower()
                        or "primary" in name.lower()
                        or name.startswith("Input (@")
                        or name.startswith("Input ()")
                        or name.startswith("Headset (@")):
                    continue
                # Skip truncated duplicates: if "Analogue 1 + 2 (Focusrite USB Audio)"
                # is already in list, skip "Analogue 1 + 2 (Focusrite USB A"
                is_truncated = False
                for existing in list(seen_full):
                    if existing.startswith(name) and existing != name:
                        is_truncated = True
                        break
                    if name.startswith(existing) and existing != name:
                        # The new name is the full version — replace the truncated one
                        devices.remove(existing)
                        seen_full.discard(existing)
                        break
                if is_truncated:
                    continue
                if name not in seen_full:
                    seen_full.add(name)
                    devices.append(name)
        return devices
    except Exception:
        return []


def _get_sounddevice_index(name: str) -> int | None:
    """Get the sounddevice device index for a given device name."""
    try:
        import sounddevice as sd
        for i, d in enumerate(sd.query_devices()):
            if d["max_input_channels"] > 0 and d["name"] == name:
                return i
    except Exception:
        pass
    return None


def _get_dshow_name(device_name: str) -> str:
    """Map a sounddevice name to its ffmpeg dshow name. They're usually the same,
    but sounddevice may truncate long names. This does a fuzzy match against dshow."""
    try:
        result = subprocess.run(
            [_find_ffmpeg(), "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
            capture_output=True, text=True, timeout=10,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        for line in result.stderr.splitlines():
            if '"' in line and "Alternative name" not in line:
                match = re.search(r'"(.+?)"', line)
                if match:
                    dshow_name = match.group(1)
                    # Exact match or sounddevice truncated version
                    if dshow_name == device_name or dshow_name.startswith(device_name):
                        return dshow_name
                    if device_name.startswith(dshow_name):
                        return dshow_name
    except Exception:
        pass
    return device_name  # fallback: use as-is


def _list_devices_ffmpeg() -> list[str]:
    """Fallback: list audio devices via ffmpeg DirectShow."""
    try:
        result = subprocess.run(
            [_find_ffmpeg(), "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
            capture_output=True, text=True, timeout=10,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        output = result.stderr
        devices = []
        in_audio = False
        for line in output.splitlines():
            if "DirectShow audio devices" in line:
                in_audio = True
                continue
            if "DirectShow video devices" in line:
                in_audio = False
                continue
            if in_audio and '"' in line and "Alternative name" not in line:
                match = re.search(r'"(.+?)"', line)
                if match:
                    devices.append(match.group(1))
        return devices
    except Exception:
        return []

COURSES = {
    "34315": {"name": "Internet of Things", "prefix": "Lecture", "short": "IoT"},
    "34620": {"name": "Basic Power Electronics", "prefix": "Lecture", "short": "BPE"},
    "34655": {"name": "Integrated Analog Electronics 2", "prefix": "Lecture", "short": "IAE2"},
    "34722": {"name": "Linear Control Design 1", "prefix": "Lesson", "short": "LCD"},
    "62711": {"name": "Digital Systems Design", "prefix": "Lecture", "short": "DSD"},
    "62743": {"name": "Digital Signal Processing (Reexam)", "prefix": "Lecture", "short": "DSP"},
}

WHISPER_MODELS = ["tiny", "base", "small", "medium", "large", "api"]

# Domain vocabulary per course — passed as initial_prompt to Whisper for better accuracy
COURSE_VOCAB = {
    "34315": "IoT, Internet of Things, microcontroller, Arduino, sensor, actuator, WiFi, Bluetooth, MQTT, GPIO, ADC, DAC, SPI, I2C, UART, PWM",
    "34620": "power electronics, MOSFET, IGBT, diode, rectifier, inverter, DC-DC converter, buck, boost, duty cycle, switching frequency, PWM, inductor, capacitor, transformer",
    "34655": "CMOS, NMOS, PMOS, OpAmp, operational amplifier, transconductance, gm, gain-bandwidth, slew rate, common-mode, differential, feedback, bias current, noise, flicker noise, thermal noise, layout, fabrication, Cadence, Virtuoso",
    "34722": "Laplace transform, transfer function, Bode plot, Nyquist plot, gain margin, phase margin, P-controller, PI-controller, PID-controller, feedback, open-loop, closed-loop, stability, poles, zeros, step response, frequency response, block diagram",
    "62711": "VHDL, FPGA, digital design, combinational, sequential, flip-flop, register, multiplexer, decoder, ALU, datapath, FSM, finite state machine, timing, clock, synthesis, simulation, testbench",
    "62743": "DFT, discrete Fourier transform, FFT, fast Fourier transform, z-transform, FIR, IIR, filter, convolution, sampling, aliasing, Nyquist, frequency response, magnitude, phase, poles, zeros, transfer function",
}

LANGUAGE_CODES = {
    "English": "en", "Danish": "da", "German": "de", "French": "fr",
    "Spanish": "es", "Italian": "it", "Portuguese": "pt", "Dutch": "nl",
    "Swedish": "sv", "Norwegian": "no", "Finnish": "fi", "Polish": "pl",
}


# ── Core functions ──────────────────────────────────────────────────

def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def find_next_lecture_number(course_id: str) -> int:
    course = COURSES[course_id]
    lecture_dir = OBSIDIAN_COURSES / f"{course_id} {course['name']}" / "Lecture Notes"
    if not lecture_dir.exists():
        return 1
    max_num = 0
    prefix = course["prefix"]
    for f in lecture_dir.glob("*.md"):
        name = f.stem
        if name.startswith(prefix):
            parts = name.split(" - ", 1)
            if parts:
                num_str = parts[0].replace(prefix, "").strip()
                try:
                    max_num = max(max_num, int(num_str))
                except ValueError:
                    pass
    return max_num + 1


def get_slides_dir(course_id: str) -> Path:
    course = COURSES[course_id]
    return OBSIDIAN_COURSES / f"{course_id} {course['name']}" / "Slides"


def list_course_pdfs(course_id: str) -> list[Path]:
    slides_dir = get_slides_dir(course_id)
    if not slides_dir.exists():
        return []
    return sorted(slides_dir.glob("*.pdf"), key=lambda p: p.name.lower())


import re

# Regex patterns per course for extracting lecture number from PDF filenames
PDF_LECTURE_PATTERNS = {
    "34722": [r"^(\d+)_", r"Lecture_0*(\d+)"],
    "62711": [r"62711_lesson(\d+)", r"lesson[_ ]?(\d+)"],
    "34655": [r"34655-0*(\d+)"],
    "34315": [],
    "34620": [],
    "62743": [],
}


def match_pdf_to_lecture(course_id: str, lecture_num: int, pdfs: list[Path]) -> Path | None:
    patterns = PDF_LECTURE_PATTERNS.get(course_id, [])
    for pdf in pdfs:
        name = pdf.stem
        for pattern in patterns:
            m = re.search(pattern, name, re.IGNORECASE)
            if m and int(m.group(1)) == lecture_num:
                return pdf
    # Fallback: try any number in filename
    if not patterns:
        for pdf in pdfs:
            m = re.search(r"(\d+)", pdf.stem)
            if m and int(m.group(1)) == lecture_num:
                return pdf
    return None


def count_pdf_pages(pdf_path: Path) -> int:
    try:
        from PyPDF2 import PdfReader
        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        return 0


# ── Speed normalization ────────────────────────────────────────────

PLAYBACK_SPEEDS = ["1×", "1.25×", "1.5×", "1.75×", "2×"]


def normalize_audio_speed(audio_path: Path, speed: float) -> Path:
    """Slow down audio recorded at higher playback speed back to 1× for transcription.

    Uses ffmpeg atempo filter.  atempo only accepts 0.5–2.0, so for speeds
    > 2× we chain multiple atempo filters (not needed here but future-proof).

    Returns path to the normalized file (or the original if speed == 1.0).
    """
    if abs(speed - 1.0) < 0.01:
        return audio_path  # already 1×

    tempo = 1.0 / speed  # e.g. speed=2.0 → tempo=0.5 (slow down)

    # Chain atempo filters if factor outside 0.5–2.0 range
    filters = []
    remaining = tempo
    while remaining < 0.5:
        filters.append("atempo=0.5")
        remaining /= 0.5
    while remaining > 2.0:
        filters.append("atempo=2.0")
        remaining /= 2.0
    filters.append(f"atempo={remaining:.4f}")
    filter_str = ",".join(filters)

    normalized_path = audio_path.with_name("recording_normalized" + audio_path.suffix)
    ffmpeg_bin = _find_ffmpeg()
    cmd = [
        ffmpeg_bin,
        "-i", str(audio_path),
        "-filter:a", filter_str,
        "-y", str(normalized_path),
    ]
    print(f"[speed] Normalizing {speed}× → 1×  (atempo filter: {filter_str})")
    result = subprocess.run(cmd, capture_output=True, timeout=600,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg speed normalization failed:\n{result.stderr.decode(errors='replace')}")
    print(f"[speed] Normalized audio saved: {normalized_path.name}")
    return normalized_path


def scale_slide_markers(markers: list[tuple[int, float]], speed: float) -> list[tuple[int, float]]:
    """Scale slide marker timestamps from sped-up recording time to real lecture time.

    E.g. at 2× playback, a marker at 30 s elapsed really corresponds to 60 s of lecture.
    """
    if abs(speed - 1.0) < 0.01:
        return markers
    return [(slide, elapsed * speed) for slide, elapsed in markers]


# ── Transcription ──────────────────────────────────────────────────

def transcribe_audio(audio_path: Path, model: str = "base", language: str = "English",
                      course_id: str | None = None) -> dict:
    import whisper
    model_obj = whisper.load_model(model)
    kwargs = {"language": language}
    if course_id and course_id in COURSE_VOCAB:
        kwargs["initial_prompt"] = COURSE_VOCAB[course_id]
    return model_obj.transcribe(str(audio_path), **kwargs)


def transcribe_audio_api(audio_path: Path, language: str = "English",
                          course_id: str | None = None) -> dict:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # OpenRouter keys don't support Whisper API
    if api_key.startswith("sk-or-"):
        raise ValueError("OpenRouter doesn't support Whisper API. Use a direct OpenAI API key (sk-proj-...) or switch to a local Whisper model.")

    client = OpenAI(api_key=api_key)
    lang_code = LANGUAGE_CODES.get(language, language[:2].lower())
    prompt = COURSE_VOCAB.get(course_id, "") if course_id else ""

    max_size = 25 * 1024 * 1024  # 25MB
    file_size = audio_path.stat().st_size

    if file_size <= max_size:
        return _transcribe_chunk_api(client, audio_path, lang_code, prompt)

    # Split large files into 10-minute chunks
    return _transcribe_chunked_api(client, audio_path, lang_code, prompt)


def _transcribe_chunk_api(client, audio_path: Path, lang_code: str, prompt: str = "") -> dict:
    kwargs = {
        "model": "whisper-1",
        "language": lang_code,
        "response_format": "verbose_json",
        "timestamp_granularities": ["segment"],
    }
    if prompt:
        kwargs["prompt"] = prompt
    with open(audio_path, "rb") as f:
        kwargs["file"] = f
        response = client.audio.transcriptions.create(**kwargs)

    segments = []
    for seg in getattr(response, "segments", []):
        segments.append({
            "start": seg.get("start", seg.get("Start", 0)),
            "end": seg.get("end", seg.get("End", 0)),
            "text": seg.get("text", seg.get("Text", "")),
        })

    return {"text": response.text, "segments": segments}


def _transcribe_chunked_api(client, audio_path: Path, lang_code: str, prompt: str = "") -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        chunk_pattern = os.path.join(tmpdir, "chunk_%03d.mp3")
        subprocess.run([
            "ffmpeg", "-i", str(audio_path),
            "-f", "segment", "-segment_time", "600",
            "-c", "copy", chunk_pattern,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

        chunks = sorted(Path(tmpdir).glob("chunk_*.mp3"))
        all_text = []
        all_segments = []
        time_offset = 0.0

        for chunk_path in chunks:
            result = _transcribe_chunk_api(client, chunk_path, lang_code, prompt)
            all_text.append(result["text"])

            for seg in result["segments"]:
                all_segments.append({
                    "start": seg["start"] + time_offset,
                    "end": seg["end"] + time_offset,
                    "text": seg["text"],
                })

            # Get chunk duration for offset
            if result["segments"]:
                time_offset += result["segments"][-1]["end"]

    return {"text": " ".join(all_text), "segments": all_segments}


# ── Speaker Diarization ────────────────────────────────────────────

def diarize_audio(audio_path: Path) -> list[dict]:
    from pyannote.audio import Pipeline
    import torch

    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN environment variable not set (needed for pyannote.audio)")

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token)

    # Try loading audio via torchaudio first (works better on Windows where torchcodec may fail)
    try:
        import torchaudio
        waveform, sample_rate = torchaudio.load(str(audio_path))
        audio_input = {"waveform": waveform, "sample_rate": sample_rate}
    except Exception:
        # Fall back to letting pyannote handle it directly
        audio_input = str(audio_path)

    diarization = pipeline(audio_input)

    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({"start": turn.start, "end": turn.end, "speaker": speaker})
    return segments


def merge_diarization_with_transcript(transcript_segments: list[dict],
                                       diarization: list[dict]) -> list[dict]:
    if not diarization:
        return transcript_segments

    # Find the most frequent speaker (assumed to be the lecturer)
    from collections import Counter
    speaker_durations: dict[str, float] = {}
    for d in diarization:
        speaker_durations[d["speaker"]] = speaker_durations.get(d["speaker"], 0) + (d["end"] - d["start"])

    sorted_speakers = sorted(speaker_durations, key=speaker_durations.get, reverse=True)
    lecturer_id = sorted_speakers[0] if sorted_speakers else None

    # Build speaker labels
    speaker_labels = {}
    student_num = 0
    for spk in sorted_speakers:
        if spk == lecturer_id:
            speaker_labels[spk] = "Lecturer"
        else:
            student_num += 1
            speaker_labels[spk] = f"Student{' ' + str(student_num) if student_num > 1 else ''}"

    # Assign speaker to each transcript segment by majority overlap
    merged = []
    for seg in transcript_segments:
        seg_start, seg_end = seg["start"], seg["end"]
        overlap_by_speaker: dict[str, float] = {}

        for d in diarization:
            overlap_start = max(seg_start, d["start"])
            overlap_end = min(seg_end, d["end"])
            if overlap_start < overlap_end:
                overlap = overlap_end - overlap_start
                overlap_by_speaker[d["speaker"]] = overlap_by_speaker.get(d["speaker"], 0) + overlap

        if overlap_by_speaker:
            best_speaker = max(overlap_by_speaker, key=overlap_by_speaker.get)
            speaker = speaker_labels.get(best_speaker, "Unknown")
        else:
            speaker = "Lecturer"  # Default if no overlap found

        merged.append({**seg, "speaker": speaker})

    return merged


# ── Markdown Builder ───────────────────────────────────────────────

def build_markdown(course_id: str, lecture_num: int, title: str, result: dict,
                   audio_path: Path, slide_markers: list[tuple[int, float]] | None = None) -> str:
    """Build Obsidian-formatted markdown. slide_markers is a list of (slide_number, timestamp_seconds)."""
    course = COURSES[course_id]
    prefix = course["prefix"]
    short = course["short"]
    date = datetime.now().strftime("%Y-%m-%d")

    segments = result.get("segments", [])
    full_title = f"{prefix} {lecture_num} - {title}" if title else f"{prefix} {lecture_num}"

    # Build transcript body
    if slide_markers and segments:
        transcript_body = _build_slide_synced_transcript(segments, slide_markers)
    elif segments:
        lines = []
        for seg in segments:
            ts = format_timestamp(seg["start"])
            text = seg["text"].strip()
            if not text:
                continue
            speaker = seg.get("speaker")
            if speaker:
                lines.append(f"**[{ts}] {speaker}:** {text}")
            else:
                lines.append(f"**[{ts}]** {text}")
        transcript_body = "\n\n".join(lines)
    else:
        transcript_body = result.get("text", "")

    # Navigation
    prev_num = lecture_num - 1
    prev_link = ""
    if prev_num >= 1:
        lecture_dir = OBSIDIAN_COURSES / f"{course_id} {course['name']}" / "Lecture Notes"
        for f in lecture_dir.glob(f"{prefix} {prev_num}*"):
            prev_link = f"[[{f.stem}|← {prefix} {prev_num}]]"
            break
        if not prev_link:
            for f in lecture_dir.glob(f"{prefix} {prev_num:02d}*"):
                prev_link = f"[[{f.stem}|← {prefix} {prev_num}]]"
                break

    slide_count = ""
    if slide_markers:
        slide_count = f"\n> **Slides marked:** {len(slide_markers)}"

    md = f"""---
course: "{course_id}"
course-name: "{course['name']}"
type: lecture-note
{prefix.lower()}: {lecture_num}
tags: [{short}, lecture, transcript]
date: {date}
---
# {full_title}

**Course:** {course_id} {course['name']}
**Date:** {date}

> [!abstract] {prefix} Overview
> Auto-transcribed lecture recording. Review and edit the transcript below to create structured notes.

> [!info] Source Recording
> `{audio_path.name}`{slide_count}

---

## Transcript

{transcript_body}

---

## Notes

> [!todo] Post-Processing
> - [ ] Review transcript for errors
> - [ ] Add section headings
> - [ ] Add equations and diagrams
> - [ ] Extract key takeaways
> - [ ] Link to related notes and slides

---

> [!nav]
> &nbsp;
>
> {prev_link}
>
> [[{course_id} {course['name']}|{course_id} Home]]
>
> [[{full_title}|{prefix} {lecture_num} →]]
"""
    return md


def _build_slide_synced_transcript(segments: list[dict], slide_markers: list[tuple[int, float]]) -> str:
    """Merge whisper segments with slide markers into slide-grouped sections."""
    # Sort markers by timestamp
    markers = sorted(slide_markers, key=lambda m: m[1])

    # Build list of (slide_num, start_time, end_time)
    slide_ranges = []
    for i, (slide_num, start) in enumerate(markers):
        end = markers[i + 1][1] if i + 1 < len(markers) else float("inf")
        slide_ranges.append((slide_num, start, end))

    # Assign each segment to a slide
    slide_segments: dict[int, list[str]] = {}
    # Segments before the first marker go under a "Before slides" section
    pre_marker_lines = []

    for seg in segments:
        ts = format_timestamp(seg["start"])
        text = seg["text"].strip()
        if not text:
            continue

        speaker = seg.get("speaker")
        if speaker:
            line = f"**[{ts}] {speaker}:** {text}"
        else:
            line = f"**[{ts}]** {text}"
        seg_time = seg["start"]

        assigned = False
        for slide_num, s_start, s_end in slide_ranges:
            if s_start <= seg_time < s_end:
                slide_segments.setdefault(slide_num, []).append(line)
                assigned = True
                break

        if not assigned:
            # Before the first slide marker
            pre_marker_lines.append(line)

    # Build output
    parts = []

    if pre_marker_lines:
        parts.append("\n\n".join(pre_marker_lines))

    for slide_num, s_start, _ in slide_ranges:
        slide_ts = format_timestamp(s_start)
        parts.append(f"### Slide {slide_num} — `{slide_ts}`")
        lines = slide_segments.get(slide_num, [])
        if lines:
            parts.append("\n\n".join(lines))
        else:
            parts.append("*(no speech detected)*")

    return "\n\n".join(parts)


def save_transcript(course_id: str, lecture_num: int, title: str, markdown: str) -> Path:
    course = COURSES[course_id]
    prefix = course["prefix"]
    full_title = f"{prefix} {lecture_num} - {title}" if title else f"{prefix} {lecture_num}"

    lecture_dir = OBSIDIAN_COURSES / f"{course_id} {course['name']}" / "Lecture Notes"
    lecture_dir.mkdir(parents=True, exist_ok=True)

    output_path = lecture_dir / f"{full_title}.md"

    if output_path.exists():
        ts = datetime.now().strftime("%H%M%S")
        output_path = lecture_dir / f"{full_title} ({ts}).md"

    output_path.write_text(markdown, encoding="utf-8")
    return output_path


# ── Structured Output ──────────────────────────────────────────────

def _build_slide_sections_data(segments: list[dict],
                                slide_markers: list[tuple[int, float]]) -> list[dict]:
    if not slide_markers or not segments:
        return []

    markers = sorted(slide_markers, key=lambda m: m[1])
    sections = []

    for i, (slide_num, start) in enumerate(markers):
        end = markers[i + 1][1] if i + 1 < len(markers) else float("inf")
        slide_segs = [s for s in segments if start <= s["start"] < end]
        text = " ".join(s["text"].strip() for s in slide_segs if s["text"].strip())
        sections.append({
            "slide": slide_num,
            "start_time": start,
            "end_time": end if end != float("inf") else (segments[-1]["end"] if segments else start),
            "transcript": text,
            "segments": slide_segs,
        })

    return sections


def save_structured_output(course_id: str, lecture_num: int, title: str,
                           result: dict, audio_path: Path,
                           slide_markers: list[tuple[int, float]] | None = None,
                           pdf_path: Path | None = None,
                           total_slides: int = 0) -> Path:
    course = COURSES[course_id]
    prefix = course["prefix"]
    segments = result.get("segments", [])

    # Compute audio duration from last segment
    duration = segments[-1]["end"] if segments else 0.0

    slide_sections = _build_slide_sections_data(segments, slide_markers or [])

    data = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "course": {
            "id": course_id,
            "name": course["name"],
            "short": course["short"],
        },
        "lecture": {
            "number": lecture_num,
            "title": title,
            "prefix": prefix,
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
        "audio": {
            "filename": audio_path.name,
            "duration_seconds": round(duration, 1),
        },
        "slides": {
            "pdf_filename": pdf_path.name if pdf_path else None,
            "total_pages": total_slides,
            "markers": [
                {"slide": s, "timestamp": round(t, 1), "timestamp_formatted": format_timestamp(t)}
                for s, t in (slide_markers or [])
            ],
        },
        "transcript": {
            "full_text": result.get("text", ""),
            "segments": [
                {
                    "start": round(s["start"], 2),
                    "end": round(s["end"], 2),
                    "text": s["text"].strip(),
                    **({"speaker": s["speaker"]} if "speaker" in s else {}),
                }
                for s in segments if s.get("text", "").strip()
            ],
        },
        "slide_sections": slide_sections,
    }

    output_path = audio_path.parent / "structured.json"
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_path


def save_prompt_template(course_id: str, lecture_num: int, title: str,
                         json_path: Path, pdf_path: Path | None = None) -> Path:
    course = COURSES[course_id]
    prefix = course["prefix"]
    short = course["short"]
    full_title = f"{prefix} {lecture_num} - {title}" if title else f"{prefix} {lecture_num}"

    pdf_section = ""
    if pdf_path:
        pdf_section = f"""
- **Lecture slides PDF**: [[{pdf_path.name}]]
  - Read the PDF slides FIRST to understand the structure, formulas, and exact numerical values
  - The slides are the authoritative source for equations, variable names, and notation
  - Embed key slides in the notes using `![[{pdf_path.name}#page=N]]` for visual reference"""

    # Find existing lecture notes to use as style reference
    lecture_dir = OBSIDIAN_COURSES / f"{course_id} {course['name']}" / "Lecture Notes"
    style_ref = ""
    if lecture_dir.exists():
        existing = sorted(lecture_dir.glob(f"{prefix} *.md"))
        # Pick a note that isn't auto-generated (not this one, prefer lower numbers)
        for note in existing:
            if str(lecture_num) not in note.stem.split("-")[0]:
                style_ref = f"\n- **Style reference**: Read `{note.name}` in the Lecture Notes folder for formatting conventions"
                break

    prompt = f"""# Lecture Note Generation — {full_title}

Create comprehensive, study-ready lecture notes for **{course_id} {course['name']}**, {full_title}.

## Source Data (read ALL of these)
- **Transcript**: `transcript.txt` — the full lecture transcription
- **Structured data**: `{json_path.name}` — transcript with timestamps and slide markers{pdf_section}{style_ref}

## Critical Instructions

### 1. Use BOTH transcript AND slides
- Read the **transcript** for the lecturer's explanations, intuitions, analogies, and verbal emphasis
- Read the **PDF slides** for precise equations, exact numerical values, variable notation, and Bode plot data
- The transcript captures WHAT the lecturer said; the slides capture the EXACT math
- When the transcript says approximate numbers, prefer the exact values from slides

### 2. Organize by TOPIC, not by slide
- Group content into logical conceptual sections (e.g., "P Controller Design", "PI Controller Design")
- Do NOT create one section per slide — slides often span the same topic across multiple pages
- Use the lecturer's verbal transitions ("now let's move to...", "the next thing is...") to identify topic boundaries
- Number sections hierarchically: `## 1. Topic`, `### 1.1 Subtopic`

### 3. Include the lecturer's intuition and emphasis
- Capture WHY things work, not just the formulas
- Include the lecturer's analogies, physical interpretations, and "how to think about this"
- Note when the lecturer says something is "important", "the key point", "remember this for the exam"
- Include practical advice and engineering rules of thumb

### 4. Worked examples with exact values
- Include ALL worked examples from the lecture with step-by-step solutions
- Use the **exact numerical values** from the slides (e.g., $\\omega_c = 5.29484$ rad/s, not "about 5.3")
- Show the complete calculation chain: specification → phase balance → Bode lookup → parameter calculation
- Include intermediate results

### 5. Formatting requirements
- **YAML frontmatter**:
  ```yaml
  ---
  course: "{course_id}"
  course-name: "{course['name']}"
  type: lecture-note
  lesson: {lecture_num}
  tags: [{short}, lecture]
  date: YYYY-MM-DD
  ---
  ```
- **Obsidian callout boxes** — use these extensively:
  - `> [!abstract]` for lecture overview at the top
  - `> [!tip]` for practical advice, MATLAB tips, analogies
  - `> [!warning]` for common mistakes, unit confusion, exam pitfalls
  - `> [!important]` for key results and theorems
  - `> [!info]` for supplementary context or teasers for future lectures
  - `> [!example]` for related materials (slides, exercises, previous lectures)
- **LaTeX equations**: use `$$...$$` for display math, `$...$` for inline
- **Tables** for comparing concepts, parameter effects, numerical results
- **Embedded slides**: `![[{pdf_path.name if pdf_path else 'slides.pdf'}#page=N]]` for key visual content (Bode plots, block diagrams, step responses)
- **MATLAB code blocks** when the lecturer shows MATLAB commands
- **Bold key terms** on first introduction

### 6. Structure template
```
# {full_title}

> [!abstract] Lecture Overview
> {prefix} N/13 — Teacher: ...
> Topics: ...

> [!example] Related Materials
> - Slides: [[...pdf]]
> - Exercise: [[...]]
> - Previous: [[...]]

---

## 1. First Major Topic
### 1.1 Subtopic
[Content with equations, explanations, callouts]

## 2. Second Major Topic
[...]

## N. Summary / Key Takeaways
[Concise summary table or bullet points]

## N+1. MATLAB Workflow
[Practical code for the lecture's design procedures]

## N+2. Exercise Preview
[What today's exercise covers]
```

### 7. What NOT to do
- Do NOT organize by slide number
- Do NOT include timestamps in the notes (they clutter the reading experience)
- Do NOT reproduce the transcript verbatim — synthesize and restructure
- Do NOT skip the lecturer's verbal explanations in favor of just copying slide content
- Do NOT use generic placeholder text — every section should have real content
- Do NOT add emojis

## Output
Save as: `{full_title}.md`
"""

    output_path = json_path.parent / "prompt.md"
    output_path.write_text(prompt, encoding="utf-8")
    return output_path


# ── Claude Enhancement ─────────────────────────────────────────────

def enhance_notes_with_claude(json_path: Path, course_id: str, lecture_num: int,
                              title: str, pdf_path: Path | None = None) -> str:
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    course = COURSES[course_id]
    prefix = course["prefix"]
    short = course["short"]
    full_title = f"{prefix} {lecture_num} - {title}" if title else f"{prefix} {lecture_num}"
    date = data["lecture"]["date"]

    # Build the structured data summary for the prompt
    transcript_json = json.dumps(data["slide_sections"] or data["transcript"]["segments"],
                                  indent=1, ensure_ascii=False)

    slide_info = ""
    pdf_embed_name = "slides.pdf"
    if data["slides"]["pdf_filename"]:
        pdf_embed_name = data["slides"]["pdf_filename"]
        slide_info = f"- Slides PDF: {pdf_embed_name} ({data['slides']['total_pages']} pages/slides)\n"
        slide_info += f"- Slide markers recorded: {len(data['slides']['markers'])}\n"

    prompt = f"""You are creating comprehensive, study-ready lecture notes from a transcript.
These notes should be the ONLY resource a student needs to study this lecture.

## Context
- Course: {course_id} {course['name']}
- {prefix}: {lecture_num} — {title}
- Date: {date}
{slide_info}
## Transcript Data (JSON)
{transcript_json}

## Critical Requirements

### Content Quality
- Organize by TOPIC/CONCEPT, NOT by slide number — group related content logically
- Capture the lecturer's intuition, analogies, and physical interpretations — not just formulas
- Include ALL worked examples with step-by-step solutions and exact numerical values
- Note when the lecturer emphasizes something as important, key, or exam-relevant
- Include practical engineering advice and rules of thumb
- Add MATLAB code blocks when the lecturer demonstrates commands

### Formatting
1. Start with this exact YAML frontmatter:
---
course: "{course_id}"
course-name: "{course['name']}"
type: lecture-note
{prefix.lower()}: {lecture_num}
tags: [{short}, lecture]
date: {date}
---

2. Use `# {full_title}` as the main heading
3. Start with an `> [!abstract] Lecture Overview` callout summarizing the lecture
4. Add `> [!example] Related Materials` linking to slides and exercises
5. Use numbered `##` sections and `###` subsections for topics
6. Use Obsidian callout boxes extensively:
   - `> [!tip]` for practical advice, MATLAB tips, analogies
   - `> [!warning]` for common mistakes, unit confusion, exam pitfalls
   - `> [!important]` for key results and theorems
   - `> [!info]` for supplementary context
7. Format equations: `$$...$$` for display math, `$...$` for inline
8. Use tables for comparing concepts and parameter effects
9. Embed key slides: `![[{pdf_embed_name}#page=N]]` for Bode plots, block diagrams, step responses
10. Bold key terms on first introduction
11. Do NOT include timestamps — they clutter the reading experience
12. Do NOT use emojis
13. End with a summary section and MATLAB workflow section

Generate ONLY the markdown content, no explanations or preamble."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16384,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def save_enhanced_notes(course_id: str, lecture_num: int, title: str,
                        enhanced_md: str) -> Path:
    course = COURSES[course_id]
    prefix = course["prefix"]
    full_title = f"{prefix} {lecture_num} - {title}" if title else f"{prefix} {lecture_num}"

    lecture_dir = OBSIDIAN_COURSES / f"{course_id} {course['name']}" / "Lecture Notes"
    lecture_dir.mkdir(parents=True, exist_ok=True)

    output_path = lecture_dir / f"{full_title}.md"

    if output_path.exists():
        ts = datetime.now().strftime("%H%M%S")
        output_path = lecture_dir / f"{full_title} ({ts}).md"

    output_path.write_text(enhanced_md, encoding="utf-8")
    return output_path


# ── GUI ─────────────────────────────────────────────────────────────

class LectureRecorderApp:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Lecture Recorder")
        self.root.geometry("660x1000")
        self.root.resizable(False, False)

        self.recording = False
        self.ffmpeg_proc = None
        self.audio_path = None
        self.record_start_time = None
        self.timer_id = None

        # Startup diagnostics
        print(f"[startup] ffmpeg: {_find_ffmpeg()}")
        print(f"[startup] devices: {list_audio_devices()}")

        # Slide markers: list of (slide_number, elapsed_seconds)
        self.slide_markers: list[tuple[int, float]] = []
        self.current_slide = 0

        # PDF tracking
        self.selected_pdf_path: Path | None = None
        self.total_slide_count: int = 0

        self._build_ui()
        self._update_lecture_number()
        self._update_pdf_list()
        self._try_auto_select_pdf()

        # Auto-match PDF when lecture number changes
        self.num_var.trace_add("write", lambda *_: self._try_auto_select_pdf())

        # Keyboard shortcut: Right arrow or Space for next slide
        self.root.bind("<Right>", lambda e: self._mark_next_slide())
        self.root.bind("<Left>", lambda e: self._undo_last_slide())

    def _build_ui(self):
        # ── Header ──
        header = ctk.CTkFrame(self.root, fg_color="#1a1a2e", height=60, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="Lecture Recorder", font=("Segoe UI", 20, "bold"),
                 text_color="white").pack(pady=15)

        # ── Main frame ──
        main = ctk.CTkFrame(self.root, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Course selector
        ctk.CTkLabel(main, text="Course", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.course_var = tk.StringVar()
        course_values = [f"{cid} — {info['name']}" for cid, info in sorted(COURSES.items())]
        self.course_combo = ctk.CTkComboBox(main, variable=self.course_var, values=course_values, state="readonly", width=400)
        self.course_combo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.course_combo.bind("<<ComboboxSelected>>", lambda e: self._on_course_changed())

        # Lecture number + title
        num_title_frame = ctk.CTkFrame(main, fg_color="transparent")
        num_title_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        ctk.CTkLabel(num_title_frame, text="#", font=("Segoe UI", 12)).pack(side="left")
        self.num_var = tk.StringVar()
        self.num_entry = ctk.CTkEntry(num_title_frame, textvariable=self.num_var, width=60)
        self.num_entry.pack(side="left", padx=(5, 20))

        ctk.CTkLabel(num_title_frame, text="Title", font=("Segoe UI", 12)).pack(side="left")
        self.title_var = tk.StringVar()
        ctk.CTkEntry(num_title_frame, textvariable=self.title_var).pack(side="left", padx=(5, 0), fill="x", expand=True)

        # Whisper model + language + start slide
        model_lang_frame = ctk.CTkFrame(main, fg_color="transparent")
        model_lang_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        ctk.CTkLabel(model_lang_frame, text="Model", font=("Segoe UI", 12)).pack(side="left")
        self.model_var = tk.StringVar(value="base")
        ctk.CTkComboBox(model_lang_frame, variable=self.model_var, values=WHISPER_MODELS, state="readonly", width=100).pack(side="left", padx=(5, 20))

        ctk.CTkLabel(model_lang_frame, text="Language", font=("Segoe UI", 12)).pack(side="left")
        self.lang_var = tk.StringVar(value="English")
        ctk.CTkEntry(model_lang_frame, textvariable=self.lang_var, width=100).pack(side="left", padx=(5, 20))

        ctk.CTkLabel(model_lang_frame, text="Start slide", font=("Segoe UI", 12)).pack(side="left")
        self.start_slide_var = tk.StringVar(value="1")
        ctk.CTkEntry(model_lang_frame, textvariable=self.start_slide_var, width=50).pack(side="left", padx=(5, 0))

        # Playback speed (for recording sped-up lectures)
        speed_frame = ctk.CTkFrame(main, fg_color="transparent")
        speed_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        ctk.CTkLabel(speed_frame, text="⏩ Playback Speed", font=("Segoe UI", 12)).pack(side="left")
        self.speed_var = tk.StringVar(value="1×")
        self.speed_combo = ctk.CTkComboBox(speed_frame, variable=self.speed_var,
                                            values=PLAYBACK_SPEEDS, state="readonly", width=80)
        self.speed_combo.pack(side="left", padx=(10, 10))
        self.speed_hint = ctk.CTkLabel(speed_frame, text="", font=("Segoe UI", 10), text_color="gray")
        self.speed_hint.pack(side="left")
        self.speed_combo.bind("<<ComboboxSelected>>", lambda e: self._update_speed_hint())

        # ── Audio Sources ──
        ctk.CTkLabel(main, text="Audio Sources", font=("Segoe UI", 14, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 5))
        audio_section = ctk.CTkFrame(main, corner_radius=8)
        audio_section.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Primary: Microphone
        mic_frame = ctk.CTkFrame(audio_section, fg_color="transparent")
        mic_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(mic_frame, text="🎤 Microphone", font=("Segoe UI", 12), width=120, anchor="w").pack(side="left")
        self.audio_devices = list_audio_devices()
        self._mic_devices = [d for d in self.audio_devices if any(kw in d.lower() for kw in MIC_KEYWORDS)] or self.audio_devices
        default_mic = DEFAULT_MICROPHONE if DEFAULT_MICROPHONE in self._mic_devices else (self._mic_devices[0] if self._mic_devices else "")
        self.audio_var = tk.StringVar(value=default_mic)
        self.audio_combo = ctk.CTkComboBox(mic_frame, variable=self.audio_var, values=self.audio_devices, state="readonly", width=350)
        self.audio_combo.pack(side="left", padx=(5, 5))

        self.audio_hint = ctk.CTkLabel(mic_frame, text="", font=("Segoe UI", 10), text_color="gray")
        self.audio_hint.pack(side="left", padx=(5, 0))
        self._update_audio_hint()
        self.audio_combo.bind("<<ComboboxSelected>>", lambda e: self._update_audio_hint())

        # Secondary: System/Browser audio (loopback)
        sys_frame = ctk.CTkFrame(audio_section, fg_color="transparent")
        sys_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.dual_audio_var = tk.BooleanVar(value=False)
        self.dual_check = ctk.CTkCheckBox(sys_frame, text="🔊 + Browser/System", variable=self.dual_audio_var, command=self._on_dual_audio_toggled, width=120)
        self.dual_check.pack(side="left")

        self._loopback_devices = [d for d in self.audio_devices if any(kw in d.lower() for kw in LOOPBACK_KEYWORDS)]
        default_loopback = self._loopback_devices[0] if self._loopback_devices else (self.audio_devices[0] if self.audio_devices else "")
        self.loopback_var = tk.StringVar(value=default_loopback)
        self.loopback_combo = ctk.CTkComboBox(sys_frame, variable=self.loopback_var, values=self.audio_devices, state="disabled", width=350)
        self.loopback_combo.pack(side="left", padx=(5, 5))

        self.loopback_hint = ctk.CTkLabel(sys_frame, text="", font=("Segoe UI", 10), text_color="gray")
        self.loopback_hint.pack(side="left", padx=(5, 0))
        self.loopback_combo.bind("<<ComboboxSelected>>", lambda e: self._update_loopback_hint())

        # Mix volume slider
        mix_frame = ctk.CTkFrame(audio_section, fg_color="transparent")
        mix_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.mic_vol_label = ctk.CTkLabel(mix_frame, text="Mic vol:", font=("Segoe UI", 10), text_color="gray")
        self.mic_vol_label.pack(side="left")
        self.mic_vol_var = tk.DoubleVar(value=1.0)
        self.mic_vol_scale = ctk.CTkSlider(mix_frame, from_=0.1, to=2.0, variable=self.mic_vol_var, width=100, state="disabled")
        self.mic_vol_scale.pack(side="left", padx=(5, 15))

        self.sys_vol_label = ctk.CTkLabel(mix_frame, text="Sys vol:", font=("Segoe UI", 10), text_color="gray")
        self.sys_vol_label.pack(side="left")
        self.sys_vol_var = tk.DoubleVar(value=1.0)
        self.sys_vol_scale = ctk.CTkSlider(mix_frame, from_=0.1, to=2.0, variable=self.sys_vol_var, width=100, state="disabled")
        self.sys_vol_scale.pack(side="left", padx=(5, 0))

        # Refresh button
        refresh_frame = ctk.CTkFrame(audio_section, fg_color="transparent")
        refresh_frame.pack(fill="x", padx=10, pady=(5, 10))
        refresh_btn = ctk.CTkButton(refresh_frame, text="↻ Refresh Devices", width=140, command=self._refresh_audio_devices, fg_color="transparent", border_width=1, text_color=("gray10", "gray90"))
        refresh_btn.pack(side="left")

        # ── Audio Level Meters ──
        ctk.CTkLabel(main, text="Audio Levels", font=("Segoe UI", 14, "bold")).grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 5))
        meter_frame = ctk.CTkFrame(main, corner_radius=8)
        meter_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Mic level
        mic_meter_row = ctk.CTkFrame(meter_frame, fg_color="transparent")
        mic_meter_row.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(mic_meter_row, text="🎤 Mic", font=("Segoe UI", 12), width=80, anchor="w").pack(side="left")
        self.mic_meter = ctk.CTkProgressBar(mic_meter_row, height=12)
        self.mic_meter.pack(side="left", padx=(5, 5), fill="x", expand=True)
        self.mic_meter.set(0)
        self.mic_db_label = ctk.CTkLabel(mic_meter_row, text="— dB", font=("Consolas", 10), text_color="gray", width=60)
        self.mic_db_label.pack(side="left")

        # System level
        sys_meter_row = ctk.CTkFrame(meter_frame, fg_color="transparent")
        sys_meter_row.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(sys_meter_row, text="🔊 System", font=("Segoe UI", 12), width=80, anchor="w").pack(side="left")
        self.sys_meter = ctk.CTkProgressBar(sys_meter_row, height=12)
        self.sys_meter.pack(side="left", padx=(5, 5), fill="x", expand=True)
        self.sys_meter.set(0)
        self.sys_db_label = ctk.CTkLabel(sys_meter_row, text="— dB", font=("Consolas", 10), text_color="gray", width=60)
        self.sys_db_label.pack(side="left")

        self._level_streams: list = []
        self._mic_level = -60.0
        self._sys_level = -60.0
        self._meter_update_id = None

        # Options row: diarize + API status
        options_frame = ctk.CTkFrame(main, fg_color="transparent")
        options_frame.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.diarize_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Diarize speakers", variable=self.diarize_var).pack(side="left", padx=(0, 20))

        self.enhance_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Enhance with Claude", variable=self.enhance_var).pack(side="left")

        self.api_status_label = ctk.CTkLabel(options_frame, text="", font=("Segoe UI", 10), text_color="gray")
        self.api_status_label.pack(side="right")

        # PDF selector
        pdf_frame = ctk.CTkFrame(main, fg_color="transparent")
        pdf_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        ctk.CTkLabel(pdf_frame, text="Slides PDF", font=("Segoe UI", 12)).pack(side="left")
        self.pdf_var = tk.StringVar(value="(none)")
        self.pdf_combo = ctk.CTkComboBox(pdf_frame, variable=self.pdf_var, state="readonly", width=350)
        self.pdf_combo.pack(side="left", padx=(10, 10))
        self.pdf_combo.bind("<<ComboboxSelected>>", lambda e: self._on_pdf_selected())

        browse_btn = ctk.CTkButton(pdf_frame, text="Browse...", width=80, command=self._browse_pdf, fg_color="#34495e", hover_color="#2c3e50")
        browse_btn.pack(side="left", padx=(0, 10))

        self.pdf_page_label = ctk.CTkLabel(pdf_frame, text="", font=("Segoe UI", 10), text_color="gray")
        self.pdf_page_label.pack(side="left")

        # ── Control Buttons ──
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.grid(row=11, column=0, columnspan=2, pady=(10, 10))

        self.record_btn = ctk.CTkButton(btn_frame, text="⏺  Record", font=("Segoe UI", 16, "bold"),
                                    fg_color="#e74c3c", hover_color="#c0392b", text_color="white", width=160, height=45,
                                    command=self._toggle_recording, cursor="hand2")
        self.record_btn.pack(side="left", padx=10)

        self.transcribe_btn = ctk.CTkButton(btn_frame, text="📝  Transcribe File", font=("Segoe UI", 14),
                                        fg_color="#3498db", hover_color="#2980b9", text_color="white", width=180, height=45,
                                        command=self._transcribe_file, cursor="hand2")
        self.transcribe_btn.pack(side="left", padx=10)

        # ── Slide Marker Section ──
        ctk.CTkLabel(main, text="Slide Tracking", font=("Segoe UI", 14, "bold")).grid(row=12, column=0, columnspan=2, sticky="w", pady=(15, 5))
        slide_frame = ctk.CTkFrame(main, corner_radius=8)
        slide_frame.grid(row=13, column=0, columnspan=2, sticky="ew")

        slide_btn_row = ctk.CTkFrame(slide_frame, fg_color="transparent")
        slide_btn_row.pack(fill="x", padx=10, pady=10)

        self.slide_btn = ctk.CTkButton(slide_btn_row, text="▶  Next Slide", font=("Segoe UI", 16, "bold"),
                                   fg_color="#27ae60", hover_color="#219653", text_color="white", width=160, height=45,
                                   command=self._mark_next_slide, cursor="hand2",
                                   state="disabled")
        self.slide_btn.pack(side="left", padx=(0, 15))

        self.undo_slide_btn = ctk.CTkButton(slide_btn_row, text="↩ Undo", font=("Segoe UI", 12),
                                        fg_color="#95a5a6", hover_color="#7f8c8d", text_color="white", width=90, height=45,
                                        command=self._undo_last_slide, cursor="hand2",
                                        state="disabled")
        self.undo_slide_btn.pack(side="left", padx=(0, 20))

        info_frame = ctk.CTkFrame(slide_btn_row, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        self.slide_label = ctk.CTkLabel(info_frame, text="Slide: —", font=("Consolas", 18, "bold"), text_color="#ecf0f1")
        self.slide_label.pack(anchor="w")

        self.slide_count_label = ctk.CTkLabel(info_frame, text="Markers: 0", font=("Segoe UI", 10), text_color="gray")
        self.slide_count_label.pack(anchor="w")

        ctk.CTkLabel(slide_frame, text="Shortcuts:  → Right Arrow = next slide    ← Left Arrow = undo",
                  font=("Segoe UI", 10), text_color="gray").pack(anchor="w", padx=10, pady=(0, 10))

        # Timer display
        self.timer_label = ctk.CTkLabel(main, text="00:00", font=("Consolas", 36, "bold"), text_color="#ecf0f1")
        self.timer_label.grid(row=14, column=0, columnspan=2, pady=(15, 10))

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ctk.CTkLabel(main, textvariable=self.status_var, font=("Segoe UI", 10),
                               text_color="gray", anchor="w")
        status_bar.grid(row=15, column=0, columnspan=2, sticky="ew")

        # Progress bar
        self.progress = ctk.CTkProgressBar(main, mode="indeterminate", width=560)
        self.progress.grid(row=16, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.progress.stop()

        main.columnconfigure(0, weight=1)
    def _get_course_id(self) -> str | None:
        val = self.course_var.get()
        if not val:
            return None
        return val.split(" — ")[0]

    def _on_course_changed(self):
        self._update_lecture_number()
        self._update_pdf_list()
        self._try_auto_select_pdf()

    def _update_lecture_number(self):
        cid = self._get_course_id()
        if cid:
            self.num_var.set(str(find_next_lecture_number(cid)))

    def _update_pdf_list(self):
        cid = self._get_course_id()
        if not cid:
            self.pdf_combo.configure(values=["(none)"])
            self.pdf_var.set("(none)")
            return

        pdfs = list_course_pdfs(cid)
        names = ["(none)"] + [p.name for p in pdfs]
        self.pdf_combo.configure(values=names)
        self.pdf_var.set("(none)")
        self.selected_pdf_path = None
        self.total_slide_count = 0
        self.pdf_page_label.configure(text="")

    def _on_pdf_selected(self):
        val = self.pdf_var.get()
        if val == "(none)":
            self.selected_pdf_path = None
            self.total_slide_count = 0
            self.pdf_page_label.configure(text="")
            return

        cid = self._get_course_id()
        if cid:
            self.selected_pdf_path = get_slides_dir(cid) / val
            self.total_slide_count = count_pdf_pages(self.selected_pdf_path)
            self.pdf_page_label.configure(text=f"{self.total_slide_count} slides")

    def _try_auto_select_pdf(self):
        cid = self._get_course_id()
        if not cid:
            return
        num_str = self.num_var.get()
        if not num_str.isdigit():
            return
        lecture_num = int(num_str)
        pdfs = list_course_pdfs(cid)
        matched = match_pdf_to_lecture(cid, lecture_num, pdfs)
        if matched:
            self.pdf_var.set(matched.name)
            self._on_pdf_selected()

    def _browse_pdf(self):
        cid = self._get_course_id()
        initial_dir = str(get_slides_dir(cid)) if cid and get_slides_dir(cid).exists() else str(Path.home())
        path = filedialog.askopenfilename(
            title="Select slides PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialdir=initial_dir,
        )
        if path:
            self.selected_pdf_path = Path(path)
            self.total_slide_count = count_pdf_pages(self.selected_pdf_path)
            self.pdf_var.set(self.selected_pdf_path.name)
            self.pdf_page_label.configure(text=f"{self.total_slide_count} slides")

    def _on_dual_audio_toggled(self):
        enabled = self.dual_audio_var.get()
        state = "readonly" if enabled else "disabled"
        scale_state = "!disabled" if enabled else "disabled"
        self.loopback_combo.configure(state=state)
        self.mic_vol_scale.configure(state="normal" if enabled else "disabled")
        self.sys_vol_scale.configure(state="normal" if enabled else "disabled")
        if enabled:
            self._update_loopback_hint()
        else:
            self.loopback_hint.configure(text="")

    def _refresh_audio_devices(self):
        self.audio_devices = list_audio_devices()
        self._mic_devices = [d for d in self.audio_devices
                             if any(kw in d.lower() for kw in MIC_KEYWORDS)] or self.audio_devices
        self._loopback_devices = [d for d in self.audio_devices
                                  if any(kw in d.lower() for kw in LOOPBACK_KEYWORDS)]

        self.audio_combo.configure(values=self.audio_devices)
        self.loopback_combo.configure(values=self.audio_devices)

        if self.audio_var.get() not in self.audio_devices and self.audio_devices:
            self.audio_var.set(self._mic_devices[0] if self._mic_devices else self.audio_devices[0])
        if self.loopback_var.get() not in self.audio_devices and self._loopback_devices:
            self.loopback_var.set(self._loopback_devices[0])

        self._update_audio_hint()
        self._update_loopback_hint()
        self.status_var.set(f"Found {len(self.audio_devices)} audio device(s)")

    def _update_audio_hint(self):
        device = self.audio_var.get().lower()
        if any(kw in device for kw in LOOPBACK_KEYWORDS):
            self.audio_hint.configure(text="(system audio)", text_color="#27ae60")
        elif any(kw in device for kw in ["focusrite", "scarlett"]):
            self.audio_hint.configure(text="(Focusrite)", text_color="#2980b9")
        elif any(kw in device for kw in MIC_KEYWORDS):
            self.audio_hint.configure(text="(mic)", text_color="gray")
        else:
            self.audio_hint.configure(text="")

    def _update_loopback_hint(self):
        device = self.loopback_var.get().lower()
        if any(kw in device for kw in LOOPBACK_KEYWORDS):
            self.loopback_hint.configure(text="(system/browser audio)", text_color="#27ae60")
        elif any(kw in device for kw in MIC_KEYWORDS):
            self.loopback_hint.configure(text="⚠ this looks like a mic, not system audio", text_color="#e67e22")
        else:
            self.loopback_hint.configure(text="")

    def _update_speed_hint(self):
        speed = self._get_playback_speed()
        if abs(speed - 1.0) < 0.01:
            self.speed_hint.configure(text="")
        else:
            # Show time saving estimate for a typical 2-hour lecture
            real_mins = 120
            rec_mins = int(real_mins / speed)
            self.speed_hint.configure(
                text=f"2h lecture in {rec_mins}min — audio normalized before transcription",
                text_color="#27ae60",
            )

    def _get_playback_speed(self) -> float:
        """Parse the speed selector value (e.g. '1.5×') to a float."""
        raw = self.speed_var.get().replace("×", "").replace("x", "").strip()
        try:
            return float(raw)
        except ValueError:
            return 1.0

    # ── Audio Level Monitoring (via sounddevice) ────────────────────────

    def _start_level_monitors(self):
        """Start sounddevice input streams for real-time VU meters."""
        self._stop_level_monitors()
        import sounddevice as sd

        mic_device = self.audio_var.get()
        dual = self.dual_audio_var.get()
        loopback_device = self.loopback_var.get() if dual else None

        # Monitor mic input
        mic_idx = _get_sounddevice_index(mic_device)
        if mic_idx is not None:
            try:
                stream = sd.InputStream(
                    device=mic_idx, channels=1, samplerate=16000, blocksize=1600,
                    callback=lambda indata, frames, t, s: self._on_audio_level(indata, "mic"),
                )
                stream.start()
                self._level_streams.append(stream)
            except Exception as e:
                self.status_var.set(f"Mic monitor failed: {e}")

        # Monitor system/loopback input
        if dual and loopback_device:
            sys_idx = _get_sounddevice_index(loopback_device)
            if sys_idx is not None:
                try:
                    stream = sd.InputStream(
                        device=sys_idx, channels=1, samplerate=16000, blocksize=1600,
                        callback=lambda indata, frames, t, s: self._on_audio_level(indata, "sys"),
                    )
                    stream.start()
                    self._level_streams.append(stream)
                except Exception as e:
                    self.status_var.set(f"System audio monitor failed: {e}")

        self._update_meters()

    def _on_audio_level(self, indata, target: str):
        """Callback from sounddevice — compute RMS dB from audio block."""
        import numpy as np
        rms = np.sqrt(np.mean(indata ** 2))
        db = 20 * np.log10(max(rms, 1e-10))
        # Smooth: exponential moving average
        if target == "mic":
            self._mic_level = self._mic_level * 0.6 + db * 0.4
        else:
            self._sys_level = self._sys_level * 0.6 + db * 0.4

    def _stop_level_monitors(self):
        """Stop all sounddevice level monitoring streams."""
        for stream in self._level_streams:
            try:
                stream.stop()
                stream.close()
            except Exception:
                pass
        self._level_streams.clear()
        self._mic_level = -60.0
        self._sys_level = -60.0

        if self._meter_update_id:
            self.root.after_cancel(self._meter_update_id)
            self._meter_update_id = None

        self._set_meter(self.mic_meter, -60.0)
        self._set_meter(self.sys_meter, -60.0)
        self.mic_db_label.configure(text="— dB")
        self.sys_db_label.configure(text="— dB")

    def _update_meters(self):
        """Periodically redraw the VU meter canvases from the latest levels."""
        if not self.recording:
            return

        self._set_meter(self.mic_meter, self._mic_level)
        self.mic_db_label.configure(text=f"{self._mic_level:.0f} dB")

        if self.dual_audio_var.get():
            self._set_meter(self.sys_meter, self._sys_level)
            self.sys_db_label.configure(text=f"{self._sys_level:.0f} dB")

        self._meter_update_id = self.root.after(100, self._update_meters)

    def _set_meter(self, meter: ctk.CTkProgressBar, db: float):
        pct = max(0.0, min(1.0, (db + 60.0) / 60.0))
        meter.set(pct)
        if pct < 0.6:
            color = "#27ae60"
        elif pct < 0.8:
            color = "#f39c12"
        else:
            color = "#e74c3c"
        meter.configure(progress_color=color)

    def _set_state(self, state: str, message: str = ""):
        self.status_var.set(message)

        if state == "ready":
            self.record_btn.configure(text="⏺  Record", fg_color="#e74c3c", hover_color="#c0392b", state="normal")
            self.transcribe_btn.configure(state="normal")
            self.course_combo.configure(state="readonly")
            self.audio_combo.configure(state="readonly")
            self.slide_btn.configure(state="disabled")
            self.undo_slide_btn.configure(state="disabled")
            self.progress.stop()
        elif state == "recording":
            self.record_btn.configure(text="⏹  Stop", fg_color="#c0392b", hover_color="#e74c3c", state="normal")
            self.transcribe_btn.configure(state="disabled")
            self.course_combo.configure(state="disabled")
            self.audio_combo.configure(state="disabled")
            self.slide_btn.configure(state="normal")
            self.undo_slide_btn.configure(state="normal")
        elif state == "busy":
            self.record_btn.configure(state="disabled")
            self.transcribe_btn.configure(state="disabled")
            self.course_combo.configure(state="disabled")
            self.audio_combo.configure(state="disabled")
            self.slide_btn.configure(state="disabled")
            self.undo_slide_btn.configure(state="disabled")
            self.progress.start()

    def _update_timer(self):
        if self.recording and self.record_start_time:
            elapsed = time.time() - self.record_start_time
            m, s = divmod(int(elapsed), 60)
            h, m = divmod(m, 60)
            if h > 0:
                self.timer_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
            else:
                self.timer_label.configure(text=f"{m:02d}:{s:02d}")
            self.timer_id = self.root.after(500, self._update_timer)

    def _slide_display(self, num: int) -> str:
        if num <= 0:
            return "Slide: —"
        if self.total_slide_count > 0:
            return f"Slide: {num}/{self.total_slide_count}"
        return f"Slide: {num}"

    def _mark_next_slide(self):
        if not self.recording:
            return
        elapsed = time.time() - self.record_start_time
        self.current_slide += 1
        self.slide_markers.append((self.current_slide, elapsed))
        self.slide_label.configure(text=self._slide_display(self.current_slide))
        self.slide_count_label.configure(text=f"Markers: {len(self.slide_markers)}")
        self.status_var.set(f"Marked slide {self.current_slide} at {format_timestamp(elapsed)}")

        # Flash the button green briefly
        self.slide_btn.configure(fg_color="#2ecc71")
        self.root.after(200, lambda: self.slide_btn.configure(fg_color="#27ae60"))

    def _undo_last_slide(self):
        if not self.recording or not self.slide_markers:
            return
        removed = self.slide_markers.pop()
        self.current_slide = self.slide_markers[-1][0] if self.slide_markers else 0
        self.slide_label.configure(text=self._slide_display(self.current_slide))
        self.slide_count_label.configure(text=f"Markers: {len(self.slide_markers)}")
        self.status_var.set(f"Removed slide {removed[0]} marker")

    def _toggle_recording(self):
        if not self.recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        cid = self._get_course_id()
        if not cid:
            messagebox.showwarning("No course", "Select a course first.")
            return

        # Build organized folder: recordings/{course_id}/Lecture_{num}_{title}/
        lecture_num = self.num_var.get().strip() if self.num_var.get().strip() else "0"
        title = self.title_var.get().strip()
        safe_title = title.replace(" ", "_").replace("/", "-") if title else "untitled"
        folder_name = f"Lecture_{lecture_num}_{safe_title}"
        lecture_dir = RECORDINGS_DIR / cid / folder_name
        lecture_dir.mkdir(parents=True, exist_ok=True)
        self.audio_path = lecture_dir / "recording.mp3"

        audio_device = self.audio_var.get()
        if not audio_device:
            messagebox.showwarning("No audio device", "Select an audio source first.")
            return

        ffmpeg_bin = _find_ffmpeg()
        dual = self.dual_audio_var.get()
        loopback_device = self.loopback_var.get() if dual else None

        # Map sounddevice names to ffmpeg dshow names
        dshow_mic = _get_dshow_name(audio_device)
        dshow_sys = _get_dshow_name(loopback_device) if loopback_device else None

        if dual and dshow_sys:
            # Dual-source: mix mic + system audio into one stream
            mic_vol = self.mic_vol_var.get()
            sys_vol = self.sys_vol_var.get()
            filter_str = (
                f"[0:a]volume={mic_vol:.2f}[mic];"
                f"[1:a]volume={sys_vol:.2f}[sys];"
                f"[mic][sys]amix=inputs=2:duration=longest:dropout_transition=3[out]"
            )
            cmd = [
                ffmpeg_bin,
                "-f", "dshow", "-i", f"audio={dshow_mic}",
                "-f", "dshow", "-i", f"audio={dshow_sys}",
                "-filter_complex", filter_str,
                "-map", "[out]",
                "-ac", "1",  # mono output for smaller files & better transcription
                "-y", str(self.audio_path),
            ]
        else:
            # Single-source recording
            cmd = [
                ffmpeg_bin, "-f", "dshow",
                "-i", f"audio={dshow_mic}",
                "-ac", "1",
                "-y", str(self.audio_path),
            ]

        try:
            self.ffmpeg_proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except FileNotFoundError:
            messagebox.showerror("ffmpeg not found",
                                 "ffmpeg not found on PATH or in common locations.\n"
                                 "Install with: winget install Gyan.FFmpeg")
            return

        # Reset slide tracking
        start_slide = int(self.start_slide_var.get()) - 1 if self.start_slide_var.get().isdigit() else 0
        self.current_slide = start_slide
        self.slide_markers = []
        self.slide_label.configure(text=self._slide_display(self.current_slide))
        self.slide_count_label.configure(text="Markers: 0")

        self.recording = True
        self.record_start_time = time.time()
        self._set_state("recording", f"Recording... tap 'Next Slide' or press → when lecturer changes slides")
        self._update_timer()
        self._start_level_monitors()

    def _stop_recording(self):
        self.recording = False
        self._stop_level_monitors()
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.ffmpeg_proc:
            try:
                self.ffmpeg_proc.stdin.write(b"q")
                self.ffmpeg_proc.stdin.flush()
            except Exception:
                pass
            self.ffmpeg_proc.wait(timeout=10)
            self.ffmpeg_proc = None

        if not self.audio_path or not self.audio_path.exists() or self.audio_path.stat().st_size == 0:
            self._set_state("ready", "Recording failed — no audio captured.")
            messagebox.showerror("Error", "Recording failed or file is empty.")
            return

        marker_info = f"\n{len(self.slide_markers)} slide markers recorded." if self.slide_markers else ""
        self._set_state("ready", f"Recorded: {self.audio_path.name}")

        if messagebox.askyesno("Transcribe?", f"Recording saved.{marker_info}\nTranscribe now?"):
            self._run_transcription(self.audio_path, self.slide_markers.copy())

    def _transcribe_file(self):
        path = filedialog.askopenfilename(
            title="Select audio file",
            filetypes=[("Audio files", "*.mp3 *.wav *.m4a *.ogg *.flac *.webm"), ("All files", "*.*")],
            initialdir=str(RECORDINGS_DIR) if RECORDINGS_DIR.exists() else str(Path.home()),
        )
        if not path:
            return
        self.audio_path = Path(path)
        self._run_transcription(self.audio_path, slide_markers=None)

    def _run_transcription(self, audio_path: Path, slide_markers: list[tuple[int, float]] | None = None):
        cid = self._get_course_id()
        if not cid:
            messagebox.showwarning("No course", "Select a course first.")
            return

        model = self.model_var.get()
        use_api = model == "api"
        do_diarize = self.diarize_var.get()
        do_enhance = self.enhance_var.get()
        pdf_path = self.selected_pdf_path
        total_slides = self.total_slide_count
        playback_speed = self._get_playback_speed()

        label = "Whisper API" if use_api else f"Whisper ({model})"
        extra = ""
        if playback_speed > 1.01:
            extra += f" (normalizing {playback_speed}× → 1×)"
        if do_diarize:
            extra += " + diarization"
        if do_enhance:
            extra += " + Claude enhancement"
        self._set_state("busy", f"Transcribing with {label}{extra}... this may take a while")

        def worker():
            try:
                transcribe_path = audio_path

                # Normalize speed if recording was done at >1× playback
                if playback_speed > 1.01:
                    self.root.after(0, lambda: self.status_var.set(
                        f"Normalizing audio from {playback_speed}× to 1× speed..."))
                    transcribe_path = normalize_audio_speed(audio_path, playback_speed)

                # Scale slide markers to real lecture time
                scaled_markers = slide_markers
                if slide_markers and playback_speed > 1.01:
                    scaled_markers = scale_slide_markers(slide_markers, playback_speed)

                # Transcribe (using the normalized audio)
                if use_api:
                    result = transcribe_audio_api(transcribe_path, language=self.lang_var.get(), course_id=cid)
                else:
                    result = transcribe_audio(transcribe_path, model=model, language=self.lang_var.get(), course_id=cid)

                # Diarize if requested (use normalized audio)
                if do_diarize:
                    self.root.after(0, lambda: self.status_var.set("Running speaker diarization..."))
                    diar = diarize_audio(transcribe_path)
                    result["segments"] = merge_diarization_with_transcript(result["segments"], diar)

                lecture_num = int(self.num_var.get()) if self.num_var.get().isdigit() else find_next_lecture_number(cid)
                title = self.title_var.get().strip()

                # Save plain transcript (in same folder as recording)
                txt_path = audio_path.parent / "transcript.txt"
                txt_path.write_text(result["text"], encoding="utf-8")

                # Build and save raw Obsidian note (use scaled markers)
                md = build_markdown(cid, lecture_num, title, result, audio_path, scaled_markers)
                output_path = save_transcript(cid, lecture_num, title, md)

                # Save structured output (use scaled markers, store speed metadata)
                json_path = save_structured_output(
                    cid, lecture_num, title, result, audio_path,
                    scaled_markers, pdf_path, total_slides,
                )

                # Append speed metadata to JSON
                if playback_speed > 1.01 and json_path and json_path.exists():
                    data = json.loads(json_path.read_text(encoding="utf-8"))
                    data["playback_speed"] = playback_speed
                    data["normalized_audio"] = str(transcribe_path)
                    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

                prompt_path = save_prompt_template(cid, lecture_num, title, json_path, pdf_path)

                # Enhance with Claude if requested
                enhanced_path = None
                if do_enhance:
                    self.root.after(0, lambda: self.status_var.set("Enhancing notes with Claude..."))
                    enhanced_md = enhance_notes_with_claude(json_path, cid, lecture_num, title, pdf_path)
                    enhanced_path = save_enhanced_notes(cid, lecture_num, title, enhanced_md)

                self.root.after(0, lambda: self._transcription_done(
                    enhanced_path or output_path, txt_path, json_path, prompt_path))
            except Exception as e:
                err_msg = str(e)
                self.root.after(0, lambda: self._transcription_error(err_msg))

        threading.Thread(target=worker, daemon=True).start()

    def _transcription_done(self, note_path: Path, txt_path: Path,
                            json_path: Path | None = None, prompt_path: Path | None = None):
        self._set_state("ready", f"Saved: {note_path.name}")
        self._update_lecture_number()
        msg = f"Note saved:\n{note_path}\n\nPlain text:\n{txt_path}"
        if json_path:
            msg += f"\n\nStructured data:\n{json_path}"
        if prompt_path:
            msg += f"\n\nClaude prompt:\n{prompt_path}"
        msg += "\n\nOpen Obsidian to edit."
        messagebox.showinfo("Done!", msg)

    def _transcription_error(self, error: str):
        self._set_state("ready", "Transcription failed.")
        messagebox.showerror("Error", f"Transcription failed:\n{error}")

    def run(self):
        self.root.mainloop()


# ── CLI ─────────────────────────────────────────────────────────────

def cli():
    import argparse

    parser = argparse.ArgumentParser(
        description="Record and transcribe lectures for Obsidian",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python lecture_recorder.py --course 34655 --title "Noise"
  python lecture_recorder.py --transcribe-only recording.mp3 --course 34655 --title "Noise"
  python lecture_recorder.py --list-courses
        """,
    )

    parser.add_argument("--course", "-c", help="Course ID (e.g. 34655)")
    parser.add_argument("--title", "-t", help="Lecture title")
    parser.add_argument("--num", "-n", type=int, help="Lecture number (auto-detected if omitted)")
    parser.add_argument("--model", "-m", default="base", help="Whisper model (default: base)")
    parser.add_argument("--language", "-l", default="English", help="Language (default: English)")
    parser.add_argument("--transcribe-only", metavar="FILE", help="Transcribe an existing audio file")
    parser.add_argument("--record-only", action="store_true", help="Only record, don't transcribe")
    parser.add_argument("--list-courses", action="store_true", help="List available courses")
    parser.add_argument("--pdf", help="Path to slides PDF for page counting")
    parser.add_argument("--whisper-api", action="store_true", help="Use OpenAI Whisper API instead of local model")
    parser.add_argument("--audio-device", help=f"Audio input device name (default: {DEFAULT_MICROPHONE})")
    parser.add_argument("--list-devices", action="store_true", help="List available audio input devices")
    parser.add_argument("--diarize", action="store_true", help="Run speaker diarization (requires pyannote.audio + HF_TOKEN)")
    parser.add_argument("--enhance", action="store_true", help="Enhance notes with Claude API (requires ANTHROPIC_API_KEY)")

    args = parser.parse_args()

    if args.list_devices:
        devices = list_audio_devices()
        print("\nAvailable audio devices:")
        for d in devices:
            marker = "  ← default" if d == DEFAULT_MICROPHONE else ""
            print(f"  {d}{marker}")
        if not devices:
            print("  (none found — is ffmpeg installed?)")
        return

    if args.list_courses:
        print("\nAvailable courses:")
        for cid, info in sorted(COURSES.items()):
            print(f"  {cid}  {info['name']}")
        return

    if not args.course:
        parser.error("--course is required")
    if args.course not in COURSES:
        parser.error(f"Unknown course: {args.course}")

    course = COURSES[args.course]
    lecture_num = args.num or find_next_lecture_number(args.course)
    title = args.title or ""

    print(f"\n{'='*60}")
    print(f"  Lecture Recorder — {args.course} {course['name']}")
    print(f"  {course['prefix']} {lecture_num}{' - ' + title if title else ''}")
    print(f"{'='*60}")

    if args.transcribe_only:
        audio_path = Path(args.transcribe_only)
        if not audio_path.exists():
            print(f"Error: File not found: {audio_path}")
            sys.exit(1)
    else:
        RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = title.replace(" ", "_").replace("/", "-") if title else "untitled"
        audio_path = RECORDINGS_DIR / f"{args.course}_{safe_title}_{timestamp}.mp3"

        mic = args.audio_device or DEFAULT_MICROPHONE
        print(f"\nRecording from: {mic}")
        print("Press Q to stop recording...\n")
        proc = subprocess.run([
            "ffmpeg", "-f", "dshow", "-i", f"audio={mic}", "-y", str(audio_path),
        ])
        if not audio_path.exists() or audio_path.stat().st_size == 0:
            print("Error: Recording failed.")
            sys.exit(1)
        print(f"\nRecording saved: {audio_path}")

        if args.record_only:
            return

    # PDF handling
    pdf_path = None
    total_slides = 0
    if args.pdf:
        pdf_path = Path(args.pdf)
        if pdf_path.exists():
            total_slides = count_pdf_pages(pdf_path)
            print(f"  Slides PDF: {pdf_path.name} ({total_slides} pages)")
        else:
            print(f"  Warning: PDF not found: {pdf_path}")
            pdf_path = None

    # Transcribe
    model = "api" if args.whisper_api else args.model
    if model == "api":
        print(f"\nTranscribing with OpenAI Whisper API...")
        result = transcribe_audio_api(audio_path, language=args.language, course_id=args.course)
    else:
        print(f"\nTranscribing with Whisper ({model})...")
        result = transcribe_audio(audio_path, model=model, language=args.language, course_id=args.course)

    # Diarize if requested
    if args.diarize:
        print("Running speaker diarization...")
        diar = diarize_audio(audio_path)
        result["segments"] = merge_diarization_with_transcript(result["segments"], diar)

    txt_path = audio_path.with_suffix(".txt")
    txt_path.write_text(result["text"], encoding="utf-8")
    print(f"Plain transcript: {txt_path}")

    md = build_markdown(args.course, lecture_num, title, result, audio_path)
    output_path = save_transcript(args.course, lecture_num, title, md)

    # Structured output
    json_path = save_structured_output(
        args.course, lecture_num, title, result, audio_path,
        slide_markers=None, pdf_path=pdf_path, total_slides=total_slides,
    )
    prompt_path = save_prompt_template(args.course, lecture_num, title, json_path, pdf_path)

    # Enhance with Claude if requested
    if args.enhance:
        print("Enhancing notes with Claude...")
        enhanced_md = enhance_notes_with_claude(json_path, args.course, lecture_num, title, pdf_path)
        enhanced_path = save_enhanced_notes(args.course, lecture_num, title, enhanced_md)
        print(f"  Enhanced note: {enhanced_path}")

    print(f"\nDone!")
    print(f"  Note saved: {output_path}")
    print(f"  Audio: {audio_path}")
    print(f"  Structured data: {json_path}")
    print(f"  Claude prompt: {prompt_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        app = LectureRecorderApp()
        app.run()
