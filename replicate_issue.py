from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size({"width": 320, "height": 480})
    page.goto("http://localhost:8000")
    page.screenshot(path="replicate_issue.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
