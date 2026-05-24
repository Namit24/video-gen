# agents.md — Text-to-Animation Agent State File

## Project Goal
IISc CIL internship assignment.
Pipeline: text prompt → Gemini 2.5 Flash generates Manim code → Manim renders → 9:16 MP4 output.

## Tech Stack
- Python 3.10+
- Multi-backend LLMs (Gemini 2.5 Flash, Claude 3.5 Sonnet, GPT-4o) — generates Manim scene code
- Manim Community Edition — renders the animation
- Orchestrator: agent.py (runs LLM call via --backend → writes scene.py → subprocess manim → copies output)
- Backend API: FastAPI (api.py)
- Frontend UI: Streamlit (app.py)
- Output format: 1080x1920 MP4 (9:16 vertical)

## File Structure
- agent.py          → slim CLI orchestrator (CLI entry point)
- llm.py            → LLM backend routing logic for all backends
- manim_runner.py   → Manim subprocess runner + error retry logic
- utils.py          → strip_fences, sanitize_scene, concept_to_slug, find_rendered_mp4
- prompts.py        → SYSTEM_PROMPT constant only
- api.py            → FastAPI backend
- app.py            → Streamlit frontend
- scene.py          → auto-generated Manim scene (ignored)
- outputs/          → final rendered videos
- requirements.txt  → pip dependencies
- README.md         → submission doc

## Pipeline Steps
1. User runs: python agent.py "concept name" [--backend gemini|claude|openai]
2. agent.py sends prompt to selected LLM backend asking for a Manim scene class
3. LLM returns Python code; agent.py strips markdown fences, sanitizes syntax errors, and saves to scene.py
4. agent.py runs: manim scene.py GeneratedScene --format mp4 --width 1080 --height 1920 -q h
5. If manim exits with error, stderr is sent back to LLM for one retry
6. On success, video is copied to outputs/<concept>.mp4

## Run Instructions
* **Terminal 1 (FastAPI backend)**:
  ```bash
  uvicorn api:app --reload --port 8000
  ```
* **Terminal 2 (Streamlit frontend)**:
  ```bash
  streamlit run app.py
  ```
* **CLI (Command line interface)**:
  ```bash
  python agent.py "concept" --backend gemini|claude|openai
  ```

## Current Status
REFACTOR COMPLETE — Code base split into logical modular components with a CLI entrypoint, FastAPI endpoint, and Streamlit frontend.

## Completed Steps
- [x] Step 0: agents.md initialized
- [x] Step 1: requirements.txt created; manim 0.19.0 and google-generativeai verified OK
- [x] Step 2: agent.py created — Gemini call, fence stripping, manim render, retry, output copy
- [x] Step 3: test run "Fourier Series" — SUCCESS (1.5MB, simple style)
- [x] Step 3B: reel-style rewrite — SUCCESS, outputs/fourier_series.mp4 (2.7MB, 9-scene arc, no retry)
- [x] SYSTEM PROMPT UPDATED WITH REFERENCE SCENE
- [x] Step 4: test run "K Means Clustering" — SUCCESS, outputs/k_means_clustering.mp4 (2.7MB, template layout, no retry)
- [x] Step 4B: Multi-backend support added (--backend gemini|claude|openai) and requirements updated
- [x] Step 4C: Project codebase refactored into prompts.py, utils.py, llm.py, manim_runner.py, api.py, and app.py
- [x] Step 5: README.md and .gitignore created for submission

## Pending Steps
None.

## Known Issues
- Gemini/LLMs invent bad Manim color names → fixed by color whitelist in system prompt + sanitize_code() regex patcher.
- Gemini/LLMs use removed API methods (get_graph, get_function, coords_to_point) → fixed by _API_FIXES in sanitize_code().
- Gemini/LLMs place config.frame_* before from manim import * → fixed by import-order rewriter in sanitize_code().
- Gemini/LLMs produce unterminated strings or syntax errors on retry → fixed by sanitize_scene() syntax compiler/truncater.
- All sanitizer passes run on both initial and retry output before manim sees the file.

## Last Updated By
Submission completion
