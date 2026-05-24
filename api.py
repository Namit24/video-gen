from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import threading, uuid
from dotenv import load_dotenv
from llm import generate_code
from utils import strip_fences, sanitize_scene
from manim_runner import render

# Load environment variables
load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

jobs = {}

class GenerateRequest(BaseModel):
    concept: str
    backend: str = "gemini"

def run_job(job_id, concept, backend):
    try:
        jobs[job_id].update({"status": "running", "step": "Calling LLM...", "progress": 20})
        raw = generate_code(concept, backend)

        jobs[job_id].update({"step": "Writing scene.py...", "progress": 35})
        code = sanitize_scene(strip_fences(raw))

        jobs[job_id].update({"step": "Rendering with Manim...", "progress": 60})
        out_path = render(concept, code, backend, generate_code)

        jobs[job_id].update({"status": "done", "step": "Done", "progress": 100, "video_path": out_path})
    except Exception as e:
        jobs[job_id].update({"status": "failed", "error": str(e)})

@app.post("/generate")
def generate(req: GenerateRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "step": "Queued", "progress": 0, "video_path": None, "error": None}
    threading.Thread(target=run_job, args=(job_id, req.concept, req.backend)).start()
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def status(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})

@app.get("/video/{job_id}")
def video(job_id: str):
    job = jobs.get(job_id)
    if not job or job["status"] != "done":
        return {"error": "Not ready"}
    return FileResponse(job["video_path"], media_type="video/mp4", filename="animation.mp4")
