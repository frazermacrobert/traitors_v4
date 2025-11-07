from playwright.sync_api import sync_playwright, expect

def run_verification(page):
    page.goto("http://localhost:8000")

    # Start the game
    page.wait_for_selector("#startBtn")
    page.select_option("#playerSelect", "charlie-content-1")
    page.click("#startBtn")

    # --- ROUND 1: Verify grey-out on vote ---
    page.wait_for_selector('#scenario[data-correct-answer]')

    # 1. Answer Scenario 1 CORRECTLY
    correct_answer_1 = page.locator("#scenario").get_attribute("data-correct-answer")
    page.click(f'input[name="scopt"][value="{correct_answer_1}"]')
    page.click("#answerBtn")

    # 2. Vote for a bot to trigger the grey-out
    page.wait_for_selector('.player-card[data-id]:not([data-id="charlie-content-1"])')
    bot_card = page.query_selector('.player-card[data-id]:not([data-id="charlie-content-1"])')
    if bot_card:
        bot_card.click()
    else:
        raise Exception("No bot card found to vote for.")

    # 3. Take screenshot of the greyed-out activity section
    expect(page.locator("#actions.is-disabled")).to_be_visible()
    page.screenshot(path="verify_grey_out.png")

    # --- ROUND 2: Verify grey-out removed AND sad avatar ---

    # 4. Wait for voting to finish and next round to start
    page.wait_for_selector('#scenario[data-correct-answer]')

    # 5. Verify the grey-out is removed
    expect(page.locator("#actions.is-disabled")).not_to_be_visible()
    page.screenshot(path="verify_grey_out_removed.png")

    # 6. Answer Scenario 2 INCORRECTLY
    correct_answer_2 = page.locator("#scenario").get_attribute("data-correct-answer")
    incorrect_answer_2 = "B" if correct_answer_2 == "A" else "A"

    page.click(f'input[name="scopt"][value="{incorrect_answer_2}"]')
    page.click("#answerBtn")

    # 7. Take screenshot of the sad avatar popup
    expect(page.locator(".explain-overlay")).to_be_visible()
    page.screenshot(path="verify_sad_avatar.png")


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            run_verification(page)
        finally:
            browser.close()