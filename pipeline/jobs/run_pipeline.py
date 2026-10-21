import subprocess

SPIDERS = ["publimaroc", "dreamjob"]

def run_command(command, cwd=None):
    result = subprocess.run(
        command,
        cwd=cwd
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}"
        )

if __name__ == "__main__":
    failed_spiders = []

    # 1) Scrapers: a failing spider must not stop the others
    for spider in SPIDERS:
        print(f"===== Spider: {spider} =====", flush=True)

        try:
            run_command(["scrapy", "crawl", spider], cwd="pipeline")
        except Exception as error:
            failed_spiders.append(spider)
            print(f"WARNING: spider '{spider}' failed: {error}", flush=True)

    if len(failed_spiders) == len(SPIDERS):
        raise RuntimeError("All spiders failed, stopping pipeline.")

    # 2) Transform + 3) Load (these must succeed)
    run_command(["python", "pipeline/transform/transform.py"])
    run_command(["python", "pipeline/load/load_to_postgres.py"])

    if failed_spiders:
        print(f"Pipeline finished WITH WARNINGS. Failed spiders: {failed_spiders}")
    else:
        print("Pipeline finished successfully.")