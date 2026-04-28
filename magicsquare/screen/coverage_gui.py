"""PyQt window: run pytest with coverage and show results in a table (no HTML)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import importlib.util
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import QProcess, QProcessEnvironment, Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

 
def _repo_root() -> Path:
    # magicsquare/screen/coverage_gui.py -> parents[2] == repository root
    return Path(__file__).resolve().parents[2]


def run_coverage_gui_app() -> None:
    from magicsquare.screen.test_runner import run_unified_runner_app

    run_unified_runner_app(initial_tab="coverage")


class CoverageWindow(QWidget):
    """Runs pytest with JSON coverage report; fills a sortable table."""

    def __init__(self, open_tests: Callable[[], None] | None = None) -> None:
        super().__init__()
        self._open_tests_callback = open_tests

        self._status = QLabel("「커버리지 실행」을 누르면 테스트 후 표가 채워집니다.")
        self._status.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._totals_label = QLabel("")
        self._totals_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self._table = QTableWidget(0, 5)
        self._table.setHorizontalHeaderLabels(["파일", "구문", "실행", "누락", "커버 %"])
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for c in range(1, 5):
            self._table.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeMode.ResizeToContents)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.itemSelectionChanged.connect(self._on_row_selected)

        self._detail = QTextEdit()
        self._detail.setReadOnly(True)
        self._detail.setPlaceholderText("표에서 행을 선택하면 미커버 줄 번호가 여기 표시됩니다.")

        run_btn = QPushButton("커버리지 실행")
        run_btn.clicked.connect(self._start_coverage)
        test_btn = QPushButton("테스트 실행")
        test_btn.clicked.connect(self._open_test_runner)
        clear_btn = QPushButton("출력 지우기")
        clear_btn.clicked.connect(self._clear_output)

        row = QHBoxLayout()
        row.addWidget(run_btn)
        row.addWidget(test_btn)
        row.addWidget(clear_btn)
        row.addStretch(1)

        split = QSplitter(Qt.Orientation.Vertical)
        split.addWidget(self._table)
        split.addWidget(self._detail)
        split.setSizes([320, 200])

        root = QVBoxLayout(self)
        root.addLayout(row)
        root.addWidget(self._status)
        root.addWidget(self._totals_label)
        root.addWidget(split)

        self._proc: QProcess | None = None
        self._json_path: Path | None = None
        self._files_data: dict[str, dict] = {}
        self._log = ""
        self._test_windows: list[QWidget] = []

    def _clear_output(self) -> None:
        self._log = ""
        self._detail.clear()

    def _append_log(self, text: str) -> None:
        self._log += text
        self._detail.setPlainText(self._log)

    def _open_test_runner(self) -> None:
        if self._open_tests_callback is not None:
            self._open_tests_callback()
            return

        from magicsquare.screen.test_runner import TestRunnerWindow

        win = TestRunnerWindow()
        win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self._test_windows.append(win)
        win.destroyed.connect(
            lambda *_args, ref=win: setattr(
                self, "_test_windows", [w for w in self._test_windows if w is not ref]
            )
        )
        win.show()
        win.raise_()
        win.activateWindow()

    def _start_coverage(self) -> None:
        if self._proc is not None and self._proc.state() != QProcess.ProcessState.NotRunning:
            QMessageBox.information(self, "실행 중", "이미 작업이 실행 중입니다.")
            return
        if importlib.util.find_spec("pytest_cov") is None:
            msg = (
                "현재 Python 환경에 pytest-cov가 없어 커버리지 옵션을 사용할 수 없습니다.\n"
                "터미널에서 다음을 실행 후 다시 시도하세요:\n"
                '  pip install -e ".[gui]"'
            )
            self._status.setText("실패: pytest-cov 미설치")
            self._append_log("[오류] pytest-cov 미설치 — --cov 옵션 사용 불가\n")
            QMessageBox.warning(self, "pytest-cov 필요", msg)
            return

        fd, raw = tempfile.mkstemp(suffix=".json", prefix="ms_cov_")
        os.close(fd)
        self._json_path = Path(raw)

        self._log = ""
        self._files_data.clear()
        self._table.setRowCount(0)
        self._totals_label.clear()
        self._append_log(f"JSON 출력: {self._json_path}\n" + "=" * 72 + "\n")
        self._status.setText("pytest + coverage 실행 중…")

        proc = QProcess(self)
        self._proc = proc
        proc.setProgram(sys.executable)
        json_arg = f"--cov-report=json:{self._json_path}"
        proc.setArguments(
            [
                "-m",
                "pytest",
                "tests",
                "-q",
                "--color=no",
                "--cov=entity",
                "--cov=boundary",
                "--cov=magicsquare",
                json_arg,
            ]
        )
        proc.setWorkingDirectory(str(_repo_root()))
        proc.setProcessEnvironment(QProcessEnvironment.systemEnvironment())
        proc.readyReadStandardOutput.connect(self._read_stdout)
        proc.readyReadStandardError.connect(self._read_stderr)
        proc.finished.connect(self._on_finished)
        proc.start()

    def _read_stdout(self) -> None:
        if self._proc:
            self._append_log(bytes(self._proc.readAllStandardOutput()).decode(errors="replace"))

    def _read_stderr(self) -> None:
        if self._proc:
            self._append_log(bytes(self._proc.readAllStandardError()).decode(errors="replace"))

    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        normal = exit_status == QProcess.ExitStatus.NormalExit
        path = self._json_path
        self._proc = None

        if path and path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                self._load_table(data)
            except (OSError, json.JSONDecodeError) as e:
                self._append_log(f"\n[오류] JSON 읽기 실패: {e}\n")
            finally:
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
        self._json_path = None

        status_ok = normal and exit_code == 0
        self._status.setText(
            f"종료: exitCode={exit_code}, exitStatus={exit_status!s} — "
            f"{'완료' if status_ok else '실패 또는 오류'} (표는 coverage JSON이 있으면 갱신됨)"
        )

    def _load_table(self, data: dict) -> None:
        files: dict[str, dict] = data.get("files") or {}
        totals = data.get("totals") or {}

        rows: list[tuple[str, dict]] = []
        for rel, finfo in sorted(files.items()):
            disp = rel.replace("\\", "/")
            rows.append((disp, finfo))

        self._files_data = {disp: finfo for disp, finfo in rows}
        self._table.setSortingEnabled(False)
        self._table.setRowCount(len(rows))

        for i, (disp, finfo) in enumerate(rows):
            summ = finfo.get("summary") or {}
            self._set_row(
                i,
                disp,
                int(summ.get("num_statements", 0)),
                int(summ.get("covered_lines", 0)),
                int(summ.get("missing_lines", 0)),
                float(summ.get("percent_covered", 0.0)),
            )

        if totals:
            n_st = int(totals.get("num_statements", 0))
            n_cov = int(totals.get("covered_lines", 0))
            n_miss = int(totals.get("missing_lines", max(0, n_st - n_cov)))
            pct = float(totals.get("percent_covered", 0.0))
            self._totals_label.setText(
                f"합계: 구문 {n_st} · 실행 {n_cov} · 누락 {n_miss} · 커버 {pct:.1f}%"
            )
        else:
            self._totals_label.clear()

        self._table.setSortingEnabled(True)
        self._table.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def _set_row(
        self,
        row: int,
        name: str,
        stmts: int,
        covered: int,
        missing: int,
        pct: float,
    ) -> None:
        def item(text: str, numeric: float | None = None) -> QTableWidgetItem:
            it = QTableWidgetItem(text)
            it.setFlags(it.flags() ^ Qt.ItemFlag.ItemIsEditable)
            if numeric is not None:
                it.setData(Qt.ItemDataRole.EditRole, numeric)
            return it

        self._table.setItem(row, 0, item(name))
        self._table.setItem(row, 1, item(str(stmts), float(stmts)))
        self._table.setItem(row, 2, item(str(covered), float(covered)))
        self._table.setItem(row, 3, item(str(missing), float(missing)))
        self._table.setItem(row, 4, item(f"{pct:.1f}", pct))

    def _on_row_selected(self) -> None:
        items = self._table.selectedItems()
        if not items:
            return
        row = items[0].row()
        name_item = self._table.item(row, 0)
        if name_item is None:
            return
        name = name_item.text()
        finfo = self._files_data.get(name)
        if not finfo:
            return
        missing = finfo.get("missing_lines") or []
        extra = f"\n\n--- 선택: {name} ---\n미커버 줄: {', '.join(str(x) for x in missing) if missing else '(없음)'}\n"
        self._detail.setPlainText(self._log + extra)
