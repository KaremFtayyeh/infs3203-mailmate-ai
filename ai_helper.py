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

            print("Gemini success response:")
            print(data)

            candidates = data.get("candidates", [])
            if not candidates:
                return "AI service returned no candidates."

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                return "AI service returned no text parts."

            text = parts[0].get("text", "")
            if not text:
                return "AI service returned an empty reply."

            return text

        except requests.exceptions.HTTPError:
            try:
                print("Gemini API error response:")
                print(response.text)
            except Exception:
                print("Could not read Gemini error response.")

            if response.status_code == 503 and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue

            return "AI service is currently unavailable or misconfigured. Please try again later."

        except requests.exceptions.RequestException as e:
            print("Gemini request failed:", str(e))
            return "AI service is currently unavailable. Please try again later."

        except Exception as e:
            print("Unexpected Gemini parsing error:", str(e))
            return "AI service returned an unexpected response. Please try again later."


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