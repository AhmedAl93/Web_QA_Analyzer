class SEOAnalyzer:
    def __init__(self, llm):
        self.llm = llm

    def analyze(self, html: str):
        prompt = """
You are an SEO auditor. Analyze the provided HTML and produce SEO-specific feedback.
Focus on:
- meta tags (title, description, robots, canonical)
- heading hierarchy
- internal links quality
- structured data
- thin content detection
- mobile friendliness issues
- missing alt attributes
Provide actionable, concise recommendations.
"""
        return self.llm.analyze_text(prompt, html)
