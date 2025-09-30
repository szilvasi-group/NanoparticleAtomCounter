"""
benchmark against the atomistic method
"""

from pathlib import Path
import sys
from ascii_colors import ASCIIColors
import pytest


def main() -> None:
    """
    Run the test_atomcount.py script,
    which benchmarks,
    then exit with pytest’s status code.
    """
    print("This should take about 5 minutes,\n depending on how many processors you have . . .\n\n")
    tests_dir = Path(__file__).resolve().parent
    exit_code = pytest.main(["-s", str(tests_dir)])
    text = "All benchmarking succeeded!" if exit_code == 0 else "Something went wrong! See .err files for details"
    color = ASCIIColors.color_green if exit_code == 0 else ASCIIColors.color_red
    ASCIIColors.print(
        text.upper(),
        color=color,
        style=ASCIIColors.style_bold,
        background=ASCIIColors.color_black,
        end="\n\n",
        flush=True,
        file=sys.stdout,
    )
    sys.exit(exit_code)  # sys.exit(pytest.main(["-s", str(tests_dir)]))


if __name__ == "__main__":
    main()
