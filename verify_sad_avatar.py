import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("http://localhost:8000")

        # Give the page a moment to load and populate the dropdown
        await asyncio.sleep(2)

        # Force the selection using evaluate to bypass visibility checks
        await page.evaluate('document.getElementById("playerSelect").value = "frazer-consultant-1"')

        await page.click("#startGameBtn")

        await page.wait_for_selector('input[name="scopt"]')

        # Deliberately answer incorrectly. We need to find the *wrong* answer.
        correct_answer = await page.inner_text("body:has(#correct-answer) #correct-answer") # hidden element
        wrong_answer = "A"
        if correct_answer == "A":
            wrong_answer = "B"

        await page.click(f'input[name="scopt"][value="{wrong_answer}"]')
        await page.click("#answerBtn")

        await page.wait_for_selector(".explain-dialog")
        await page.screenshot(path="sad_avatar_popup.png")

        await browser.close()

if __name__ == "__main__":
    # Temporarily add the correct answer to the DOM for the script to read
    with open("js/script.js", "r+") as f:
        content = f.read()
        if '<div id="correct-answer"' not in content:
            f.seek(0)
            f.write(content.replace(
                '<h2>Scenario</h2>',
                '<h2>Scenario</h2><div id="correct-answer" style="display: none;">${sc.correct}</div>'
            ))

    asyncio.run(main())

    # Clean up the temporary change
    with open("js/script.js", "r+") as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('<div id="correct-answer" style="display: none;">${sc.correct}</div>', ''))
