# app.py
import streamlit as st
from utils.llm import GeminiLLM
from utils.helpers import fetch_page_html_and_screenshot, fetch_page_html
from modules.seo_analyzer import SEOAnalyzer
from modules.visual_analyzer import VisualAnalyzer
from modules.content_analyzer import ContentAnalyzer
from modules.agentic_analyzer import AgenticAnalyzer
import asyncio

@st.cache_resource
def get_llm():
    return GeminiLLM()

@st.cache_resource
def get_analyzers():
    llm = get_llm()
    return {
        "seo": SEOAnalyzer(llm),
        "visual": VisualAnalyzer(llm),
        "content": ContentAnalyzer(llm),
        "Agentic_QA": AgenticAnalyzer("config.json")
    }

analyzers = get_analyzers()

st.title("🔍 Webpage QA Analyzer")

url = st.text_input("Enter a webpage URL")

if st.button("Analyze Page"):
    if not url:
        st.error("Please enter a valid URL.")
        st.stop()

    # Status to show progress
    with st.status("Fetching Page...", expanded=True) as status:

        # Collect UI logs
        logs = []

        def log_to_ui(message):
            logs.append(message)
            st.write(f"• {message}")

        # Fetch page with logging
        html, screenshot, text = fetch_page_html(
            url, log_callback=log_to_ui
        )
        # html, screenshot, text, cons_logs = fetch_page_html_and_screenshot(
        #     url, log_callback=log_to_ui
        # )

        if html is None:
            status.update(label="❌ Failed to fetch page. Check the logs below", 
                          state="error")
            st.stop()

        status.update(label="✅ Page fetched successfully.", state="complete")

    if screenshot:
        with st.status(f"Click to check web page overview", 
                       expanded=False) as screenshot_status:
            st.image(screenshot, caption="Webpage Screenshot", 
                    #  width= "auto",
                    #  use_column_width=True
                    )

    st.subheader("Analysis Results")
    tab_seo, tab_visual, tab_content, tab_agent = st.tabs(
        ["SEO", "Visual/UX", "Content", "QA by Agent"]
    )

    with tab_seo:
        seo_placeholder = st.empty()
        seo_placeholder.write("Running SEO analysis via LLM...")

    with tab_visual:
        ux_placeholder = st.empty()
        ux_placeholder.write("Running UX analysis via LLM...")

    with tab_content:
        c_placeholder = st.empty()
        c_placeholder.write("Evaluating content quality via LLM ...")

    with tab_agent:
        agent_placeholder = st.empty()
        agent_placeholder.write("End-to-end QA analysis by a browsing agent ...")

    seo_placeholder.write(analyzers["seo"].analyze(html))
    ux_placeholder.write(analyzers["visual"].analyze(html, screenshot))
    c_placeholder.write(analyzers["content"].analyze(text))
    agent_placeholder.write(
        asyncio.run(
            analyzers["Agentic_QA"].analyze(url)
            )
            )
    
