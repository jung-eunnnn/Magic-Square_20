"""PyQt window: run pytest in the project root and stream output."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import QProcess, QProcessEnvironment, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


def _repo_root() -> Path:
    # magicsquare/screen/test_runner.py -> parents[2] == repository root
    return Path(__file__).resolve().parents[2]


def run_test_runner_app() -> None:
    app = QApplication(sys.argv)
    win = TestRunnerWindow()
    win.show()
    sys.exit(app.exec())


class TestRunnerWindow(QWidget):
    """Runs ``python -m pytest tests -v`` from repo root; shows stdout/stderr."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("pytest — Magic Square")
        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setMinimumSize(720, 480)
        self._status = QLabel("준비됨 — 「테스트 실행」을 누르세요.")
        self._status.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        run_btn = QPushButton("테스트 실행")
        run_btn.clicked.connect(self._start_pytest)
        clear_btn = QPushButton("출력 지우기")
        clear_btn.clicked.connect(self._output.clear)

        row = QHBoxLayout()
        row.addWidget(run_btn)
        row.addWidget(clear_btn)
        row.addStretch(1)

        root = QVBoxLayout(self)
        root.addLayout(row)
        root.addWidget(self._status)
        root.addWidget(self._output)

        self._proc: QProcess | None = None

    def _append(self, text: str) -> None:
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)
        self._output.insertPlainText(text)

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
