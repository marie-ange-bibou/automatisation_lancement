"""Exécute le binaire dans un conteneur Docker neuf par run, avec limite CPU et timeout."""
import subprocess
import time
import uuid
from pathlib import Path
from typing import Optional

from config import DOCKER_IMAGE, RUNS_PER_CONFIG, TIMEOUT_SECONDS
from compiler import EXEC_NAME


def run_config(code_dir: Path, cpus: int) -> list[float]:
    """Lance RUNS_PER_CONFIG exécutions avec --cpus=cpus, retourne les durées réussies (secondes)."""
    durations = []
    for _ in range(RUNS_PER_CONFIG):
        duration = _run_once(code_dir, cpus)
        if duration is not None:
            durations.append(duration)
    return durations


def _run_once(code_dir: Path, cpus: int) -> Optional[float]:
    container_name = f"bench-{uuid.uuid4().hex[:12]}"
    cmd = [
        "docker", "run", "--rm", "--privileged",
        f"--cpus={cpus}",
        "--name", container_name,
        "-v", f"{code_dir.resolve()}:/code",
        "-w", "/code",
        DOCKER_IMAGE,
        f"./{EXEC_NAME}",
    ]

    start = time.perf_counter()
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "kill", container_name], capture_output=True)
        return None
    elapsed = time.perf_counter() - start

    if result.returncode != 0:
        return None
    return elapsed
