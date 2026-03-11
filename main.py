from filter import load_config, load_jobs, filter_jobs
from ranker import analyze_job_with_ollama
from report import build_report


def main():
    config = load_config()
    jobs = load_jobs()
    filtered = filter_jobs(jobs, config)

    print("\nRESULTADOS ORDENADOS\n")

    jobs_with_analysis = []

    for job in filtered:
        print(f"Título: {job['title']}")
        print(f"Empresa: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Score: {job['score']}")
        print(f"URL: {job['url']}")
        print("Evaluación LLM:")

        analysis = analyze_job_with_ollama(job)
        print(analysis)
        print("-" * 40)

        jobs_with_analysis.append({
            "job": job,
            "analysis": analysis
        })

    report_file = build_report(jobs_with_analysis)
    print(f"\nReporte guardado en: {report_file}")


if __name__ == "__main__":
    main()
