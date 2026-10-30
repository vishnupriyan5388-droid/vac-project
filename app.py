import os
import streamlit as st
from dotenv import load_dotenv
from seminar_generator import generate_seminar

load_dotenv()

st.set_page_config(page_title="Technical Seminar Preparation Kit", page_icon="🎓", layout="wide")
st.title("🎓 Technical Seminar Preparation Kit")
st.caption("Enter a topic and generate a structured seminar pack using OpenAI, Groq, or Anthropic Claude.")

with st.sidebar:
    st.header("AI provider")
    provider = st.selectbox("Choose provider", ["Groq", "OpenAI", "Anthropic (Claude)"])
    model_defaults = {
        "Groq": "llama-3.3-70b-versatile",
        "OpenAI": "gpt-4o-mini",
        "Anthropic (Claude)": "claude-3-5-sonnet-latest",
    }
    model = st.text_input("Model", value=model_defaults[provider])
    st.caption("API keys are read from your local .env file. They are not stored by this app.")

with st.form("seminar_form"):
    topic = st.text_input("Seminar topic *", placeholder="e.g. Generative AI in Healthcare")
    col1, col2, col3 = st.columns(3)
    audience = col1.text_input("Target audience", "Undergraduate engineering students")
    duration = col2.selectbox("Duration", ["10 minutes", "15 minutes", "20 minutes", "30 minutes", "45 minutes", "60 minutes"])
    level = col3.selectbox("Technical depth", ["Beginner", "Intermediate", "Advanced"])
    extra = st.text_area("Specific requirements (optional)", placeholder="Include a practical demo, focus on cybersecurity, use examples from industry...")
    submitted = st.form_submit_button("Generate seminar kit", type="primary")

if submitted:
    if not topic.strip():
        st.error("Please enter a seminar topic.")
    else:
        with st.spinner("Preparing your seminar content..."):
            try:
                result = generate_seminar(
                    provider=provider, model=model.strip(), topic=topic.strip(),
                    audience=audience.strip(), duration=duration, level=level, extra=extra.strip()
                )
                st.session_state["seminar_result"] = result
                st.session_state["seminar_topic"] = topic.strip()
            except Exception as exc:
                st.error(f"Generation failed: {exc}")
                st.info("Check that the selected provider's API key is present in your .env file and that your account can access the chosen model.")

if st.session_state.get("seminar_result"):
    st.divider()
    st.subheader(f"Generated seminar pack: {st.session_state.get('seminar_topic', '')}")
    content = st.session_state["seminar_result"]
    st.markdown(content)
    st.download_button(
        "Download seminar content (.md)",
        data=content,
        file_name="seminar_preparation_kit.md",
        mime="text/markdown"
    )
