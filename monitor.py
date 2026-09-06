from playwright.sync_api import sync_playwright

URL = "https://cherga.dmsu.gov.ua/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    print("Відкриваємо сайт ДМС...")
    page.goto(URL, wait_until="networkidle", timeout=60000)

    # Вибираємо область
    region = page.get_by_placeholder("Область")
    region.click()
    region.fill("Київ")

    page.wait_for_timeout(1000)

    # Вибираємо запропонований Київ
    page.get_by_text("м. Київ, Київська область", exact=True).click()

    page.wait_for_timeout(1000)

    # Відкриваємо поле підрозділу
    unit = page.get_by_placeholder("Територіальний підрозділ ДМС")
    unit.click()
    unit.fill("Герцена")

    page.wait_for_timeout(2000)

    print("\n--- ПІСЛЯ ВИБОРУ ГЕРЦЕНА ---")
    print(page.locator("body").inner_text())

    page.screenshot(path="herzena.png", full_page=True)

    browser.close()
