import json
from datetime import datetime


def load_config():
    with open("config.json") as f:
        return json.load(f)


def load_jobs():
    with open("data/sample_jobs.json") as f:
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


def filter_jobs(jobs, config):
    results = []

    for job in jobs:
        if not is_recent(job["date_posted"], config["max_age_days"]):
            continue

        if contains_excluded(job, config["exclude"]):
            continue

        if not matches_keywords(job, config["keywords"]):
            continue

        job["score"] = score_job(job, config)
        results.append(job)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results