"""Helper functions that wrap OpenAI's GPT API for summaries and emails."""
import os
from typing import Dict

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

SUMMARY_PROMPT = (
    "You are an expert in government procurement. "
    "Provide a concise summary of the following solicitation:\n{solicitation}"
)

EMAIL_PROMPT = (
    "You are a helpful assistant tasked with drafting a short outreach email to a vendor.\n"
    "Solicitation info: {solicitation}.\n"
    "Write a professional email requesting a quote and referencing the solicitation number."
)


def summarize_solicitation(text: str) -> str:
    """Summarize the solicitation text using GPT."""
    if not openai.api_key:
        return "[OpenAI API key not configured]"
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": SUMMARY_PROMPT.format(solicitation=text)}],
    )
    return resp.choices[0].message["content"].strip()


def generate_outreach_email(data: Dict) -> str:
    """Generate an email for the given solicitation record."""
    if not openai.api_key:
        return "[OpenAI API key not configured]"
    solicitation_text = f"Solicitation {data.get('solicitation')} - {data.get('description')}"
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": EMAIL_PROMPT.format(solicitation=solicitation_text)}],
    )
    return resp.choices[0].message["content"].strip()
