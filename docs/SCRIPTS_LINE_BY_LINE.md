# Command scripts: every source line explained

Read [START_HERE](START_HERE.md) first. These scripts adapt command-line options to package calls; none implements RTL.

## scripts/_common.py

The connector shared by both vector-generation commands: JSON -> Config -> run -> export_simulation.

Source snapshot SHA-256: `a684fbfe87954b21c6e2965467408251b7cc1255357f83417ae13a9a338716b6`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Shared CLI handling; install lvdt_sim with pip install -e . before use.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>import argparse</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>import logging</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from lvdt_sim.config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code>from lvdt_sim.pipeline import run, export_simulation, standard_scenarios</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code></code> | Blank separator for readability; no operation. |
| 10 | <code>def vector_cli(description: str) -&gt; None:</code> | Defines shared argument parsing and vector generation. |
| 11 | <code>    parser = argparse.ArgumentParser(description=description)</code> | Creates a parser using the calling script's description. |
| 12 | <code>    parser.add_argument(&quot;--config&quot;, type=Path, default=Path(&quot;configs/baseline.json&quot;))</code> | Adds --config, defaulting to configs/baseline.json relative to working directory. |
| 13 | <code>    parser.add_argument(&quot;--output-dir&quot;, type=Path, default=Path(&quot;output&quot;))</code> | Adds --output-dir, default output. |
| 14 | <code>    parser.add_argument(&quot;--name&quot;, help=&quot;Scenario directory name; defaults to config filename stem&quot;)</code> | Adds an optional scenario directory name. |
| 15 | <code>    parser.add_argument(&quot;--stream-id&quot;, type=int, default=0)</code> | Adds a base noise stream ID, default zero. |
| 16 | <code>    parser.add_argument(&quot;--all&quot;, action=&quot;store_true&quot;, help=&quot;Generate the ten standard independent scenarios&quot;)</code> | Adds the boolean --all switch selecting the standard catalog. |
| 17 | <code>    args = parser.parse_args()</code> | Parses command-line arguments. |
| 18 | <code>    logging.basicConfig(level=logging.INFO, format=&quot;%(levelname)s: %(message)s&quot;)</code> | Configures informational logging. |
| 19 | <code>    try:</code> | Starts expected-error handling. |
| 20 | <code>        c = Config.load(args.config)</code> | Loads and validates JSON instrument settings. |
| 21 | <code>        cases = standard_scenarios(c) if args.all else {args.name or args.config.stem: c}</code> | Chooses the standard catalog or a single config named by --name or filename stem. |
| 22 | <code>        for i, (name, config) in enumerate(cases.items()):</code> | Loops through cases in insertion order with a numerical scenario index. |
| 23 | <code>            sim = run(config, args.stream_id+i)</code> | Runs each scenario independently, offsetting stream ID by its index. |
| 24 | <code>            export_simulation(sim, args.output_dir, name)</code> | Exports all matching signal/vector/metadata files. |
| 25 | <code>            logging.info(&quot;%s: %d samples, %d windows, %d clipped&quot;, name, config.sample_count,</code> | Begins a status log with scenario name and sample count. |
| 26 | <code>                         len(sim.fixed.accumulator), sim.adc.clipped_count)</code> | Adds complete-window count and clipped-sample count. |
| 27 | <code>    except (ValueError, TypeError, KeyError, OSError) as error:</code> | Catches expected parameter, missing-key, and filesystem failures. |
| 28 | <code>        parser.exit(1, f&quot;ERROR: {error}\n&quot;)</code> | Prints an error and exits with status 1. |

## scripts/generate_scenarios.py

Thin entry point: both generation scripts call the same shared CLI and produce both vectors and ground truth.

Source snapshot SHA-256: `8afd0ab304416a7d2825c3261a5ec61d75354d108c8f5d352a5bd835a8a193db`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Generate analog ground truth, ADC vectors, metadata and expected sums.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code>from _common import vector_cli</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 3 | <code></code> | Blank separator for readability; no operation. |
| 4 | <code>if __name__ == &quot;__main__&quot;:</code> | Runs the following entry point only when this file is executed as a script, not when imported. |
| 5 | <code>    vector_cli(__doc__)</code> | Calls the shared vector CLI, using this script's docstring as its help description. |

## scripts/generate_hdl_vectors.py

