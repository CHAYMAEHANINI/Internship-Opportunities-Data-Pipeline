import subprocess


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
    run_command(
        [
            "scrapy",
            "crawl",
            "publimaroc"
        ],
        cwd="pipeline"
    )

    run_command([
        "python",
        "pipeline/transform/transform.py"
    ])
    run_command([
        "python",
        "pipeline/load/load_to_postgres.py"
     ])