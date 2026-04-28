"""Official entry: ``python -m magicsquare`` (requires ``pip install -e ".[gui]"``)."""

from __future__ import annotations

import sys


def main() -> None:
    try:
        from magicsquare.screen.app import run_app
    except ImportError as exc:
        print('PyQt6가 필요합니다. 설치: pip install -e ".[gui]"', file=sys.stderr)
        raise SystemExit(1) from exc
    run_app()


if __name__ == "__main__":
    main()
