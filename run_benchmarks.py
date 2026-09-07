#!/usr/bin/env python3
"""Benchmark runner for the C++ unit testing framework comparison.

Expects, under --root (default: frameworks/), one directory per framework,
each containing up to two independent project subdirectories:
  <framework>/loop/            -- always present, target `test_loop`
  <framework>/parameterized/   -- only if the framework supports it,
                                   target `test_parameterized`
per benchmark_prompt.md (Prompt A / Prompt B). Each project subdirectory
contains only a CMakeLists.txt (+ test.cpp, and optionally main.cpp/
test.hpp) -- no shell scripts and no timing logic of its own. All fetching
happens through CMake's FetchContent; this script drives cmake directly
and performs all timing itself.

Each project's CMakeLists.txt must fetch dependencies into ./deps/ (via
FETCHCONTENT_BASE_DIR) and support -DFETCHCONTENT_FULLY_DISCONNECTED=ON to
rebuild without touching the network.

For each project, this measures (each repeated --runs times):
  - configure_cold: clean build/+deps/, then `cmake -S . -B build`
                    (this is what triggers FetchContent to fetch the
                    framework)
  - build_cold:     `cmake --build build --target <name>`, right after a
                     cold configure
  - configure_warm: clean build/ only (keep deps/), then `cmake -S . -B
                     build -DFETCHCONTENT_FULLY_DISCONNECTED=ON`
  - build_warm:     same as build_cold, but after a warm configure
  - execution:      run the built test binary directly

Results are appended row-by-row to a timestamped CSV under results/, and a
summary (mean/stdev per framework/variant/phase) is printed at the end.
"""
import argparse
import csv
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

VARIANTS = ("loop", "test_loop"), ("parameterized", "test_parameterized")


def discover_projects(root: Path, only=None):
    """Yields (framework_name, variant, target_name, project_dir)."""
    projects = []
    for framework_dir in sorted(root.iterdir()):
        if not framework_dir.is_dir():
            continue
        if only and framework_dir.name not in only:
            continue
        found_any = False
        for variant, target in VARIANTS:
            project_dir = framework_dir / variant
            if (project_dir / "CMakeLists.txt").exists():
                projects.append((framework_dir.name, variant, target, project_dir))
                found_any = True
        if only and not found_any:
            print(f"warning: {framework_dir} has no loop/ or parameterized/ project, skipping", file=sys.stderr)
    return projects


def clean(project_dir: Path, remove_deps: bool):
    shutil.rmtree(project_dir / "build", ignore_errors=True)
    if remove_deps:
        shutil.rmtree(project_dir / "deps", ignore_errors=True)


