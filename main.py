#!/usr/bin/env python3

"""
Tokenizer Benchmark

Entry point for the tokenizer benchmark application.
"""

import argparse
from benchmark.runner import BenchmarkRunner


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Benchmark multilingual tokenizer efficiency."
    )

    parser.add_argument(
        "--config",
        default="configs/benchmark.json",
        help="Path to benchmark configuration file.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    runner = BenchmarkRunner(config_path=args.config)
    runner.run()


if __name__ == "__main__":
    main()
