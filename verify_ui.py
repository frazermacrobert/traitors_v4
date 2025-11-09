from playwright.sync_api import sync_playwright

def run_verification(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()


    page.goto("http://localhost:8000")

    # Screenshot of the main menu
    page.screenshot(path="main_menu.png")

    # Screenshot of the character selection modal
    page.click("#selectCharacterBtn")
    page.select_option("#playerSelect", "alex-consultant-1")
    page.screenshot(path="character_selection.png")
    page.click("#confirmCharacterBtn")

    # Screenshot of the options modal
    page.click("#optionsBtn")
    page.screenshot(path="options.png")
    page.click("#confirmOptionsBtn")

    # Screenshot of the how to play modal
    page.click("#howToPlayBtn")
    page.screenshot(path="how_to_play.png")
    page.click("#closeRulesBtn")

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)
