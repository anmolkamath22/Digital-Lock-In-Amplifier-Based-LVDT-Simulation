"""Generate all eight static PNG diagnostics and supporting numerical studies."""
import argparse
import logging
from pathlib import Path
from lvdt_sim.validation import studies
from lvdt_sim.diagnostics import generate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--trials", type=int, default=1000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        report = studies(args.output_dir, args.trials)
        paths = generate(args.output_dir, report)
    except (ValueError, RuntimeError, OSError) as error:
        parser.exit(1, f"ERROR: {error}\n")
    logging.info("Saved %d PNG diagnostics to %s", len(paths), args.output_dir / "diagnostics")


if __name__ == "__main__":
    main()
