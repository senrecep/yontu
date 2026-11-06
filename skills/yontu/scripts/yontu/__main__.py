"""Entry point for `python3 -m yontu` and `python3 <skill>/scripts/yontu`."""
import os
import sys

if not __package__:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from yontu.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
