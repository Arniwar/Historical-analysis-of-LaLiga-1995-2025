"""
Tests de l’exercici 6: comprovo ``fun_total_goals`` amb un DataFrame petit.

Afegeixo ``src`` a ``sys.path`` perquè pugui importar ``exercises`` igual que
quan executo el projecte des de l’arrel; el test el faig amb dades inventades
per verificar la suma manualment.
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from exercises.ex6 import fun_total_goals  # pylint: disable=wrong-import-position


def test_fun_total_goals() -> None:
    """
    Donat un petit dataframe, els totals han de coincidir amb la suma de FTHG i FTAG.

    Espero (6, 4, 10) perquè sumo locals 2+1+0+3=6 i visitants 1+1+2+0=4.
    """
    data = pd.DataFrame(
        {
            "FTHG": [2, 1, 0, 3],
            "FTAG": [1, 1, 2, 0],
        }
    )

    result = fun_total_goals(data)

    assert result == (6, 4, 10)
