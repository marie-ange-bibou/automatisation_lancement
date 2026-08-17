"""Détecte le type de code source dans un dossier: binaire compilé, Makefile, ou fichiers .c bruts."""
from enum import Enum
from pathlib import Path

from config import EXEC_NAME


class CodeType(Enum):
    BINARY = "binary"
    MAKEFILE = "makefile"
    RAW_C = "raw_c"


def detect(code_dir: Path) -> CodeType:
    files = [f for f in code_dir.iterdir() if f.is_file()]

    if any(f.name == EXEC_NAME for f in files):
        return CodeType.BINARY

    if any(f.name.lower() == "makefile" for f in files):
        return CodeType.MAKEFILE

    if any(f.suffix == ".c" for f in files):
        return CodeType.RAW_C

    raise ValueError(f"aucun fichier reconnu dans {code_dir}")
