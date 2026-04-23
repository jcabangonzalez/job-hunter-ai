import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:latest"


def build_prompt(job):
    return f"""
You are a job fit evaluator. Respond ONLY in this exact format, nothing else:

VERDICT: <STRONG | MEDIUM | WEAK>
REASON: <one sentence max>

Candidate: Python, Cybersecurity, SOC, Log analysis, Automation. Remote only. Entry/junior/intermediate level.

Job:
Title: {job.get("title", "")}
Location: {job.get("location", "")}
Description: {job.get("description", "")}
"""

def analyze_job_with_ollama(job):
    prompt = build_prompt(job)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()