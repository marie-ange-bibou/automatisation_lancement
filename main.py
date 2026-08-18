"""Orchestrateur: détecte, compile, exécute (6 configs CPU x 5 runs) et collecte les résultats."""
from config import CODES_DIR, CPU_CONFIGS, RESULTS_FILE
from detector import detect
from compiler import compile_code
from runner import run_config
from collector import median_or_none, save_results


def main() -> None:
    results: dict = {}

    code_dirs = sorted(p for p in CODES_DIR.iterdir() if p.is_dir())
    for code_dir in code_dirs:
        name = code_dir.name
        print(f"[{name}] détection...")

        try:
            code_type = detect(code_dir)
        except ValueError as e:
            print(f"[{name}] ignoré: {e}")
            results[name] = {"error": str(e)}
            save_results(results, RESULTS_FILE)
            continue

        print(f"[{name}] type détecté: {code_type.value}, compilation...")
        ok, error = compile_code(code_dir, code_type)
        if not ok:
            print(f"[{name}] erreur de compilation: {error}")
            results[name] = {"error": f"compilation failed: {error}"}
            save_results(results, RESULTS_FILE)
            continue

        code_results = {}
        for cpus in CPU_CONFIGS:
            print(f"[{name}] exécution avec --cpus={cpus}...")
            durations = run_config(code_dir, cpus, code_type)
            median = median_or_none(durations)
            code_results[f"{cpus}cpu"] = median
            print(f"[{name}] {cpus}cpu -> médiane={median}")

        results[name] = code_results
        save_results(results, RESULTS_FILE)

    print(f"Terminé. Résultats écrits dans {RESULTS_FILE}")


if __name__ == "__main__":
    main()
