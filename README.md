# Text-to-Animation Agent
### IISc Computational Intelligence Lab — Internship Assignment

## Overview
An AI agent that takes any STEM concept as text input and automatically generates a 9:16 vertical animated explainer video — reel-style, like an educational Instagram/YouTube Short.

## Demo Videos
Sample outputs in `outputs/` directory:
- `fourier_series.mp4`
- `gradient_descent.mp4`
- `k_means_clustering.mp4`

## Methodology

### Pipeline
User Input (concept)
│
▼
LLM Backend (Gemini 2.5 Flash / Claude Sonnet / GPT-4o)
│  generates complete Manim Python scene
▼
Sanitizer (strip fences, fix common errors)
│
▼
Manim Renderer (subprocess, 1080x1920, MP4)
│  error? → auto-retry with stderr fed back to LLM
▼
Output Video
│
▼
FastAPI → Streamlit UI (progress bar + preview + download)

### Animation Structure
Every concept follows a fixed 9-scene reel arc:

| Scene | Purpose | Duration |
|-------|---------|----------|
| 1. Hook | Bold question to grab attention | 2-3s |
| 2. Intuition | Start from something familiar | 3-4s |
| 3. Core Visual | Animated step-by-step build | 5-6s |
| 4. Key Insight | The "aha moment" in one sentence | 3-4s |
| 5. Formula | Animated equation with vertical annotation table | 3-4s |
| 6. Deeper Mechanism | Edge cases, limiting behavior | 4-5s |
| 7. Applications | 3 real-world use cards, sliding in one at a time | 3-4s |
| 8. Surprising Fact | Striking number or historical fact | 2-3s |
| 9. Outro | Concept name + "Now you know." | 2s |

### Key Design Decisions
- **Reference-guided generation**: system prompt embeds a verified working Manim scene as a gold-standard example, dramatically improving first-pass correctness
- **Reel-style structure**: fixed 9-scene arc ensures consistent, informative output for any STEM concept
- **Auto-retry**: manim stderr is automatically fed back to the LLM for one correction attempt
- **Multi-backend**: swap Gemini, Claude, or OpenAI with `--backend` flag, no code changes
- **Modular codebase**: clean separation of LLM, rendering, API, and UI concerns

## Project Structure
├── agent.py          # CLI entry point
├── llm.py            # LLM backends (Gemini / Claude / OpenAI)
├── manim_runner.py   # Manim subprocess + auto-retry logic
├── utils.py          # strip_fences, sanitize_scene, concept_to_slug, find_rendered_mp4
├── prompts.py        # SYSTEM_PROMPT
├── api.py            # FastAPI backend
├── app.py            # Streamlit frontend
├── requirements.txt
└── outputs/          # Generated MP4 videos

## Setup

### Prerequisites
- Python 3.10+
- Manim Community Edition (`pip install manim`)
- At least one LLM API key

### Install
```bash
git clone <repo-url>
cd iisc
pip install -r requirements.txt
```

### Environment Variables
```bash
export GEMINI_API_KEY=your_key        # primary
export ANTHROPIC_API_KEY=your_key     # optional
export OPENAI_API_KEY=your_key        # optional
```

## Usage

### CLI
```bash
python agent.py "Fourier Series"
python agent.py "Gradient Descent" --backend claude
python agent.py "K Means Clustering" --backend openai
```

### Web UI
```bash
# Terminal 1 — start API
uvicorn api:app --port 8000

# Terminal 2 — start UI
streamlit run app.py
```
Then open http://localhost:8501

### Sample Prompts (tested)
- Fourier Series
- Gradient Descent
- K Means Clustering
- Linear Regression
- Newton's Laws of Motion
- DNA Replication
- Binary Search
- Ohm's Law

## Tech Stack
| Component | Technology |
|---|---|
| Animation | Manim Community v0.19 |
| LLM (primary) | Gemini 2.5 Flash |
| LLM (alternatives) | Claude Sonnet 4.6, GPT-4o |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Output | MP4, 1080x1920 (9:16 vertical) |

## Future Prospects
- **Voiceover sync** — per-scene narration via ElevenLabs TTS merged with ffmpeg
- **Local LLM** — Ollama + Qwen2.5-Coder for zero-cost offline generation
- **Vision feedback loop** — vision model reviews rendered frames and auto-corrects layout issues
- **Bilingual support** — Hindi/English narration for Indian education context
