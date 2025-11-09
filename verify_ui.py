from playwright.sync_api import sync_playwright

def run_verification(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    page.goto("http://localhost:8000")

    # Start the game
    page.click("#startGameBtn")

    # Screenshot of the scenario box
    page.locator("#scenario").screenshot(path="scenario.png")

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)
