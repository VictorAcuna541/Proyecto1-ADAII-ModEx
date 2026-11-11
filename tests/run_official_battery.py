
import csv
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

BATTERY = ROOT / "bateria_pruebas"
OUTPUT = ROOT / "reports" / "official_battery_results.csv"

ALGORITHMS = ["Fuerza Bruta", "Voraz", "Programación Dinámica"]
TIMEOUT_SECONDS = 15


def execute_case(path, algorithm):
    from algorithms.brute_force import modexFB
    from algorithms.greedy import modexV
    from algorithms.dynamic_programming import modexPD
    from core.io import parse_input
    from core.calculations import (
        calculate_effort,
        calculate_extremism,
        validate_strategy,
    )

    network = parse_input(path.read_text(encoding="utf-8-sig"))

    functions = {
        "Fuerza Bruta": modexFB,
        "Voraz": modexV,
        "Programación Dinámica": modexPD,
    }

    start = time.perf_counter()
    strategy, effort, extremism = functions[algorithm](network)
    duration = time.perf_counter() - start

    validate_strategy(network, strategy)

    real_effort = calculate_effort(network, strategy)
    real_extremism = calculate_extremism(network, strategy)

    valid = (
        effort == real_effort
        and effort <= network.max_budget
        and math.isfinite(extremism)
        and math.isclose(
            extremism, real_extremism,
            rel_tol=1e-8, abs_tol=1e-8
        )
    )

    return {
        "status": "PASS" if valid else "FAIL",
        "agents": len(network.agents),
        "budget": network.max_budget,
        "effort": effort,
        "extremism": round(extremism, 6),
        "time_seconds": round(duration, 6),
        "detail": "" if valid else "Invalid result",
    }


def run_worker(path, algorithm):
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        str(path),
        algorithm,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

        if result.returncode != 0:
            return {
                "status": "ERROR",
                "detail": result.stderr.strip()[-300:],
            }

        return json.loads(result.stdout)

    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "detail": f"Exceeded {TIMEOUT_SECONDS} seconds",
        }
    except Exception as exc:
        return {"status": "ERROR", "detail": str(exc)}


def main():
    from core.io import parse_input

    files = sorted(
        BATTERY.glob("Prueba*.txt"),
        key=lambda p: int(re.search(r"\d+", p.stem).group()),
    )

    if not files:
        print("No official test files were found.")
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for path in files:
        try:
            network = parse_input(
                path.read_text(encoding="utf-8-sig")
            )
        except Exception as exc:
            print(f"{path.name}: INPUT ERROR - {exc}")
            continue

        n = len(network.agents)

        for algorithm in ALGORITHMS:
            skip = (
                algorithm == "Fuerza Bruta" and n > 20
            ) or (
                algorithm == "Programación Dinámica"
                and (n > 500 or network.max_budget > 20000)
            )

            if skip:
                result = {
                    "status": "SKIPPED",
                    "detail": "Resource safety limit",
                }
            else:
                result = run_worker(path, algorithm)

            row = {
                "file": path.name,
                "algorithm": algorithm,
                "agents": n,
                "budget": network.max_budget,
                "status": result["status"],
                "effort": result.get("effort", ""),
                "extremism": result.get("extremism", ""),
                "time_seconds": result.get("time_seconds", ""),
                "detail": result.get("detail", ""),
            }
            rows.append(row)

            print(
                f"{path.name:15} | {algorithm:21} | "
                f"{row['status']}"
            )

    fields = [
        "file", "algorithm", "agents", "budget",
        "status", "effort", "extremism",
        "time_seconds", "detail",
    ]

    with OUTPUT.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nCases found: {len(files)}")
    for status in ["PASS", "FAIL", "ERROR", "TIMEOUT", "SKIPPED"]:
        count = sum(r["status"] == status for r in rows)
        print(f"{status}: {count}")

    print(f"\nResults saved to: {OUTPUT}")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--worker":
        try:
            output = execute_case(
                Path(sys.argv[2]), sys.argv[3]
            )
            print(json.dumps(output))
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)
    else:
        main()
