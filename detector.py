"""Détecte le type de code source dans un dossier: binaire compilé, Makefile, ou fichiers .c bruts."""
from enum import Enum
from pathlib import Path


class CodeType(Enum):
    BINARY = "binary"
    MAKEFILE = "makefile"
    RAW_C = "raw_c"


def detect(code_dir: Path) -> CodeType:
    files = [f for f in code_dir.iterdir() if f.is_file()]

    if any(f.name.lower() == "makefile" for f in files):
        return CodeType.MAKEFILE

    if any(f.suffix == ".c" for f in files):
        return CodeType.RAW_C

    if files:
        return CodeType.BINARY

    raise ValueError(f"aucun fichier reconnu dans {code_dir}")
