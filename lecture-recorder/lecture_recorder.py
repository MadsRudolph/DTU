"""
Lecture Recorder & Transcriber for Obsidian
Records audio via ffmpeg, transcribes with Whisper, and saves as Obsidian-formatted markdown.
Supports slide markers during recording for slide-synced transcripts.
"""

import subprocess
import sys
import os
import json
import threading
import time
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from pathlib import Path

OBSIDIAN_COURSES = Path(r"C:\Users\Mads2\DTU\Obsidian\Courses")
RECORDINGS_DIR = Path(r"C:\Users\Mads2\DTU\lecture-recorder\recordings")
MICROPHONE = "Microphone Array (Realtek(R) Audio)"

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

    output_path = audio_path.with_suffix(".json")
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_path


def save_prompt_template(course_id: str, lecture_num: int, title: str,
                         json_path: Path, pdf_path: Path | None = None) -> Path:
    course = COURSES[course_id]
    prefix = course["prefix"]
    full_title = f"{prefix} {lecture_num} - {title}" if title else f"{prefix} {lecture_num}"

    pdf_line = f"\n- The lecture slides are: [[{pdf_path.name}]]" if pdf_path else ""

    prompt = f"""# Lecture Note Generation

Use the structured recording data in `{json_path.name}` to generate comprehensive
lecture notes for **{course_id} {course['name']}**, {full_title}.

## Source Data
- Structured transcript with timestamps: `{json_path.name}`{pdf_line}
- The `slide_sections` array groups the transcript by slide — use these as the primary structure

## Instructions
- Organize notes by slide, using the slide_sections from the JSON
- Include timestamps as references (e.g., [00:45])
- Fix obvious transcription errors and expand abbreviations
- Add clear section headings based on slide transitions and content
- Format equations in LaTeX ($...$)
- Use Obsidian-compatible markdown with [[wiki-links]]
- If speaker labels are present, note when students ask questions
- Summarize key takeaways at the end
- Keep the tone academic but accessible

## Output Format
Obsidian markdown note with YAML frontmatter, ready to save as `{full_title}.md`
"""

    output_path = json_path.with_suffix(".prompt.md")
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
    if data["slides"]["pdf_filename"]:
        slide_info = f"- Slides PDF: {data['slides']['pdf_filename']} ({data['slides']['total_pages']} pages/slides)\n"
        slide_info += f"- Slide markers recorded: {len(data['slides']['markers'])}\n"

    prompt = f"""You are creating lecture notes from a transcription. Generate comprehensive, well-structured
Obsidian-compatible markdown notes.

## Context
- Course: {course_id} {course['name']}
- {prefix}: {lecture_num} — {title}
- Date: {date}
{slide_info}
## Transcript Data (JSON)
{transcript_json}

## Requirements
1. Start with this exact YAML frontmatter:
---
course: "{course_id}"
course-name: "{course['name']}"
type: lecture-note
{prefix.lower()}: {lecture_num}
tags: [{short}, lecture, notes]
date: {date}
---

2. Use `# {full_title}` as the main heading
3. Organize by slide/topic with clear `##` and `###` headings
4. Fix transcription errors and expand abbreviations
5. Format equations in LaTeX ($...$) and use proper mathematical notation
6. Include key timestamps as references like [00:45]
7. If speaker labels are present, note student questions in blockquotes
8. Add a `## Key Takeaways` section at the end
9. Use Obsidian [[wiki-links]] where relevant
10. Keep the tone academic but clear and accessible
11. Include navigation at the bottom linking to [[{course_id} {course['name']}|{course_id} Home]]

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
        self.root = tk.Tk()
        self.root.title("Lecture Recorder")
        self.root.geometry("620x750")
        self.root.resizable(False, False)

        self.recording = False
        self.ffmpeg_proc = None
        self.audio_path = None
        self.record_start_time = None
        self.timer_id = None

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
        header = tk.Frame(self.root, bg="#1a1a2e", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Lecture Recorder", font=("Segoe UI", 16, "bold"),
                 bg="#1a1a2e", fg="white").pack(pady=10)

        # ── Main frame ──
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        # Course selector
        ttk.Label(main, text="Course", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.course_var = tk.StringVar()
        course_values = [f"{cid} — {info['name']}" for cid, info in sorted(COURSES.items())]
        self.course_combo = ttk.Combobox(main, textvariable=self.course_var, values=course_values,
                                         state="readonly", width=45)
        self.course_combo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.course_combo.bind("<<ComboboxSelected>>", lambda e: self._on_course_changed())

        # Lecture number + title
        num_title_frame = ttk.Frame(main)
        num_title_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ttk.Label(num_title_frame, text="#", font=("Segoe UI", 10)).pack(side="left")
        self.num_var = tk.StringVar()
        self.num_entry = ttk.Entry(num_title_frame, textvariable=self.num_var, width=5)
        self.num_entry.pack(side="left", padx=(5, 15))

        ttk.Label(num_title_frame, text="Title", font=("Segoe UI", 10)).pack(side="left")
        self.title_var = tk.StringVar()
        ttk.Entry(num_title_frame, textvariable=self.title_var, width=35).pack(side="left", padx=(5, 0), fill="x", expand=True)

        # Whisper model + language + start slide
        model_lang_frame = ttk.Frame(main)
        model_lang_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        ttk.Label(model_lang_frame, text="Model", font=("Segoe UI", 10)).pack(side="left")
        self.model_var = tk.StringVar(value="base")
        ttk.Combobox(model_lang_frame, textvariable=self.model_var, values=WHISPER_MODELS,
                     state="readonly", width=8).pack(side="left", padx=(5, 15))

        ttk.Label(model_lang_frame, text="Language", font=("Segoe UI", 10)).pack(side="left")
        self.lang_var = tk.StringVar(value="English")
        ttk.Entry(model_lang_frame, textvariable=self.lang_var, width=10).pack(side="left", padx=(5, 15))

        ttk.Label(model_lang_frame, text="Start slide", font=("Segoe UI", 10)).pack(side="left")
        self.start_slide_var = tk.StringVar(value="1")
        ttk.Entry(model_lang_frame, textvariable=self.start_slide_var, width=4).pack(side="left", padx=(5, 0))

        # Options row: diarize + API status
        options_frame = ttk.Frame(main)
        options_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        self.diarize_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Diarize speakers", variable=self.diarize_var).pack(side="left", padx=(0, 10))

        self.enhance_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Enhance with Claude", variable=self.enhance_var).pack(side="left")

        self.api_status_label = tk.Label(options_frame, text="", font=("Segoe UI", 8), fg="gray")
        self.api_status_label.pack(side="right")

        # PDF selector
        pdf_frame = ttk.Frame(main)
        pdf_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ttk.Label(pdf_frame, text="Slides PDF", font=("Segoe UI", 10)).pack(side="left")
        self.pdf_var = tk.StringVar(value="(none)")
        self.pdf_combo = ttk.Combobox(pdf_frame, textvariable=self.pdf_var, state="readonly", width=35)
        self.pdf_combo.pack(side="left", padx=(5, 5))
        self.pdf_combo.bind("<<ComboboxSelected>>", lambda e: self._on_pdf_selected())

        browse_btn = ttk.Button(pdf_frame, text="Browse...", width=8, command=self._browse_pdf)
        browse_btn.pack(side="left", padx=(0, 5))

        self.pdf_page_label = tk.Label(pdf_frame, text="", font=("Segoe UI", 9), fg="gray")
        self.pdf_page_label.pack(side="left")

        # ── Control Buttons ──
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(5, 5))

        self.record_btn = tk.Button(btn_frame, text="⏺  Record", font=("Segoe UI", 12, "bold"),
                                    bg="#e74c3c", fg="white", width=14, height=2,
                                    command=self._toggle_recording, relief="flat", cursor="hand2")
        self.record_btn.pack(side="left", padx=5)

        self.transcribe_btn = tk.Button(btn_frame, text="📝  Transcribe File", font=("Segoe UI", 11),
                                        bg="#3498db", fg="white", width=16, height=2,
                                        command=self._transcribe_file, relief="flat", cursor="hand2")
        self.transcribe_btn.pack(side="left", padx=5)

        # ── Slide Marker Section ──
        slide_frame = ttk.LabelFrame(main, text="Slide Tracking", padding=10)
        slide_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(5, 5))

        # Next slide button + undo
        slide_btn_row = ttk.Frame(slide_frame)
        slide_btn_row.pack(fill="x")

        self.slide_btn = tk.Button(slide_btn_row, text="▶  Next Slide", font=("Segoe UI", 13, "bold"),
                                   bg="#27ae60", fg="white", width=16, height=2,
                                   command=self._mark_next_slide, relief="flat", cursor="hand2",
                                   state="disabled")
        self.slide_btn.pack(side="left", padx=(0, 10))

        self.undo_slide_btn = tk.Button(slide_btn_row, text="↩ Undo", font=("Segoe UI", 10),
                                        bg="#95a5a6", fg="white", width=8, height=2,
                                        command=self._undo_last_slide, relief="flat", cursor="hand2",
                                        state="disabled")
        self.undo_slide_btn.pack(side="left", padx=(0, 10))

        # Slide info
        info_frame = ttk.Frame(slide_btn_row)
        info_frame.pack(side="left", fill="both", expand=True)

        self.slide_label = tk.Label(info_frame, text="Slide: —", font=("Consolas", 16, "bold"), fg="#2c3e50")
        self.slide_label.pack(anchor="w")

        self.slide_count_label = tk.Label(info_frame, text="Markers: 0", font=("Segoe UI", 9), fg="gray")
        self.slide_count_label.pack(anchor="w")

        # Shortcuts hint
        ttk.Label(slide_frame, text="Shortcuts:  → Right Arrow = next slide    ← Left Arrow = undo",
                  font=("Segoe UI", 8), foreground="gray").pack(anchor="w", pady=(5, 0))

        # Timer display
        self.timer_label = tk.Label(main, text="00:00", font=("Consolas", 28), fg="#333")
        self.timer_label.grid(row=8, column=0, columnspan=2, pady=(10, 5))

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main, textvariable=self.status_var, font=("Segoe UI", 9),
                               foreground="gray", anchor="w")
        status_bar.grid(row=9, column=0, columnspan=2, sticky="ew")

        # Progress bar
        self.progress = ttk.Progressbar(main, mode="indeterminate", length=560)
        self.progress.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(5, 0))

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
            self.pdf_combo["values"] = ["(none)"]
            self.pdf_var.set("(none)")
            return

        pdfs = list_course_pdfs(cid)
        names = ["(none)"] + [p.name for p in pdfs]
        self.pdf_combo["values"] = names
        self.pdf_var.set("(none)")
        self.selected_pdf_path = None
        self.total_slide_count = 0
        self.pdf_page_label.config(text="")

    def _on_pdf_selected(self):
        val = self.pdf_var.get()
        if val == "(none)":
            self.selected_pdf_path = None
            self.total_slide_count = 0
            self.pdf_page_label.config(text="")
            return

        cid = self._get_course_id()
        if cid:
            self.selected_pdf_path = get_slides_dir(cid) / val
            self.total_slide_count = count_pdf_pages(self.selected_pdf_path)
            self.pdf_page_label.config(text=f"{self.total_slide_count} slides")

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
            self.pdf_page_label.config(text=f"{self.total_slide_count} slides")

    def _set_state(self, state: str, message: str = ""):
        self.status_var.set(message)

        if state == "ready":
            self.record_btn.config(text="⏺  Record", bg="#e74c3c", state="normal")
            self.transcribe_btn.config(state="normal")
            self.course_combo.config(state="readonly")
            self.slide_btn.config(state="disabled")
            self.undo_slide_btn.config(state="disabled")
            self.progress.stop()
        elif state == "recording":
            self.record_btn.config(text="⏹  Stop", bg="#c0392b", state="normal")
            self.transcribe_btn.config(state="disabled")
            self.course_combo.config(state="disabled")
            self.slide_btn.config(state="normal")
            self.undo_slide_btn.config(state="normal")
        elif state == "busy":
            self.record_btn.config(state="disabled")
            self.transcribe_btn.config(state="disabled")
            self.course_combo.config(state="disabled")
            self.slide_btn.config(state="disabled")
            self.undo_slide_btn.config(state="disabled")
            self.progress.start(15)

    def _update_timer(self):
        if self.recording and self.record_start_time:
            elapsed = time.time() - self.record_start_time
            m, s = divmod(int(elapsed), 60)
            h, m = divmod(m, 60)
            if h > 0:
                self.timer_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            else:
                self.timer_label.config(text=f"{m:02d}:{s:02d}")
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
        self.slide_label.config(text=self._slide_display(self.current_slide))
        self.slide_count_label.config(text=f"Markers: {len(self.slide_markers)}")
        self.status_var.set(f"Marked slide {self.current_slide} at {format_timestamp(elapsed)}")

        # Flash the button green briefly
        self.slide_btn.config(bg="#2ecc71")
        self.root.after(200, lambda: self.slide_btn.config(bg="#27ae60"))

    def _undo_last_slide(self):
        if not self.recording or not self.slide_markers:
            return
        removed = self.slide_markers.pop()
        self.current_slide = self.slide_markers[-1][0] if self.slide_markers else 0
        self.slide_label.config(text=self._slide_display(self.current_slide))
        self.slide_count_label.config(text=f"Markers: {len(self.slide_markers)}")
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

        RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        title = self.title_var.get().strip()
        safe_title = title.replace(" ", "_").replace("/", "-") if title else "untitled"
        self.audio_path = RECORDINGS_DIR / f"{cid}_{safe_title}_{timestamp}.mp3"

        cmd = [
            "ffmpeg", "-f", "dshow",
            "-i", f"audio={MICROPHONE}",
            "-y",
            str(self.audio_path),
        ]

        try:
            self.ffmpeg_proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except FileNotFoundError:
            messagebox.showerror("ffmpeg not found", "Install ffmpeg and make sure it's on PATH.")
            return

        # Reset slide tracking
        start_slide = int(self.start_slide_var.get()) - 1 if self.start_slide_var.get().isdigit() else 0
        self.current_slide = start_slide
        self.slide_markers = []
        self.slide_label.config(text=self._slide_display(self.current_slide))
        self.slide_count_label.config(text="Markers: 0")

        self.recording = True
        self.record_start_time = time.time()
        self._set_state("recording", f"Recording... tap 'Next Slide' or press → when lecturer changes slides")
        self._update_timer()

    def _stop_recording(self):
        self.recording = False
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

        label = "Whisper API" if use_api else f"Whisper ({model})"
        extra = ""
        if do_diarize:
            extra += " + diarization"
        if do_enhance:
            extra += " + Claude enhancement"
        self._set_state("busy", f"Transcribing with {label}{extra}... this may take a while")

        def worker():
            try:
                # Transcribe
                if use_api:
                    result = transcribe_audio_api(audio_path, language=self.lang_var.get(), course_id=cid)
                else:
                    result = transcribe_audio(audio_path, model=model, language=self.lang_var.get(), course_id=cid)

                # Diarize if requested
                if do_diarize:
                    self.root.after(0, lambda: self.status_var.set("Running speaker diarization..."))
                    diar = diarize_audio(audio_path)
                    result["segments"] = merge_diarization_with_transcript(result["segments"], diar)

                lecture_num = int(self.num_var.get()) if self.num_var.get().isdigit() else find_next_lecture_number(cid)
                title = self.title_var.get().strip()

                # Save plain transcript
                txt_path = audio_path.with_suffix(".txt")
                txt_path.write_text(result["text"], encoding="utf-8")

                # Build and save raw Obsidian note
                md = build_markdown(cid, lecture_num, title, result, audio_path, slide_markers)
                output_path = save_transcript(cid, lecture_num, title, md)

                # Save structured output
                json_path = save_structured_output(
                    cid, lecture_num, title, result, audio_path,
                    slide_markers, pdf_path, total_slides,
                )
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
    parser.add_argument("--diarize", action="store_true", help="Run speaker diarization (requires pyannote.audio + HF_TOKEN)")
    parser.add_argument("--enhance", action="store_true", help="Enhance notes with Claude API (requires ANTHROPIC_API_KEY)")

    args = parser.parse_args()

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

        mic = MICROPHONE
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
