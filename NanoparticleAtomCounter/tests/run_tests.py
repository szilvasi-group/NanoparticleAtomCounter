"""
Automatically test all functions;
also benchmark against a traditional atomistic method
"""
from pathlib import Path
import sys
from ascii_colors import ASCIIColors
import pytest

FILE = sys.stdout
FLUSH = True
BACKGROUND = ASCIIColors.color_black
STYLE = ASCIIColors.style_bold
END = "\n\n"

def main() -> None:
    """
    Run every test in the project,
    then exit with pytest’s status code.
    """
    print("We might be here for about 5 minutes . . .\n\n")
    tests_dir = Path(__file__).resolve().parent
    exit_code = pytest.main(["-s", str(tests_dir)])
    text = "All tests passed!" if exit_code == 0 else "Some tests failed!"
    color = ASCIIColors.color_green if  exit_code == 0 else ASCIIColors.color_red
    ASCIIColors.print(
            text,
            color=color,
            style=STYLE,
            background=BACKGROUND,
            end=END,
            flush=FLUSH,
            file=FILE
            )
    sys.exit(exit_code) #sys.exit(pytest.main(["-s", str(tests_dir)]))

if __name__ == "__main__":
    main()

