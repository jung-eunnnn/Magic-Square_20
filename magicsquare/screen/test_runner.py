"""Unified PyQt runner: tests + coverage tabs."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import QProcess, QProcessEnvironment, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

_OPEN_UNIFIED_WINDOWS: list["UnifiedRunnerWindow"] = []


def _repo_root() -> Path:
    # magicsquare/screen/test_runner.py -> parents[2] == repository root
    return Path(__file__).resolve().parents[2]


def run_test_runner_app() -> None:
    run_unified_runner_app("tests")


def run_unified_runner_app(initial_tab: str = "tests") -> None:
    app = QApplication.instance()
    created_app = app is None
    if app is None:
        app = QApplication(sys.argv)

    win = UnifiedRunnerWindow(initial_tab=initial_tab)
    win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
    _OPEN_UNIFIED_WINDOWS.append(win)
    win.destroyed.connect(
        lambda *_args, ref=win: _OPEN_UNIFIED_WINDOWS.remove(ref)
        if ref in _OPEN_UNIFIED_WINDOWS
        else None
    )
    win.show()
    win.raise_()
    win.activateWindow()

    if created_app:
        sys.exit(app.exec())


class UnifiedRunnerWindow(QWidget):
    """Single window that provides test and coverage tabs."""

    def __init__(self, initial_tab: str = "tests") -> None:
        super().__init__()
        self.setWindowTitle("pytest / coverage — Magic Square")
        self.resize(980, 640)

        self._tabs = QTabWidget(self)
        self._tests_tab = TestRunnerWindow(open_coverage=self.show_coverage_tab)

        # Local import to avoid circular import at module load.
        from magicsquare.screen.coverage_gui import CoverageWindow

        self._coverage_tab = CoverageWindow(open_tests=self.show_tests_tab)

        self._tabs.addTab(self._tests_tab, "테스트 실행")
        self._tabs.addTab(self._coverage_tab, "커버리지")

        root = QVBoxLayout(self)
        root.addWidget(self._tabs)

        if initial_tab in {"coverage", "--coverage"}:
            self.show_coverage_tab()
        else:
            self.show_tests_tab()

    def show_tests_tab(self) -> None:
        self._tabs.setCurrentWidget(self._tests_tab)

    def show_coverage_tab(self) -> None:
        self._tabs.setCurrentWidget(self._coverage_tab)


class TestRunnerWindow(QWidget):
    """Runs ``python -m pytest tests -v`` from repo root; shows stdout/stderr."""

    def __init__(self, open_coverage: Callable[[], None] | None = None) -> None:
        super().__init__()
        self._open_coverage_callback = open_coverage
        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setMinimumSize(720, 480)
        self._status = QLabel("준비됨 — 「테스트 실행」을 누르세요.")
        self._status.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        run_btn = QPushButton("테스트 실행")
        run_btn.clicked.connect(self._start_pytest)
        cov_btn = QPushButton("커버리지")
        cov_btn.clicked.connect(self._open_coverage_window)
        clear_btn = QPushButton("출력 지우기")
        clear_btn.clicked.connect(self._output.clear)

        row = QHBoxLayout()
        row.addWidget(run_btn)
        row.addWidget(cov_btn)
        row.addWidget(clear_btn)
        row.addStretch(1)

        root = QVBoxLayout(self)
        root.addLayout(row)
        root.addWidget(self._status)
        root.addWidget(self._output)

        self._proc: QProcess | None = None
        # Keep child windows alive while opened.
        self._coverage_windows: list[QWidget] = []

    def _append(self, text: str) -> None:
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)
        self._output.insertPlainText(text)

    def _open_coverage_window(self) -> None:
        if self._open_coverage_callback is not None:
            self._open_coverage_callback()
            return

        from magicsquare.screen.coverage_gui import CoverageWindow

        win = CoverageWindow()
        win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self._coverage_windows.append(win)
        win.destroyed.connect(
            lambda *_args, ref=win: setattr(
                self, "_coverage_windows", [w for w in self._coverage_windows if w is not ref]
            )
        )
        win.show()
        win.raise_()
        win.activateWindow()

    def _start_pytest(self) -> None:
        if self._proc is not None and self._proc.state() != QProcess.ProcessState.NotRunning:
            QMessageBox.information(self, "실행 중", "이미 테스트가 실행 중입니다.")
            return

        self._append("\n" + "=" * 72 + "\n")
        self._status.setText("실행 중…")

        proc = QProcess(self)
        self._proc = proc
        proc.setProgram(sys.executable)
        proc.setArguments(["-m", "pytest", "tests", "-v", "--color=no"])
        proc.setWorkingDirectory(str(_repo_root()))

        env = QProcessEnvironment.systemEnvironment()
        proc.setProcessEnvironment(env)

        proc.readyReadStandardOutput.connect(self._read_stdout)
        proc.readyReadStandardError.connect(self._read_stderr)
        proc.finished.connect(self._on_finished)

        proc.start()

    def _read_stdout(self) -> None:
        if self._proc:
            self._append(bytes(self._proc.readAllStandardOutput()).decode(errors="replace"))

    def _read_stderr(self) -> None:
        if self._proc:
            self._append(bytes(self._proc.readAllStandardError()).decode(errors="replace"))

    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        normal = exit_status == QProcess.ExitStatus.NormalExit
        status_ok = normal and exit_code == 0
        self._status.setText(
            f"종료: exitCode={exit_code}, exitStatus={exit_status!s} — "
            f"{'PASS' if status_ok else 'FAIL 또는 오류'}"
        )
        self._proc = None


if __name__ == "__main__":
    run_test_runner_app()
