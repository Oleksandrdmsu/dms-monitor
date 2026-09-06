from playwright.sync_api import sync_playwright

URL = "https://cherga.dmsu.gov.ua/"

with sync_playwright() as p:
    print("1. Запускаємо Playwright")

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("2. Відкриваємо сайт")
    page.goto(URL, wait_until="networkidle", timeout=60000)

    print("3. Сайт відкритий")

    region = page.get_by_placeholder("Область")
    region.fill("Київ")
    page.wait_for_timeout(1000)

    print("4. Область знайдена")

    page.get_by_text("м. Київ, Київська область", exact=True).click()
    page.wait_for_timeout(1000)

    print("5. Область вибрана")

    unit = page.get_by_placeholder("Територіальний підрозділ ДМС")
    unit.fill("Герцена")
    page.wait_for_timeout(1500)

    print("6. Підрозділ знайдений")

    page.get_by_text(
        "8036 СОД № 2 Шевченківського відділу ЦМУ ДМС м. Київ, вул. Герцена, 9",
        exact=True
    ).click()

    page.wait_for_timeout(500)

    print("7. Підрозділ вибраний")

    page.get_by_text("Далі", exact=True).click()
    page.wait_for_timeout(1500)

    print("8. Сторінка послуг")

    page.get_by_text(
        "Паспорт громадянина України для виїзду за кордон, або у формі картки (ID)",
        exact=True
    ).click()

    page.wait_for_timeout(500)

    page.get_by_text("Далі", exact=True).click()
    page.wait_for_timeout(2000)

    print("9. Календар відкритий")

    print(page.locator("body").inner_text())

    print("10. Натискаємо 7")

    dates = page.get_by_text("7", exact=True)
    print("Знайдено елементів 7:", dates.count())

    dates.first.click()

    page.wait_for_timeout(2000)

    print("11. Після натискання 7")
    print(page.locator("body").inner_text())
