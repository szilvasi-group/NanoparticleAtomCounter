"""
Automatically test all functions;
also benchmark against a traditional atomistic method
"""
from pathlib import Path
import sys
import pytest

def main() -> None:
    """
    Run every test in the project, then exit with pytest’s status code.
    """
    tests_dir = Path(__file__).parent
#    print(tests_dir)
    sys.exit(pytest.main(["-s", str(tests_dir)]))

if __name__ == "__main__":
    main()

