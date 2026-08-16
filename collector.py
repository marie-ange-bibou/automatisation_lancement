"""Calcule la médiane par configuration CPU et écrit le résultat JSON."""
import json
import statistics
from pathlib import Path
from typing import Optional


def median_or_none(durations: list[float]) -> Optional[float]:
    if not durations:
        return None
    return statistics.median(durations)


def save_results(results: dict, output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
