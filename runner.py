"""Exécute le binaire dans un conteneur Docker neuf par run, avec limite CPU et timeout."""
import subprocess
import time
import uuid
from pathlib import Path
from typing import Optional

from config import DOCKER_IMAGE, EXEC_NAME, RUNS_PER_CONFIG, TIMEOUT_SECONDS, image_tag_for
from detector import CodeType


def run_config(code_dir: Path, cpus: int, code_type: CodeType) -> list[float]:
    """Lance RUNS_PER_CONFIG exécutions avec --cpus=cpus, retourne les durées réussies (secondes)."""
    durations = []
    for _ in range(RUNS_PER_CONFIG):
        duration = _run_once(code_dir, cpus, code_type)
        if duration is not None:
            durations.append(duration)
    return durations


def _check_executable_present(code_dir: Path) -> None:
    executable = code_dir / EXEC_NAME

    if not executable.exists():
        raise FileNotFoundError(f"Exécutable introuvable : {executable}")

    if not executable.is_file():
        raise ValueError(f"Ce n'est pas un fichier : {executable}")


def _build_cmd(code_dir: Path, cpus: int, code_type: CodeType, container_name: str) -> list[str]:
    base = [
        "docker", "run", "--rm", "--privileged",
        f"--cpus={cpus}",
        "--name", container_name,
    ]

    if code_type == CodeType.DOCKERFILE:
        return base + [image_tag_for(code_dir)]

    _check_executable_present(code_dir)
    return base + [
        "-v", f"{code_dir.resolve()}:/code",
        "-w", "/code",
        DOCKER_IMAGE,
        "sh", "-c", f"chmod +x ./{EXEC_NAME} && ./{EXEC_NAME}",
    ]


def _run_once(code_dir: Path, cpus: int, code_type: CodeType) -> Optional[float]:
    container_name = f"bench-{uuid.uuid4().hex[:12]}"
    cmd = _build_cmd(code_dir, cpus, code_type, container_name)

    start = time.perf_counter()
    try:
        subprocess.run(cmd, capture_output=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "kill", container_name], capture_output=True)
        return None
    elapsed = time.perf_counter() - start

    return elapsed
