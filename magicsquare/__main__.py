"""Official entry: ``python -m magicsquare`` (requires ``pip install -e ".[gui]"``)."""

from __future__ import annotations

import sys


def main() -> None:
    try:
        if len(sys.argv) > 1 and sys.argv[1] in ("--tests", "tests"):
            from magicsquare.screen.test_runner import run_test_runner_app

            run_test_runner_app()
            return
        if len(sys.argv) > 1 and sys.argv[1] in ("--coverage", "coverage"):
            from magicsquare.screen.coverage_gui import run_coverage_gui_app

            run_coverage_gui_app()
            return
        from magicsquare.screen.app import run_app
    except ImportError as exc:
        print('PyQt6가 필요합니다. 설치: pip install -e ".[gui]"', file=sys.stderr)
        raise SystemExit(1) from exc
    run_app()


if __name__ == "__main__":
    main()