Thin entry point: both generation scripts call the same shared CLI and produce both vectors and ground truth.

Source snapshot SHA-256: `48c5b04dd9590ed987ca4c3d227e4ec9e7d4a0f52e9952790580d6ed61c2ef7c`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Generate complete HDL input/output contracts, including matching ground truth.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code>from _common import vector_cli</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 3 | <code></code> | Blank separator for readability; no operation. |
| 4 | <code>if __name__ == &quot;__main__&quot;:</code> | Runs the following entry point only when this file is executed as a script, not when imported. |
| 5 | <code>    vector_cli(__doc__)</code> | Calls the shared vector CLI, using this script's docstring as its help description. |

## scripts/run_validation.py

Runs pytest and then baseline engineering studies. Failures return nonzero exit status.

Source snapshot SHA-256: `0c406f9b781690f9b46402e7df8b11241141daa27db69fd7386b08ce9e586c91`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Run the full unit suite followed by deterministic numerical studies.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code>import argparse</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>import logging</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>import subprocess</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 6 | <code>import sys</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 7 | <code>import xml.etree.ElementTree as ET</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 8 | <code>from lvdt_sim.validation import studies</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 9 | <code>from lvdt_sim.export import write_json</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 10 | <code></code> | Blank separator for readability; no operation. |
| 11 | <code></code> | Blank separator for readability; no operation. |
| 12 | <code>def main() -&gt; None:</code> | Defines the validation command entry point. |
| 13 | <code>    parser = argparse.ArgumentParser(description=__doc__)</code> | Creates its argument parser. |
| 14 | <code>    parser.add_argument(&quot;--output-dir&quot;, type=Path, default=Path(&quot;output&quot;))</code> | Adds output-directory selection. |
| 15 | <code>    parser.add_argument(&quot;--trials&quot;, type=int, default=1000)</code> | Adds the Monte Carlo trial-count option. |
| 16 | <code>    args = parser.parse_args()</code> | Reads command-line arguments. |
| 17 | <code>    logging.basicConfig(level=logging.INFO, format=&quot;%(levelname)s: %(message)s&quot;)</code> | Configures status logging. |
| 18 | <code>    project = Path(__file__).resolve().parents[1]</code> | Finds the project root relative to this script, independent of current working directory. |
| 19 | <code>    reports = args.output_dir.resolve() / &quot;reports&quot;</code> | Resolves the reports directory absolutely before the child process changes working directory. |
| 20 | <code>    reports.mkdir(parents=True, exist_ok=True)</code> | Creates missing report directories. |
| 21 | <code>    result = subprocess.run([sys.executable, &quot;-m&quot;, &quot;pytest&quot;, str(project / &quot;tests&quot;), &quot;-q&quot;,</code> | Starts pytest using this same Python interpreter and the project's tests folder, in quiet mode. |
| 22 | <code>                             f&quot;--junitxml={reports / &#x27;pytest.xml&#x27;}&quot;], cwd=project)</code> | Requests JUnit XML and runs the child from the project root; waits for completion. |
| 23 | <code>    if result.returncode:</code> | Checks pytest's return status. |
| 24 | <code>        raise SystemExit(result.returncode)</code> | Propagates any nonzero test status and stops further studies. |
| 25 | <code>    tree = ET.parse(reports / &quot;pytest.xml&quot;)</code> | Parses the saved JUnit XML. |
| 26 | <code>    suites = tree.findall(&quot;.//testsuite&quot;)</code> | Finds test-suite elements. |
| 27 | <code>    counts = {key: sum(int(s.get(key, &quot;0&quot;)) for s in suites) for key in (&quot;tests&quot;, &quot;failures&quot;, &quot;errors&quot;, &quot;skipped&quot;)}</code> | Sums total tests, failures, errors, and skipped counts. |
| 28 | <code>    counts[&quot;passed&quot;] = counts[&quot;tests&quot;]-counts[&quot;failures&quot;]-counts[&quot;errors&quot;]-counts[&quot;skipped&quot;]</code> | Computes passed count by subtraction. |
| 29 | <code>    write_json(reports / &quot;test_results.json&quot;, counts)</code> | Writes test_results.json. |
| 30 | <code>    try:</code> | Starts study error handling. |
| 31 | <code>        report = studies(args.output_dir, args.trials)</code> | Runs numerical studies and writes their reports. |
| 32 | <code>    except (ValueError, RuntimeError, OSError) as error:</code> | Catches invalid arguments, failed acceptance checks, and file errors. |
| 33 | <code>        parser.exit(1, f&quot;ERROR: {error}\n&quot;)</code> | Exits with status 1 and a useful message on study failure. |
| 34 | <code>    logging.info(&quot;%d tests passed; %d numerical checks passed. Reports: %s&quot;, counts[&quot;passed&quot;], len(report[&quot;checks&quot;]), reports)</code> | Logs final passing counts and report location. |
| 35 | <code></code> | Blank separator for readability; no operation. |
| 36 | <code></code> | Blank separator for readability; no operation. |
| 37 | <code>if __name__ == &quot;__main__&quot;:</code> | Runs the following entry point only when this file is executed as a script, not when imported. |
| 38 | <code>    main()</code> | Calls the script's main function. |

## scripts/generate_diagnostic_plots.py

Creates default numerical studies and eight static PNGs without opening a window.

Source snapshot SHA-256: `1bce5746be013145707fc6feb0dd0d7a8dc36db08b46f1a4dd74ed390e6cf4db`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Generate all eight static PNG diagnostics and supporting numerical studies.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code>import argparse</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>import logging</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>from lvdt_sim.validation import studies</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from lvdt_sim.diagnostics import generate</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code>def main() -&gt; None:</code> | Defines the plotting entry point. |
| 10 | <code>    parser = argparse.ArgumentParser(description=__doc__)</code> | Creates its argument parser. |
| 11 | <code>    parser.add_argument(&quot;--output-dir&quot;, type=Path, default=Path(&quot;output&quot;))</code> | Adds output-directory selection. |
| 12 | <code>    parser.add_argument(&quot;--trials&quot;, type=int, default=1000)</code> | Adds Monte Carlo trial count for the supporting studies. |
| 13 | <code>    args = parser.parse_args()</code> | Reads arguments. |
| 14 | <code>    logging.basicConfig(level=logging.INFO, format=&quot;%(levelname)s: %(message)s&quot;)</code> | Configures informational logging. |
| 15 | <code>    try:</code> | Starts numerical/file error handling. |
| 16 | <code>        report = studies(args.output_dir, args.trials)</code> | Runs numerical studies so plotted metrics come from an actual reproducible experiment. |
| 17 | <code>        paths = generate(args.output_dir, report)</code> | Creates the eight PNGs and receives saved paths. |
| 18 | <code>    except (ValueError, RuntimeError, OSError) as error:</code> | Catches invalid requests, acceptance failures, and filesystem errors. |
| 19 | <code>        parser.exit(1, f&quot;ERROR: {error}\n&quot;)</code> | Prints the error and exits with status 1. |
| 20 | <code>    logging.info(&quot;Saved %d PNG diagnostics to %s&quot;, len(paths), args.output_dir / &quot;diagnostics&quot;)</code> | Logs the number and destination of saved PNGs. |
| 21 | <code></code> | Blank separator for readability; no operation. |
| 22 | <code></code> | Blank separator for readability; no operation. |
| 23 | <code>if __name__ == &quot;__main__&quot;:</code> | Runs the following entry point only when this file is executed as a script, not when imported. |
| 24 | <code>    main()</code> | Calls the plotting entry point. |

## scripts/audit_exports.py

Independently decodes exported files and computes scalar integer sums, instead of trusting the pipeline's correlation result.

Source snapshot SHA-256: `441aa9c3d01db817c76d68baa924453480822ba0e3333bd3b3d38bc2ef58be43`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Independently decode every generated vector and verify its exact integer sums.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>import argparse</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>import csv</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>import hashlib</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 6 | <code>import json</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 7 | <code>import logging</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 8 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 9 | <code></code> | Blank separator for readability; no operation. |
| 10 | <code></code> | Blank separator for readability; no operation. |
| 11 | <code>def decode(path: Path) -&gt; list[int]:</code> | Defines independent signed-16 HEX decoding. |
| 12 | <code>    lines = path.read_text(encoding=&quot;ascii&quot;).splitlines()</code> | Reads ASCII words as lines. |
| 13 | <code>    if any(len(s) != 4 or any(c not in &quot;0123456789ABCDEF&quot; for c in s) for s in lines):</code> | Requires four uppercase hexadecimal digits per word; this audit is stricter about case than export.read_hex. |
| 14 | <code>        raise ValueError(f&quot;Invalid HEX format: {path}&quot;)</code> | Rejects malformed vector formatting. |
| 15 | <code>    return [int(s, 16) - (65536 if int(s, 16) &gt;= 32768 else 0) for s in lines]</code> | Parses base-16 words and subtracts 65536 when bit 15 is set. |
| 16 | <code></code> | Blank separator for readability; no operation. |
| 17 | <code></code> | Blank separator for readability; no operation. |
| 18 | <code>def main() -&gt; None:</code> | Defines the audit entry point. |
| 19 | <code>    parser = argparse.ArgumentParser(description=__doc__)</code> | Creates its argument parser. |
| 20 | <code>    parser.add_argument(&quot;--output-dir&quot;, type=Path, default=Path(&quot;output&quot;))</code> | Adds the output directory to inspect. |
| 21 | <code>    args = parser.parse_args()</code> | Reads arguments. |
| 22 | <code>    logging.basicConfig(level=logging.INFO, format=&quot;%(levelname)s: %(message)s&quot;)</code> | Configures status logging. |
| 23 | <code>    audits = []</code> | Starts successful per-scenario audit records. |
| 24 | <code>    try:</code> | Starts expected-error handling. |
| 25 | <code>        for directory in sorted((args.output_dir / &quot;vectors&quot;).iterdir()):</code> | Walks sorted entries under output/vectors. |
| 26 | <code>            if not directory.is_dir():</code> | Identifies non-directory entries. |
| 27 | <code>                continue</code> | Skips entries that cannot be scenario folders. |
| 28 | <code>            meta = json.loads((directory / &quot;metadata.json&quot;).read_text(encoding=&quot;utf-8&quot;))</code> | Reads the scenario's metadata contract. |
| 29 | <code>            q = decode(directory / &quot;adc_samples.hex&quot;)</code> | Independently decodes all ADC words. |
| 30 | <code>            r = decode(directory / &quot;reference_lut.hex&quot;)</code> | Independently decodes all reference words. |
| 31 | <code>            n, period = meta[&quot;window_samples&quot;], meta[&quot;reference&quot;][&quot;length&quot;]</code> | Reads measurement-window length and reference period from metadata. |
| 32 | <code>            def require(condition: bool, detail: str) -&gt; None:</code> | Defines a scenario-specific assertion helper. |
| 33 | <code>                if not condition:</code> | Checks whether the condition failed. |
| 34 | <code>                    raise ValueError(f&quot;{directory.name}: {detail}&quot;)</code> | Raises a descriptive error naming the scenario. |
| 35 | <code>            require(len(q) == meta[&quot;number_of_samples&quot;], &quot;sample count mismatch&quot;)</code> | Verifies actual input sample count matches metadata. |
| 36 | <code>            require(len(r) == period and r[0] == 0, &quot;reference count or phase mismatch&quot;)</code> | Checks actual reference length and initial zero. |
| 37 | <code>            require(all(meta[&quot;adc&quot;][&quot;code_min&quot;] &lt;= code &lt;= meta[&quot;adc&quot;][&quot;code_max&quot;] for code in q), &quot;invalid ADC range/sign extension&quot;)</code> | Checks all decoded ADC values against the declared signed numerical range. |
| 38 | <code>            with (directory / &quot;expected_results.csv&quot;).open(newline=&quot;&quot;, encoding=&quot;utf-8&quot;) as handle:</code> | Opens expected_results.csv. |
| 39 | <code>                expected = list(csv.DictReader(handle))</code> | Reads expected rows keyed by CSV column names. |
| 40 | <code>            require(len(expected) == len(q)//n == meta[&quot;number_of_windows&quot;], &quot;window count mismatch&quot;)</code> | Checks expected-result count equals complete input windows and metadata count. |
| 41 | <code>            for i, row in enumerate(expected):</code> | Iterates completed results in order. |
| 42 | <code>                start, end = i*n, (i+1)*n-1</code> | Computes the inclusive input interval belonging to each result. |
| 43 | <code>                require(int(row[&quot;window_index&quot;]) == i and int(row[&quot;start_sample&quot;]) == start</code> | Checks zero-based result index and first sample. |
| 44 | <code>                        and int(row[&quot;end_sample&quot;]) == end, &quot;window alignment mismatch&quot;)</code> | Also checks the last inclusive sample. |
| 45 | <code>                actual = sum(q[j]*r[j % period] for j in range(start, end+1))</code> | Recomputes each exact sum with Python integer multiplication/addition and global modulo indexing. |
| 46 | <code>                require(actual == int(row[&quot;expected_accumulator&quot;]), f&quot;integer accumulator mismatch in window {i}&quot;)</code> | Requires exact agreement with the exported expected_accumulator, without floating tolerance. |
| 47 | <code>            truth = args.output_dir / &quot;ground_truth&quot; / directory.name / &quot;ground_truth.csv&quot;</code> | Locates the matching ground-truth file. |
| 48 | <code>            with truth.open(newline=&quot;&quot;, encoding=&quot;utf-8&quot;) as handle:</code> | Opens the physical ground-truth CSV. |
| 49 | <code>                rows = csv.DictReader(handle)</code> | Creates a named-column CSV reader. |
| 50 | <code>                count = 0</code> | Initializes the record count. |
| 51 | <code>                for index, row in enumerate(rows):</code> | Iterates rows alongside their expected zero-based index. |
| 52 | <code>                    require(index &lt; len(q), &quot;extra ground truth row&quot;)</code> | Rejects extra truth records. |
| 53 | <code>                    require(int(row[&quot;sample_index&quot;]) == index and int(row[&quot;adc_code&quot;]) == q[index], &quot;ground truth ordering/code mismatch&quot;)</code> | Verifies physical sample indices and signed ADC values agree with the HEX input sequence. |
| 54 | <code>                    count += 1</code> | Counts this verified physical record. |
| 55 | <code>            require(count == len(q), &quot;ground truth row count mismatch&quot;)</code> | Checks final physical record count. |
| 56 | <code>            files = list(directory.iterdir()) + [truth]</code> | Collects the scenario files plus ground truth. |
| 57 | <code>            hashes = {str(path.relative_to(args.output_dir)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}</code> | Computes SHA-256 fingerprints with relative file paths. |
| 58 | <code>            audits.append({&quot;scenario&quot;: directory.name, &quot;samples&quot;: len(q), &quot;windows&quot;: len(expected), &quot;sha256&quot;: hashes})</code> | Stores scenario name, verified counts, and fingerprints. |
| 59 | <code>            logging.info(&quot;%s: %d samples and %d exact accumulators verified&quot;, directory.name, len(q), len(expected))</code> | Logs successful sample and accumulator verification. |
| 60 | <code>        if not audits:</code> | Checks that some exports were actually inspected. |
| 61 | <code>            raise ValueError(&quot;No scenario exports found&quot;)</code> | Rejects an empty scenario set. |
| 62 | <code>        report = {&quot;status&quot;: &quot;passed&quot;, &quot;scenario_count&quot;: len(audits), &quot;sample_count&quot;: sum(a[&quot;samples&quot;] for a in audits),</code> | Starts the combined report with success, scenario count, and total samples. |
| 63 | <code>                  &quot;window_count&quot;: sum(a[&quot;windows&quot;] for a in audits), &quot;scenarios&quot;: audits}</code> | Adds total windows and all per-scenario records. |
| 64 | <code>        reports = args.output_dir / &quot;reports&quot;</code> | Chooses output/reports. |
| 65 | <code>        reports.mkdir(parents=True, exist_ok=True)</code> | Creates missing report directories. |
| 66 | <code>        (reports / &quot;export_audit.json&quot;).write_text(json.dumps(report, indent=2)+&quot;\n&quot;, encoding=&quot;utf-8&quot;)</code> | Writes export_audit.json with indentation and a final newline. |
| 67 | <code>    except (OSError, ValueError, KeyError) as error:</code> | Catches missing files, malformed values, and missing metadata keys. |
| 68 | <code>        parser.exit(1, f&quot;ERROR: {error}\n&quot;)</code> | Exits with status 1 and a descriptive error. |
| 69 | <code></code> | Blank separator for readability; no operation. |
| 70 | <code></code> | Blank separator for readability; no operation. |
| 71 | <code>if __name__ == &quot;__main__&quot;:</code> | Runs the following entry point only when this file is executed as a script, not when imported. |
| 72 | <code>    main()</code> | Calls the audit entry point. |

