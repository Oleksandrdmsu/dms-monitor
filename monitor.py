import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://cherga.dmsu.gov.ua/"

TARGET_DATES = [
    "7 вересня 2026 р.",
    "8 вересня 2026 р.",
    "9 вересня 2026 р.",
    "10 вересня 2026 р.",
    "11 вересня 2026 р.",
    "12 вересня 2026 р.",
]

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=30,
    )

    response.raise_for_status()


def open_calendar(page):

    print("Відкриваємо сайт ДМС...")

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000,
    )

    # Область
    print("Обираємо область...")

    page.get_by_placeholder(
        "Область"
    ).fill("Київ")

    page.wait_for_timeout(1000)

    page.get_by_text(
        "м. Київ, Київська область",
        exact=True,
    ).click()

    page.wait_for_timeout(1000)

    # Підрозділ
    print("Обираємо Герцена, 9...")

    page.get_by_placeholder(
        "Територіальний підрозділ ДМС"
    ).fill("Герцена")

    page.wait_for_timeout(1500)

    page.get_by_text(
        "8036 СОД № 2 Шевченківського відділу ЦМУ ДМС м. Київ, вул. Герцена, 9",
        exact=True,
    ).click()

    page.wait_for_timeout(500)

    # Далі
    page.get_by_text(
        "Далі",
        exact=True,
    ).click()

    page.wait_for_timeout(1500)

    # Закордонний паспорт
    print("Обираємо закордонний паспорт...")

    page.get_by_text(
        "Паспорт громадянина України для виїзду за кордон, або у формі картки (ID)",
        exact=True,
    ).click()

    page.wait_for_timeout(500)

    page.get_by_text(
        "Далі",
        exact=True,
    ).click()

    page.wait_for_timeout(2000)


def check_dates(page):

    available = []

    for date_label in TARGET_DATES:

        date_element = page.locator(
            f'abbr[aria-label="{date_label}"]'
        )

        if date_element.count() == 0:
            print(
                f"НЕ ЗНАЙДЕНО: {date_label}"
            )
            continue

        # ABBR знаходиться всередині BUTTON
        button = date_element.locator("..")

        disabled = button.is_disabled()

        print(
            f"{date_label}: "
            f"{'ДОСТУПНА' if not disabled else 'недоступна'}"
        )

        if not disabled:
            available.append(date_label)

    return available


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        viewport={
            "width": 1280,
            "height": 900,
        },
        locale="uk-UA",
    )

    try:

        open_calendar(page)

        print()
        print("=" * 60)
        print("ПЕРЕВІРКА ДАТ 7–12 ВЕРЕСНЯ")
        print("=" * 60)

        available_dates = check_dates(page)

        print()
        print("=" * 60)

        if available_dates:

            print("ЗНАЙДЕНО ДОСТУПНІ ДАТИ:")
            
            for date in available_dates:
                print("  ", date)

            message = (
                "🚨 ДМС: З'ЯВИЛАСЯ ДОСТУПНА ДАТА!\n\n"
                "📍 Київ, вул. Герцена, 9\n"
                "📄 Закордонний паспорт\n\n"
                "📅 Доступні дати:\n"
                + "\n".join(
                    f"• {date}"
                    for date in available_dates
                )
                + "\n\n"
                "Перевірте електронну чергу ДМС."
            )

            send_telegram(message)

            print()
            print("Telegram-повідомлення НАДІСЛАНО.")

        else:

            print(
                "Доступних дат 7–12 вересня наразі немає."
            )

        print("=" * 60)

    except Exception as e:

        print()
        print("ПОМИЛКА:")
        print(str(e))

        raise

    finally:

        browser.close()
