"""Compile le code selon son type, dans un conteneur gcc:latest, avant l'exécution."""
import subprocess
from pathlib import Path

from config import DOCKER_IMAGE, EXEC_NAME, image_tag_for
from detector import CodeType


def compile_code(code_dir: Path, code_type: CodeType) -> tuple[bool, str]:
    """Compile (si besoin) et rend le binaire exécutable. Retourne (succès, message d'erreur)."""
    if code_type == CodeType.DOCKERFILE:
        return _build_image(code_dir)

    if code_type == CodeType.MAKEFILE:
        result = _run_in_container(code_dir, "make")
        if result.returncode != 0:
            return False, result.stderr.strip() or result.stdout.strip()
    elif code_type == CodeType.RAW_C:
        result = _run_in_container(code_dir, f"gcc -O2 *.c -o {EXEC_NAME}")
        if result.returncode != 0:
            return False, result.stderr.strip() or result.stdout.strip()

    return _ensure_executable(code_dir)


def _ensure_executable(code_dir: Path) -> tuple[bool, str]:
    exec_path = code_dir / EXEC_NAME
    if not exec_path.exists():
        return False, f"binaire '{EXEC_NAME}' introuvable après compilation"

    result = _run_in_container(code_dir, f"chmod +x {EXEC_NAME}")
    if result.returncode != 0:
        return False, result.stderr.strip()

    return True, ""


def _build_image(code_dir: Path) -> tuple[bool, str]:
    tag = image_tag_for(code_dir)
    result = subprocess.run(
        ["docker", "build", "-t", tag, str(code_dir.resolve())],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return False, result.stderr.strip() or result.stdout.strip()
    return True, ""


def _run_in_container(code_dir: Path, shell_cmd: str) -> subprocess.CompletedProcess:
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{code_dir.resolve()}:/code",
        "-w", "/code",
        DOCKER_IMAGE,
        "sh", "-c", shell_cmd,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)
