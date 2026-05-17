"""
Configuració central del projecte.

Construeixo els camins a partir de la ubicació d’aquest fitxer dins de `src/`,
així el CSV i les carpetes `img` i `model` es troben sempre sense dependre
del directori de treball actual (encara que habitualment executo des de l’arrel
del repositori).
"""

from datetime import datetime
from pathlib import Path

# Directori `src/` on viu aquest mòdul
_SRC = Path(__file__).resolve().parent

nom_alumne = "Arnau_Guerra_González"
date_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Rutes relatives a `src/` (es converteixen a cadena on cal per pandas/plt/pickle)
DATA_PATH = str(_SRC / "data" / "LaLiga_Matches.csv")
IMG_PATH = str(_SRC / "img")
MODEL_PATH = str(_SRC / "model")