def timed(cmd, cwd, log_path):
    start = time.perf_counter()
    with open(log_path, "w") as log:
        result = subprocess.run(cmd, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
    return time.perf_counter() - start, result.returncode


def record(writer, csv_file, framework, variant, phase, run, elapsed, rc):
    status = "ok" if rc == 0 else "fail"
    writer.writerow([framework, variant, phase, run, f"{elapsed:.6f}", status, datetime.now().isoformat()])
    csv_file.flush()
    return status


def benchmark_project(framework, variant, target, project_dir: Path, runs: int, log_dir: Path, writer, csv_file):
    tag = f"{framework}/{variant}"
    print(f"\n=== {tag} ===")

    for i in range(1, runs + 1):
        clean(project_dir, remove_deps=True)
        log_path = log_dir / f"{framework}_{variant}_configure_cold_run{i}.log"
        elapsed, rc = timed(["cmake", "-S", ".", "-B", "build"], project_dir, log_path)
        status = record(writer, csv_file, framework, variant, "configure_cold", i, elapsed, rc)
        print(f"  configure_cold run {i}: {elapsed:.3f}s ({status})")
        if rc != 0:
            print(f"  !! configure_cold failed for {tag}, see {log_path}", file=sys.stderr)
            continue

        log_path = log_dir / f"{framework}_{variant}_build_cold_run{i}.log"
        elapsed, rc = timed(["cmake", "--build", "build", "--target", target], project_dir, log_path)
        status = record(writer, csv_file, framework, variant, "build_cold", i, elapsed, rc)
        print(f"  build_cold run {i}: {elapsed:.3f}s ({status})")
        if rc != 0:
            print(f"  !! build_cold failed for {tag}, see {log_path}", file=sys.stderr)

    if not (project_dir / "deps").exists():
        print(f"  !! {tag}: deps/ missing, skipping warm phase/execution", file=sys.stderr)
        return

    for i in range(1, runs + 1):
        clean(project_dir, remove_deps=False)
        log_path = log_dir / f"{framework}_{variant}_configure_warm_run{i}.log"
        elapsed, rc = timed(
            ["cmake", "-S", ".", "-B", "build", "-DFETCHCONTENT_FULLY_DISCONNECTED=ON"],
            project_dir, log_path,
        )
        status = record(writer, csv_file, framework, variant, "configure_warm", i, elapsed, rc)
        print(f"  configure_warm run {i}: {elapsed:.3f}s ({status})")
        if rc != 0:
            print(f"  !! configure_warm failed for {tag}, see {log_path}", file=sys.stderr)
            continue

        log_path = log_dir / f"{framework}_{variant}_build_warm_run{i}.log"
        elapsed, rc = timed(["cmake", "--build", "build", "--target", target], project_dir, log_path)
        status = record(writer, csv_file, framework, variant, "build_warm", i, elapsed, rc)
        print(f"  build_warm run {i}: {elapsed:.3f}s ({status})")
        if rc != 0:
            print(f"  !! build_warm failed for {tag}, see {log_path}", file=sys.stderr)

    binary_path = project_dir / "build" / target
    if not binary_path.exists():
        print(f"  !! expected binary missing: {binary_path}", file=sys.stderr)
        return
    for i in range(1, runs + 1):
        log_path = log_dir / f"{framework}_{variant}_exec_run{i}.log"
        elapsed, rc = timed([str(binary_path.resolve())], project_dir, log_path)
        status = record(writer, csv_file, framework, variant, "execution", i, elapsed, rc)
        print(f"  exec run {i}: {elapsed:.3f}s ({status})")
        if rc != 0:
            print(f"  !! execution failed for {tag}, see {log_path}", file=sys.stderr)


def print_summary(csv_path: Path):
    with open(csv_path) as f:
        rows = list(csv.DictReader(f))
    groups = {}
    for r in rows:
        if r["status"] != "ok":
            continue
        key = (r["framework"], r["variant"], r["phase"])
        groups.setdefault(key, []).append(float(r["seconds"]))
    print("\n=== Summary (ok runs only) ===")
    print(f"{'framework':20} {'variant':14} {'phase':16} {'n':>3} {'mean_s':>10} {'stdev_s':>10}")
    for (fw, variant, phase), values in sorted(groups.items()):
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0.0
        print(f"{fw:20} {variant:14} {phase:16} {len(values):>3} {mean:>10.4f} {stdev:>10.4f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="frameworks", help="directory containing one subdirectory per framework")
    parser.add_argument("--runs", type=int, default=5, help="number of repetitions per phase")
    parser.add_argument("--only", nargs="*", help="only benchmark these framework directory names")
    parser.add_argument("--out", default=None, help="output CSV path (default: results/results_<timestamp>.csv)")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        sys.exit(f"error: {root} is not a directory")

    projects = discover_projects(root, only=set(args.only) if args.only else None)
    if not projects:
        sys.exit(f"error: no loop/ or parameterized/ projects with CMakeLists.txt found under {root}")

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    log_dir = results_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    out_path = Path(args.out) if args.out else results_dir / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["framework", "variant", "phase", "run", "seconds", "status", "timestamp"])
        for framework, variant, target, project_dir in projects:
            benchmark_project(framework, variant, target, project_dir, args.runs, log_dir, writer, f)

    print(f"\nResults written to {out_path}")
    print_summary(out_path)


if __name__ == "__main__":
    main()
