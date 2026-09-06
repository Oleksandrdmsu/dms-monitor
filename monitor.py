from playwright.sync_api import sync_playwright

URL = "https://cherga.dmsu.gov.ua/"

TARGET_DATES = {
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
}

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        viewport={"width": 1280, "height": 900},
        locale="uk-UA",
    )

    print("Відкриваємо сайт ДМС...")

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    # =========================================================
    # 1. ОБЛАСТЬ
    # =========================================================

    print("Обираємо область...")

    page.get_by_placeholder("Область").fill("Київ")
    page.wait_for_timeout(1000)

    page.get_by_text(
        "м. Київ, Київська область",
        exact=True
    ).click()

    page.wait_for_timeout(1000)

    # =========================================================
    # 2. ПІДРОЗДІЛ ДМС
    # =========================================================

    print("Обираємо підрозділ...")

    page.get_by_placeholder(
        "Територіальний підрозділ ДМС"
    ).fill("Герцена")

    page.wait_for_timeout(1500)

    page.get_by_text(
        "8036 СОД № 2 Шевченківського відділу ЦМУ ДМС м. Київ, вул. Герцена, 9",
        exact=True
    ).click()

    page.wait_for_timeout(500)

    # =========================================================
    # 3. ДАЛІ
    # =========================================================

    print("Переходимо до вибору послуги...")

    page.get_by_text(
        "Далі",
        exact=True
    ).click()

    page.wait_for_timeout(1500)

    # =========================================================
    # 4. ЗАКОРДОННИЙ ПАСПОРТ
    # =========================================================

    print("Обираємо послугу закордонного паспорта...")

    page.get_by_text(
        "Паспорт громадянина України для виїзду за кордон, або у формі картки (ID)",
        exact=True
    ).click()

    page.wait_for_timeout(500)

    # =========================================================
    # 5. ВІДКРИВАЄМО КАЛЕНДАР
    # =========================================================

    page.get_by_text(
        "Далі",
        exact=True
    ).click()

    page.wait_for_timeout(2000)

    print()
    print("=" * 60)
    print("КАЛЕНДАР ВІДКРИТО")
    print("=" * 60)

    # =========================================================
    # 6. ЗБЕРІГАЄМО HTML І SCREENSHOT
    # =========================================================

    with open(
        "calendar.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(
            page.locator("body").inner_html()
        )

    page.screenshot(
        path="calendar.png",
        full_page=True
    )

    print("Збережено calendar.html")
    print("Збережено calendar.png")

    # =========================================================
    # 7. ПОКАЗУЄМО ВСІ BUTTON
    # =========================================================

    print()
    print("=" * 60)
    print("УСІ BUTTON НА СТОРІНЦІ")
    print("=" * 60)

    buttons = page.locator("button")

    print(
        "Кількість button:",
        buttons.count()
    )

    for i in range(buttons.count()):

        b = buttons.nth(i)

        try:
            text = b.inner_text().strip()
        except Exception:
            text = ""

        try:
            aria = b.get_attribute("aria-label")
        except Exception:
            aria = None

        try:
            disabled = b.is_disabled()
        except Exception:
            disabled = "N/A"

        try:
            cls = b.get_attribute("class")
        except Exception:
            cls = None

        if text or aria:

            print()
            print(f"BUTTON #{i}")
            print(f"  text     = {text!r}")
            print(f"  aria     = {aria!r}")
            print(f"  disabled = {disabled}")
            print(f"  class    = {cls!r}")

    # =========================================================
    # 8. ШУКАЄМО 7–12
    # =========================================================

    print()
    print("=" * 60)
    print("ДОСЛІДЖЕННЯ ДАТ 7–12")
    print("=" * 60)

    for number in TARGET_DATES:

        locator = page.get_by_text(
            number,
            exact=True
        )

        count = locator.count()

        print()
        print(
            f"ДАТА {number}: знайдено {count} елемент(ів)"
        )

        for i in range(count):

            el = locator.nth(i)

            try:
                tag = el.evaluate(
                    "(e) => e.tagName"
                )
            except Exception:
                tag = "?"

            try:
                text = el.inner_text()
            except Exception:
                text = "?"

            try:
                cls = el.get_attribute("class")
            except Exception:
                cls = None

            try:
                aria = el.get_attribute(
                    "aria-label"
                )
            except Exception:
                aria = None

            try:
                parent_tag = el.evaluate(
                    "(e) => e.parentElement ? e.parentElement.tagName : null"
                )
            except Exception:
                parent_tag = None

            try:
                parent_class = el.evaluate(
                    "(e) => e.parentElement ? e.parentElement.className : null"
                )
            except Exception:
                parent_class = None

            try:
                parent_disabled = el.evaluate(
                    """
                    (e) => e.parentElement
                        ? e.parentElement.disabled
                        : null
                    """
                )
            except Exception:
                parent_disabled = None

            print(f"  Елемент #{i}")
            print(f"    tag             = {tag}")
            print(f"    text            = {text!r}")
            print(f"    class           = {cls!r}")
            print(f"    aria-label      = {aria!r}")
            print(f"    parent tag      = {parent_tag!r}")
            print(f"    parent class    = {parent_class!r}")
            print(f"    parent disabled = {parent_disabled!r}")

    # =========================================================
    # 9. ДОДАТКОВО — ЕЛЕМЕНТИ З ARIA-LABEL
    # =========================================================

    print()
    print("=" * 60)
    print("ЕЛЕМЕНТИ З ARIA-LABEL")
    print("=" * 60)

    aria_elements = page.locator(
        "[aria-label]"
    )

    print(
        "Кількість:",
        aria_elements.count()
    )

    for i in range(
        min(aria_elements.count(), 100)
    ):

        el = aria_elements.nth(i)

        try:
            tag = el.evaluate(
                "(e) => e.tagName"
            )
            aria = el.get_attribute(
                "aria-label"
            )
            text = el.inner_text().strip()
            cls = el.get_attribute("class")

            print(
                f"{i}: "
                f"tag={tag}, "
                f"aria={aria!r}, "
                f"text={text!r}, "
                f"class={cls!r}"
            )

        except Exception:
            pass

    # =========================================================
    # 10. КІНЕЦЬ
    # =========================================================

    print()
    print("=" * 60)
    print("ДІАГНОСТИКА ЗАВЕРШЕНА")
    print("=" * 60)

    browser.close()
