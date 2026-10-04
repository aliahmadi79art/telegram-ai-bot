import os
import time
import requests
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{BASE_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=30
    )


def ask_ai(text):
    response = client.responses.create(
        model="gpt-5.5",
        input=text
    )
    return response.output_text


offset = 0

while True:
    try:
        response = requests.get(
            f"{BASE_URL}/getUpdates",
            params={
                "offset": offset,
                "timeout": 30
            },
            timeout=40
        )

        data = response.json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message")

            if not message or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            text = message["text"]

            if text == "/start":
                send_message(
                    chat_id,
                    "سلام 👋\nپیامت رو بفرست تا با هوش مصنوعی جواب بدم."
                )
                continue

            try:
                answer = ask_ai(text)
                send_message(chat_id, answer)

            except Exception:
                send_message(
                    chat_id,
                    "متأسفم، مشکلی پیش اومد. دوباره امتحان کن."
                )

    except Exception:
        time.sleep(5)
