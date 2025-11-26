from playwright.sync_api import sync_playwright  # Changed from async_playwright
from bs4 import BeautifulSoup
import time
import requests
from bs4 import BeautifulSoup


def fetch_page_html_and_screenshot(url: str, log_callback=print):
    """
    Fetches screenshot + HTML + visible text using SYNCHRONOUS Playwright.
    This prevents 'Event Loop' hangs in Streamlit.
    """
    html = screenshot = extracted_text = None
    console_logs = []

    try:
        with sync_playwright() as p:
            log_callback("Launching browser...")
            
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"] 
            )

            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (compatible; QAWebApp/1.0)"
            )

            page = context.new_page()

            # Capture console logs
            page.on("console", lambda msg: console_logs.append({
                "type": msg.type,
                "text": msg.text
            }))

            log_callback(f"Navigating to {url}...")
            
            # wait_until="domcontentloaded" is 5x faster than "networkidle"
            page.goto(url, wait_until="domcontentloaded", timeout=15000)

            # Short static sleep to allow animations/lazy-loading to settle
            time.sleep(2) 

            title = page.title()
            log_callback(f"Page loaded: {title}")

            log_callback("Capturing screenshot...")
            screenshot = page.screenshot(full_page=False) # full_page=False is faster and often enough for QA

            log_callback("Extracting HTML...")
            html = page.content()

            log_callback("Extracting visible text...")
            soup = BeautifulSoup(html, "html.parser")
            extracted_text = soup.get_text(separator="\n", strip=True)

            browser.close()
            log_callback("Browser closed — done!")

            return html, screenshot, extracted_text, console_logs

    except Exception as e:
        log_callback(f"❌ Error: {str(e)}")
        # Return Nones so the app handles it gracefully
        return None, None, None, None
    

def fetch_page_html(url: str, log_callback=print):
    """
    Fetch a webpage using requests.
    
    Returns:
        html (str)
        screenshot_bytes (bytes or None)
        extracted_text (str)
    """

    try:
        # -----------------------------
        # 1. Fetch HTML using requests
        # -----------------------------
        log_callback(f"Fetching HTML from {url} ...")

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; QAWebApp/1.0)"
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        html = response.text
        log_callback("HTML fetched successfully.")

        # -----------------------------
        # 2. Extract visible text
        # -----------------------------
        log_callback("Extracting visible text from HTML...")
        soup = BeautifulSoup(html, "html.parser")
        extracted_text = soup.get_text(separator="\n", strip=True)
        log_callback("Text extraction complete.")

        # -----------------------------
        # 3. Fetch Screenshot via external service
        # -----------------------------
        log_callback("Capturing screenshot (external API)...")

        screenshot_url = f"https://image.thum.io/get/fullpage/{url}"

        screenshot_response = requests.get(screenshot_url, timeout=20)

        if screenshot_response.status_code == 200:
            screenshot_bytes = screenshot_response.content
            log_callback("Screenshot captured successfully.")
        else:
            screenshot_bytes = None
            log_callback("Warning: Screenshot service failed.")

        return html, screenshot_bytes, extracted_text

    except Exception as e:
        log_callback(f"❌ Error during fetch: {str(e)}")
        return None, None, None
