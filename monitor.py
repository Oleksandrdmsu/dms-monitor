from playwright.sync_api import sync_playwright

URL = "https://cherga.dmsu.gov.ua/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    print("Відкриваємо сайт ДМС...")
    page.goto(URL, wait_until="networkidle", timeout=60000)

    # Область
    region = page.get_by_placeholder("Область")
    region.click()
    region.fill("Київ")
    page.wait_for_timeout(1000)

    page.get_by_text("м. Київ, Київська область", exact=True).click()
    page.wait_for_timeout(1000)

    # Підрозділ
    unit = page.get_by_placeholder("Територіальний підрозділ ДМС")
    unit.click()
    unit.fill("Герцена")
    page.wait_for_timeout(1500)

    page.get_by_text(
        "8036 СОД № 2 Шевченківського відділу ЦМУ ДМС м. Київ, вул. Герцена, 9",
        exact=True
    ).click()

    page.wait_for_timeout(500)

    # Далі
    page.get_by_text("Далі", exact=True).click()
    page.wait_for_timeout(1500)

    # Вибір послуги
    service = page.get_by_text(
        "Паспорт громадянина України для виїзду за кордон, або у формі картки (ID)",
        exact=True
    )
    service.click()

    page.wait_for_timeout(500)

    # Далі
    page.get_by_text("Далі", exact=True).click()
    page.wait_for_timeout(3000)

print("\n--- КАЛЕНДАР ---")

# Пробуємо натиснути 7 вересня
page.get_by_text("7", exact=True).click()

page.wait_for_timeout(2000)

print("\n--- ПІСЛЯ НАТИСКАННЯ 7 ---")
print("URL:", page.url)
print(page.locator("body").inner_text())

page.screenshot(path="date_7.png", full_page=True)
