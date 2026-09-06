import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://cherga.dmsu.gov.ua/"

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

TARGET_DATES = {
    "7 вересня 2026 р.",
    "8 вересня 2026 р.",
    "9 вересня 2026 р.",
    "10 вересня 2026 р.",
    "11 вересня 2026 р.",
}


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
        },
        timeout=20,
    )

    response.raise_for_status()


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        viewport={"width": 1280, "height": 900},
        locale="uk-UA",
    )

    print("Відкриваємо сайт ДМС...")
    page.goto(URL, wait_until="networkidle", timeout=60000)

    # -----------------------------
    # 1. Область
    # -----------------------------

    region = page.get_by_placeholder("Область")
    region.fill("Київ")
    page.wait_for_timeout(1000)

    page.get_by_text(
        "м. Київ, Київська область",
        exact=True
    ).click()

    page.wait_for_timeout(1000)

    # -----------------------------
    # 2. Підрозділ
    # -----------------------------

    unit = page.get_by_placeholder(
        "Територіальний підрозділ ДМС"
    )

    unit.fill("Герцена")
    page.wait_for_timeout(1500)

    page.get_by_text(
        "8036 СОД № 2 Шевченківського відділу ЦМУ ДМС м. Київ, вул. Герцена, 9",
        exact=True
    ).click()

    page.wait_for_timeout(500)

    # -----------------------------
    # 3. Послуга
    # -----------------------------

    page.get_by_text("Далі", exact=True).click()
    page.wait_for_timeout(1500)

    page.get_by_text(
        "Паспорт громадянина України для виїзду за кордон, або у формі картки (ID)",
        exact=True
    ).click()

    page.wait_for_timeout(500)

    page.get_by_text("Далі", exact=True).click()
    page.wait_for_timeout(2000)

    print("Календар відкритий.")

    # -----------------------------
    # 4. Перевіряємо потрібні дати
    # -----------------------------

    available_dates = []

    date_elements = page.locator(
        'abbr[aria-label]'
    )

    count = date_elements.count()

    print(f"Знайдено дат у календарі: {count}")

    for i in range(count):

        element = date_elements.nth(i)

        aria_label = element.get_attribute("aria-label")

        if not aria_label:
            continue

        if aria_label not in TARGET_DATES:
            continue

        # Перевіряємо, чи дата disabled
        parent = element.locator("..")

        disabled = False

        if element.get_attribute("disabled") is not None:
            disabled = True

        if parent.get_attribute("disabled") is not None:
            disabled = True

        if parent.get_attribute("aria-disabled") == "true":
            disabled = True

        class_name = (
            parent.get_attribute("class") or ""
        ).lower()

        if "disabled" in class_name:
            disabled = True

        print(
            f"{aria_label}: "
            + ("НЕДОСТУПНА" if disabled else "ДОСТУПНА")
        )

        if not disabled:
            available_dates.append(aria_label)

    # -----------------------------
    # 5. Якщо доступних дат немає
    # -----------------------------

    if not available_dates:

        print(
            "На 7–11 вересня доступних дат зараз немає."
        )

        browser.close()

    else:

        print(
            "Знайдено доступні дати:",
            available_dates
        )

        # -----------------------------
        # 6. Відкриваємо першу доступну дату
        # -----------------------------

        target = page.locator(
            f'abbr[aria-label="{available_dates[0]}"]'
        )

        target.click()

        page.wait_for_timeout(2000)

        print("\n--- ПІСЛЯ ВИБОРУ ДАТИ ---")
        print(page.locator("body").inner_text())

        # -----------------------------
        # 7. Telegram
        # -----------------------------

        message = (
            "🚨 ДМС — Є ВІЛЬНА ДАТА!\n\n"
            "Підрозділ: вул. Герцена, 9\n"
            "Послуга: закордонний паспорт\n\n"
            "Доступна дата:\n"
            + "\n".join(available_dates)
            + "\n\n"
            "Перевірити та записатися:\n"
            + URL
        )

        send_telegram(message)

        print("Повідомлення надіслано в Telegram.")

        browser.close()
