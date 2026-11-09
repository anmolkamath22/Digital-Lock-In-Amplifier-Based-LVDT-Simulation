"""Shared CLI handling; install lvdt_sim with pip install -e . before use."""

import argparse
import logging
from pathlib import Path
from lvdt_sim.config import Config
from lvdt_sim.pipeline import run, export_simulation, standard_scenarios


def vector_cli(description: str) -> None:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", type=Path, default=Path("configs/baseline.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--name", help="Scenario directory name; defaults to config filename stem")
    parser.add_argument("--stream-id", type=int, default=0)
    parser.add_argument("--all", action="store_true", help="Generate the ten standard independent scenarios")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        c = Config.load(args.config)
        cases = standard_scenarios(c) if args.all else {args.name or args.config.stem: c}
        for i, (name, config) in enumerate(cases.items()):
            sim = run(config, args.stream_id+i)
            export_simulation(sim, args.output_dir, name)
            logging.info("%s: %d samples, %d windows, %d clipped", name, config.sample_count,
                         len(sim.fixed.accumulator), sim.adc.clipped_count)
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(1, f"ERROR: {error}\n")
