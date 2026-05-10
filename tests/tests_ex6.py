"""Tests for exercise 6."""
"""Tests de l'exercici 6: funció fun_total_goals."""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from exercises.ex6 import fun_total_goals  # pylint: disable=wrong-import-position


def test_fun_total_goals() -> None:
    """
    Comprova que fun_total_goals calcula correctament els gols locals,
    visitants i totals.
    """
    data = pd.DataFrame(
        {
            "FTHG": [2, 1, 0, 3],
            "FTAG": [1, 1, 2, 0],
        }
    )

    result = fun_total_goals(data)

    assert result == (6, 4, 10)