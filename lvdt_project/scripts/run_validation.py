"""Run the full unit suite followed by deterministic numerical studies."""
import argparse
import logging
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
from lvdt_sim.validation import studies
from lvdt_sim.export import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--trials", type=int, default=1000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    project = Path(__file__).resolve().parents[1]
    reports = args.output_dir.resolve() / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([sys.executable, "-m", "pytest", str(project / "tests"), "-q",
                             f"--junitxml={reports / 'pytest.xml'}"], cwd=project)
    if result.returncode:
        raise SystemExit(result.returncode)
    tree = ET.parse(reports / "pytest.xml")
    suites = tree.findall(".//testsuite")
    counts = {key: sum(int(s.get(key, "0")) for s in suites) for key in ("tests", "failures", "errors", "skipped")}
    counts["passed"] = counts["tests"]-counts["failures"]-counts["errors"]-counts["skipped"]
    write_json(reports / "test_results.json", counts)
    try:
        report = studies(args.output_dir, args.trials)
    except (ValueError, RuntimeError, OSError) as error:
        parser.exit(1, f"ERROR: {error}\n")
    logging.info("%d tests passed; %d numerical checks passed. Reports: %s", counts["passed"], len(report["checks"]), reports)


if __name__ == "__main__":
    main()
