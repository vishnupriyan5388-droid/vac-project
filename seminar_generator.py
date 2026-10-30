import os
from openai import OpenAI
from anthropic import Anthropic

SYSTEM_PROMPT = """You are an expert technical seminar coach and technical educator.
Create accurate, clear, useful seminar materials. Be explicit about assumptions.
Do not invent citations, papers, statistics, URLs, or product capabilities. If reliable
references cannot be confidently named, provide a 'References to verify' section with
search phrases and authoritative source types instead of fabricated citations.
Use Markdown headings, concise bullets, and technically meaningful examples."""

def build_prompt(topic, audience, duration, level, extra):
    return f"""
Prepare a complete technical seminar kit.

TOPIC: {topic}
TARGET AUDIENCE: {audience or 'General technical audience'}
DURATION: {duration}
TECHNICAL DEPTH: {level}
ADDITIONAL REQUIREMENTS: {extra or 'None'}

Include these sections:
1. Seminar title and one-sentence positioning
2. Abstract (100-150 words)
3. Learning objectives (4-6 measurable objectives)
4. Prerequisite knowledge
5. Timed agenda whose timings add up to the requested duration
6. Detailed seminar content, organized into logical sections with explanations,
   examples, key terms, and transitions
7. Slide-by-slide plan (slide title, key bullets, suggested visual)
8. Speaker notes / suggested narration for each major section
9. Practical demonstration or case study (include steps and expected result)
10. Audience engagement questions or short activity
11. Frequently asked questions with clear answers (at least 8)
12. Conclusion and takeaways
13. References to verify: real authoritative sources only when confident;
    otherwise give targeted search phrases and source types. Clearly flag facts
    or claims the presenter should verify before presenting.

Make the content suitable to present aloud, not just a list of headings.
"""

def generate_seminar(provider, model, topic, audience, duration, level, extra):
    prompt = build_prompt(topic, audience, duration, level, extra)
    if provider == "OpenAI":
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is missing.")
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=model or "gpt-6 luna",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content or ""

    if provider == "Groq":
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY is missing.")
        client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model=model or "llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content or ""

    if provider == "Anthropic (Claude)":
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY is missing.")
        client = Anthropic(api_key=key)
        response = client.messages.create(
            model=model or "claude-3-5-sonnet-latest",
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return "\n\n".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )

    raise ValueError("Unsupported provider.")
