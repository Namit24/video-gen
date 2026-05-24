#!/usr/bin/env python3
import argparse, os
from dotenv import load_dotenv
from llm import generate_code
from utils import strip_fences, sanitize_scene
from manim_runner import render

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("concept")
    parser.add_argument("--backend", default="gemini", choices=["gemini", "claude", "openai"])
    args = parser.parse_args()

    print(f"Concept : '{args.concept}'")
    print(f"Backend : {args.backend}")
    print(f"Calling {args.backend}...")

    raw = generate_code(args.concept, args.backend)
    code = sanitize_scene(strip_fences(raw))

    out = render(args.concept, code, args.backend, generate_code)
    print(f"SUCCESS: {out}")

if __name__ == "__main__":
    main()
