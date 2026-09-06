import os
from playwright.sync_api import sync_playwright

URL = "https://cherga.dmsu.gov.ua/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Відкриваємо сайт ДМС...")
    page.goto(URL, wait_until="networkidle", timeout=60000)

    print("TITLE:", page.title())
    print("URL:", page.url)

    print("\n--- INPUTS ---")
    for i, el in enumerate(page.locator("input").all()):
        try:
            print(i, {
                "placeholder": el.get_attribute("placeholder"),
                "name": el.get_attribute("name"),
                "type": el.get_attribute("type"),
                "value": el.input_value()
            })
        except:
            pass

    print("\n--- BUTTONS ---")
    for i, el in enumerate(page.locator("button").all()):
        try:
            print(i, el.inner_text())
        except:
            pass

    print("\n--- SELECTS ---")
    for i, el in enumerate(page.locator("select").all()):
        try:
            print(i, el.inner_text())
        except:
            pass

    page.screenshot(path="dms_page.png", full_page=True)

    browser.close()
