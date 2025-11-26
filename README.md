# Webpage QA Analyzer 🔍

A Streamlit-powered web application that performs comprehensive quality assurance analysis on any public URL.

It combines:
- Static HTML/text analysis
- Screenshot-based visual & UX evaluation
- Full browsing agent capabilities (via [browser-use](https://github.com/browser-use/browser-use))
- Gemini multimodal LLM for intelligent feedback (model name to be specified in config.json)


### Features
The web app includes real-time logs, screenshot preview, and multiple analysis tabs.

| Tab             | Analysis Type                  | Method                              | Key Checks |
|-----------------|--------------------------------|-------------------------------------|-------------------------------------|
| **SEO**         | On-page SEO                    | url → HTML parsing → LLM               | Meta tags, headings, alt texts, structured data |
| **Visual/UX**   | Design & usability             | url → Screenshot + HTML → Multimodal LLM  | Layout issues, contrast, hierarchy |
| **Content**     | Text quality & trustworthiness | url → Extracted text → LLM             | Readability, tone, UX writing |
| **QA by Agent** | End-to-end QA analysis    | url → browsing agent       | Navigation flow, JS errors, accessibility, performance |

---

### Tech Stack

- **Frontend/Backend**: Streamlit
- **Package manager**: [uv](https://docs.astral.sh/uv/)
- **LLM**: Currently gemini-2.5-flash, other models available [here](https://ai.google.dev/gemini-api/docs/models)
- **Browsing Agent**: [browser-use](https://github.com/browser-use/browser-use)
- **HTML & Text**: requests + BeautifulSoup
- **Screenshots**: requests + https://image.thum.io/get/fullpage/

---

### Installation & Local Run

```bash
# 1. Clone the repo
git clone https://github.com/AhmedAl93/Web_QA_Analyzer/tree/master
cd webpage-qa-analyzer

# 2. Install dependencies with uv
uv sync

# 3. Provide environment variables and add necessary API keys
nano .env
# .env should be in this format:
# GEMINI_API_KEY=your_key_here
# BrowserUse_API_KEY=your_key_here

# 4. Launch the app
uv run streamlit run app.py
```
You can get necessary API keys from the following links: [Gemini API](https://ai.google.dev/gemini-api/docs/api-key),
[Browser-Use API](https://github.com/browser-use/browser-use/tree/main#:~:text=Get%20your%20API%20key%20from%20Browser%20Use%20Cloud)

### Current Issues
On some websites with anti-bot protection, the browsing agent raises the following error:
```bash
TimeoutError: Event handler browser_use.browser.watchdog_base.BrowserSession.on_BrowserStartEvent#5136(?▶ BrowserStartEvent#a1c2 🏃) timed out after 30.0s and interrupted any processing of 1 child events
```
A simple fixing attemept would be to increase watchdog timeout, to be experimented later.