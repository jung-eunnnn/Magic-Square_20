"""PyQt6 main window: grid input, validate → solution, result or error dialog."""

from __future__ import annotations

import sys
from typing import Final

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.magic_square import solution, validate
from constants import MATRIX_SIZE

# Demo partial grid (two blanks); matches Level 4 Gherkin-style fixture.
_DEFAULT_GRID: Final[list[list[int]]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]


def run_app() -> None:
    app = QApplication(sys.argv)
    win = MagicSquareWindow()
    win.show()
    sys.exit(app.exec())


class MagicSquareWindow(QWidget):
    """4×4 spin boxes (0 = blank), Solve runs ``validate`` then ``solution``."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Magic Square 4×4")
        self._cells: list[list[QSpinBox]] = []
        grid = QGridLayout()
        for r in range(MATRIX_SIZE):
            row_widgets: list[QSpinBox] = []
            for c in range(MATRIX_SIZE):
                spin = QSpinBox()
                spin.setRange(0, 16)
                spin.setValue(_DEFAULT_GRID[r][c])
                spin.setMinimumWidth(48)
                grid.addWidget(spin, r, c)
                row_widgets.append(spin)
            self._cells.append(row_widgets)

        self._result_label = QLabel("결과: —")
        self._result_label.setWordWrap(True)

        solve_btn = QPushButton("풀기")
        solve_btn.clicked.connect(self._on_solve)

        actions = QHBoxLayout()
        actions.addWidget(solve_btn)
        actions.addStretch(1)

        root = QVBoxLayout(self)
        root.addLayout(grid)
        root.addLayout(actions)
        root.addWidget(self._result_label)

    def _read_grid(self) -> list[list[int]]:
        return [[self._cells[r][c].value() for c in range(MATRIX_SIZE)] for r in range(MATRIX_SIZE)]

    def _on_solve(self) -> None:
        grid = self._read_grid()
        try:
            validated = validate(grid)
            out = solution(validated)
        except (TypeError, ValueError) as e:
            QMessageBox.warning(self, "입력 오류", str(e) or type(e).__name__)
            self._result_label.setText("결과: —")
            return
        r1, c1, n1, r2, c2, n2 = out
        self._result_label.setText(
            f"결과: ({r1},{c1})={n1}, ({r2},{c2})={n2}  —  [{r1}, {c1}, {n1}, {r2}, {c2}, {n2}]"
        )


if __name__ == "__main__":
    run_app()
