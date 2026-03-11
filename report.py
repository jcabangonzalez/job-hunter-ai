from datetime import datetime
import os


def build_report(jobs_with_analysis):
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"reports/{today}_jobs.md"

    os.makedirs("reports", exist_ok=True)

    lines = []
    lines.append("# Job Hunter Report\n")

    if not jobs_with_analysis:
        lines.append("No relevant jobs found.\n")
    else:
        for idx, item in enumerate(jobs_with_analysis, start=1):
            job = item["job"]
            analysis = item["analysis"]

            lines.append(f"## {idx}. {job['title']}\n")
            lines.append(f"- Company: {job['company']}\n")
            lines.append(f"- Location: {job['location']}\n")
            lines.append(f"- Score: {job['score']}\n")
            lines.append(f"- URL: {job['url']}\n")
            lines.append("- LLM Analysis:\n")
            lines.append(f"```text\n{analysis}\n```\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filename
