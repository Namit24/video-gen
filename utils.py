import os
import re

# ---------------------------------------------------------------------------
# Known bad Manim color names Gemini tends to invent → safe replacements
# ---------------------------------------------------------------------------
_COLOR_FIXES = {
    r"\bBLUE_GRAY\b":  "BLUE_E",
    r"\bBLUE_GREY\b":  "BLUE_E",
    r"\bGRAY_BLUE\b":  "BLUE_E",
    r"\bGREY_BLUE\b":  "BLUE_E",
    r"\bLIGHT_BLUE\b": "BLUE_A",
    r"\bDARK_BLUE\b":  "BLUE_E",
    r"\bCYAN\b":       "TEAL_A",
    r"\bINDIGO\b":     "PURPLE_B",
    r"\bVIOLET\b":     "PURPLE_C",
    r"\bLIGHT_GREEN\b":"GREEN_A",
    r"\bDARK_GREEN\b": "GREEN_E",
    r"\bLIGHT_RED\b":  "RED_A",
    r"\bDARK_RED\b":   "RED_E",
    r"\bLIGHT_GRAY\b": "GRAY_A",
    r"\bDARK_GRAY\b":  "GRAY_E",
    r"\bLIGHT_GREY\b": "GRAY_A",
    r"\bDARK_GREY\b":  "GRAY_E",
}

# ---------------------------------------------------------------------------
# Known bad Manim Axes/Mobject API calls Gemini tends to invent → corrections
# These are applied as simple regex substitutions on the raw code text.
# ---------------------------------------------------------------------------
_API_FIXES = {
    # axes.get_function / axes.get_graph → axes.plot (Manim v0.19 API)
    r"\.get_function\(": ".plot(",
    r"\.get_graph\(": ".plot(",
    # axes.coords_to_point → axes.c2p
    r"\.coords_to_point\(": ".c2p(",
    # axes.point_to_coords → axes.p2c
    r"\.point_to_coords\(": ".p2c(",
}

def strip_fences(text: str) -> str:
    """Remove markdown code fences (```python ... ``` or ``` ... ```)."""
    # Remove opening fence with optional language tag
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text.strip(), flags=re.MULTILINE)
    # Remove closing fence
    text = re.sub(r"^```\s*$", "", text.strip(), flags=re.MULTILINE)
    return text.strip()

def sanitize_code(code: str) -> str:
    """Patch known bad color names and API calls Gemini commonly gets wrong."""
    # 1. Color name fixes
    for pattern, replacement in _COLOR_FIXES.items():
        new_code = re.sub(pattern, replacement, code)
        if new_code != code:
            print(f"  [sanitizer] replaced color {pattern!r} → {replacement!r}")
        code = new_code

    # 2. API method fixes
    for pattern, replacement in _API_FIXES.items():
        new_code = re.sub(pattern, replacement, code)
        if new_code != code:
            print(f"  [sanitizer] replaced API {pattern!r} → {replacement!r}")
        code = new_code

    # Fix: config.frame_* placed before 'from manim import *' → NameError.
    # Move any such lines to immediately after the manim import line.
    lines = code.split("\n")
    config_frame_lines = []
    other_lines = []
    for line in lines:
        if re.match(r"^\s*config\.(frame_width|frame_height)\s*=", line):
            config_frame_lines.append(line)
        else:
            other_lines.append(line)

    if config_frame_lines:
        # Find 'from manim import *' (or 'import manim') in the remaining lines
        manim_idx = None
        for i, line in enumerate(other_lines):
            if re.match(r"^\s*from manim import", line) or re.match(r"^\s*import manim", line):
                manim_idx = i
                break

        if manim_idx is not None:
            rebuilt = (
                other_lines[: manim_idx + 1]
                + config_frame_lines
                + other_lines[manim_idx + 1 :]
            )
        else:
            # No manim import found — prepend one, then config lines
            rebuilt = ["from manim import *"] + config_frame_lines + other_lines
            print("  [sanitizer] added missing 'from manim import *'")

        new_code = "\n".join(rebuilt)
        if new_code != code:
            print("  [sanitizer] moved config.frame_* to after 'from manim import *'")
        code = new_code

    return code

def sanitize_scene(code: str) -> str:
    # First apply our API and color sanitization fixes
    code = sanitize_code(code)
    # Fix unterminated strings by checking syntax
    try:
        compile(code, "scene.py", "exec")
    except SyntaxError as e:
        # Truncate at last valid complete statement before the error line
        lines = code.splitlines()
        code = "\n".join(lines[:e.lineno - 1])
        # Close any open class/def blocks
        code += "\n        self.wait(1)\n"
    return code

def concept_to_slug(concept: str) -> str:
    """Convert concept name to a safe filename slug."""
    return re.sub(r"[^\w]+", "_", concept.strip().lower()).strip("_")

def find_rendered_mp4() -> str | None:
    """
    Manim writes output to media/videos/scene/<quality>/GeneratedScene.mp4.
    Walk the media/ tree to find it.
    """
    for root, _dirs, files in os.walk("media"):
        for fname in files:
            if fname == "GeneratedScene.mp4":
                return os.path.join(root, fname)
    return None
