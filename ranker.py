import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:latest"


def build_prompt(job):
    return f"""
You are evaluating whether this job matches a candidate.

Candidate profile:
- Python
- Cybersecurity
- SOC
- Log analysis
- Automation
- Prefers remote jobs
- Prefers entry, junior, or intermediate roles

Job:
Title: {job.get("title", "")}
Company: {job.get("company", "")}
Location: {job.get("location", "")}
Description: {job.get("description", "")}

Return only this format:

fit: <good / medium / weak>
reason: <one short sentence>
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