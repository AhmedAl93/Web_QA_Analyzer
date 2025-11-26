class VisualAnalyzer:
    def __init__(self, llm):
        self.llm = llm

    def analyze(self, html: str, screenshot_bytes: bytes):
        prompt = f"""
You are a UX/UI QA expert.
Evaluate the webpage design using the screenshot and HTML.
Identify:

- layout issues (overlaps, misalignments, empty whitespace)
- visual hierarchy clarity
- color contrast problems
- intrusive popups
- mobile/desktop inconsistencies
- readability problems
- CTA visibility and clarity
- overall aesthetics and trust signals

Return your findings as bullet points grouped by category. Here is the HTML: {html}
"""
        return self.llm.analyze_multimodal(
            prompt= prompt,
            # html=html,
            image_bytes= screenshot_bytes
        )