import json
import os
from datetime import datetime

SEEN_JOBS_FILE = os.path.join(os.path.dirname(__file__), "seen_jobs.json")


def load_config():
    with open("config.json") as f:
        return json.load(f)


def load_jobs():
    import os
    import glob
    files = sorted(glob.glob("data/jobs_*.json"))
    if not files:
        files = ["data/sample_jobs.json"]
    with open(files[-1]) as f:
        return json.load(f)


def is_recent(date_posted, max_days):
    posted = datetime.strptime(date_posted, "%Y-%m-%d")
    age = (datetime.today() - posted).days
    return age <= max_days


def matches_keywords(job, keywords):
    text = (job["title"] + " " + job["description"]).lower()
    return any(k.lower() in text for k in keywords)


def contains_excluded(job, exclude):
    text = (job["title"] + " " + job["description"] + " " + job["location"]).lower()
    return any(e.lower() in text for e in exclude)


def score_job(job, config):
    score = 0
    text = (job["title"] + " " + job["description"] + " " + job["location"]).lower()

    for keyword in config["keywords"]:
        if keyword.lower() in text:
            score += 3

    for level in config["preferred_levels"]:
        if level.lower() in text:
            score += 2

    if "remote" in text:
        score += 2

    return score


def load_seen_jobs(filepath: str = SEEN_JOBS_FILE) -> set:
    if not os.path.isfile(filepath):
        return set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data) if isinstance(data, list) else set()
    except (json.JSONDecodeError, OSError):
        return set()


def save_seen_jobs(seen: set, filepath: str = SEEN_JOBS_FILE) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, indent=2)


def job_key(job: dict) -> str:
    return job.get("url") or f"{job.get('title', '')}|{job.get('company', '')}"


def filter_jobs(jobs, config):
    results = []
    seen_jobs = load_seen_jobs()
    seen_updated = False

    for job in jobs:
        if not is_recent(job["date_posted"], config["max_age_days"]):
            continue

        if contains_excluded(job, config["exclude"]):
            continue

        if not matches_keywords(job, config["keywords"]):
            continue

        key = job_key(job)
        if key in seen_jobs:
            continue

        job["score"] = score_job(job, config)
        seen_jobs.add(key)
        seen_updated = True
        results.append(job)

    if seen_updated:
        save_seen_jobs(seen_jobs)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results