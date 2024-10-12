import argparse
from pathlib import Path

from kotoha.core import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=Path, nargs="+")
    args = parser.parse_args()

    for src in args.src:
        run(src.read_text())


if __name__ == "__main__":
    main()
