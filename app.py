import streamlit as st
import requests, time

st.set_page_config(page_title="Text to Animation", layout="centered")
st.title("🎬 Text to Animation")
st.caption("Enter any STEM concept and get an animated explainer video.")

col1, col2 = st.columns([3, 1])
with col1:
    concept = st.text_input("Concept", placeholder="e.g. Fourier Series")
with col2:
    backend = st.selectbox("Backend", ["gemini", "claude", "openai"])

if st.button("Generate Animation", use_container_width=True):
    if not concept.strip():
        st.warning("Please enter a concept.")
    else:
        res = requests.post("http://localhost:8000/generate", json={"concept": concept, "backend": backend})
        job_id = res.json()["job_id"]

        progress_bar = st.progress(0)
        status_text = st.empty()

        while True:
            poll = requests.get(f"http://localhost:8000/status/{job_id}").json()
            progress_bar.progress(poll["progress"])
            status_text.text(f"Status: {poll['step']}")

            if poll["status"] == "done":
                st.success("✅ Video ready!")
                video_bytes = requests.get(f"http://localhost:8000/video/{job_id}").content
                st.video(video_bytes)
                st.download_button(
                    "⬇️ Download Video",
                    data=video_bytes,
                    file_name=f"{concept}.mp4",
                    mime="video/mp4"
                )
                break
            elif poll["status"] == "failed":
                st.error(f"❌ Failed: {poll['error']}")
                break

            time.sleep(2)
