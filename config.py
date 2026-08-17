"""Paramètres globaux du benchmark."""
from pathlib import Path

CODES_DIR = Path("codes")
RESULTS_FILE = Path("results.json")

DOCKER_IMAGE = "gcc:latest"
EXEC_NAME = "exploit"

CPU_CONFIGS = [1, 2, 4, 8, 16, 32]
RUNS_PER_CONFIG = 5
TIMEOUT_SECONDS = 6 * 60
