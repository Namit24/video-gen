# Handles manim subprocess execution and one retry
import subprocess, shutil, os
from utils import find_rendered_mp4, concept_to_slug

MANIM_CMD = ["manim", "scene.py", "GeneratedScene", "--format", "mp4", "-r", "1080,1920", "-ql"]

def render(concept: str, code: str, backend: str, generate_fn) -> str:
    """
    Writes code to scene.py, runs manim, retries once on error.
    Returns path to output mp4 on success, raises RuntimeError on failure.
    """
    with open("scene.py", "w") as f:
        f.write(code)

    result = subprocess.run(MANIM_CMD, capture_output=True, text=True)

    if result.returncode != 0:
        # Retry logic: pass the error context as the prompt
        retry_prompt = f"Fix this Manim error:\n---CODE---\n{code}\n---ERROR---\n{result.stderr}"
        retry_code = generate_fn(retry_prompt, backend)
        from utils import strip_fences, sanitize_scene
        retry_code = sanitize_scene(strip_fences(retry_code))
        with open("scene.py", "w") as f:
            f.write(retry_code)
        result = subprocess.run(MANIM_CMD, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr[-800:])

    mp4 = find_rendered_mp4()
    if not mp4:
        raise RuntimeError("Output video file could not be found.")
    slug = concept_to_slug(concept)
    os.makedirs("outputs", exist_ok=True)
    out_path = f"outputs/{slug}.mp4"
    shutil.copy(mp4, out_path)
    return out_path
