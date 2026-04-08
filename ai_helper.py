import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_email_reply(original_email, tone, reply_length):
    prompt = f"""
Read the following incoming email and write a reply.

Tone: {tone}
Length: {reply_length}

Incoming email:
{original_email}

Write a clear and ready-to-send reply.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        return f"AI service error: {e}"


def improve_email_reply(reply_text):
    prompt = f"""
Improve the following email reply. Make it clearer and more professional.

Reply:
{reply_text}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        return f"AI service error: {e}"