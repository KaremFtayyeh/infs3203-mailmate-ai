import os
import time
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    max_retries = 3
    delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except requests.exceptions.HTTPError:
            try:
                print("Gemini API response body:")
                print(response.text)
            except Exception:
                pass

            if response.status_code == 503 and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue

            return "AI service is currently unavailable or misconfigured. Please try again later."

        except requests.exceptions.RequestException as e:
            print("Gemini request failed:", str(e))
            return "AI service is currently unavailable. Please try again later."


def generate_email_reply(original_email, tone, reply_length):
    prompt = f"""
Read the following incoming email and write a reply.

Tone: {tone}
Length: {reply_length}

Incoming email:
{original_email}

Write a clear and ready-to-send reply.
"""
    return call_gemini(prompt)


def improve_email_reply(reply_text):
    prompt = f"""
Improve the following email reply. Make it clearer and more professional.

Reply:
{reply_text}
"""
    return call_gemini(prompt)