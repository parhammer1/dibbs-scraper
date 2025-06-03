"""Utility functions integrating OpenAI GPT for analysis and email generation."""

import os
from typing import Dict

import openai

# Make sure to set OPENAI_API_KEY in your environment
openai.api_key = os.getenv("OPENAI_API_KEY")


PROMPT_TEMPLATE = (
    "You are an expert in government procurement. "
    "Summarize the following solicitation and highlight key action items:\n{solicitation}"
)

EMAIL_TEMPLATE = (
    "You are a helpful assistant tasked with drafting a professional email to a supplier.\n"
    "Solicitation info: {solicitation}.\n"
    "Write a short email asking for a quote, referencing the solicitation number."
)


def summarize_solicitation(text: str) -> str:
    """Return a short summary of the solicitation using OpenAI GPT."""
    if not openai.api_key:
        return "[OpenAI API key not configured]"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(solicitation=text)}],
    )
    return response.choices[0].message["content"].strip()


def generate_email(data: Dict) -> str:
    """Generate an outreach email for the given solicitation data."""
    if not openai.api_key:
        return "[OpenAI API key not configured]"
    solicitation_text = f"Solicitation {data.get('solicitation')} - {data.get('description')}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": EMAIL_TEMPLATE.format(solicitation=solicitation_text)}],
    )
    return response.choices[0].message["content"].strip()
