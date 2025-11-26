class ContentAnalyzer:
    def __init__(self, llm):
        self.llm = llm

    def analyze(self, 
                # html: str, 
                extracted_text: str):
        prompt = """
You are a senior content quality evaluator.
Given the extracted text from a webpage, evaluate:

1. Readability (clarity, grammar, sentence structure)
2. Professionalism / trustworthiness
3. Tone (consistent or not)
4. UX writing quality (button labels, headings)
5. Content completeness and accuracy
6. Spam signals or misleading content

Return structured recommendations.
"""
        return self.llm.analyze_text(prompt, extracted_text)
