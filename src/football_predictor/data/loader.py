from pathlib import Path
from typing import Optional, Union

import pandas as pd

DATA_PATH = (
    Path(__file__).resolve().parent / "raw"
)

def load_csv(path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load real historical football results from a local CSV."""
    csv_path = DATA_PATH / path if path else DATA_PATH / "E0.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"No se encontró el dataset: {csv_path}"
        )

    # Football-Data files may have different encodings
    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="cp1252")

    return df


def load_data(path: Optional[Union[str, Path]] = None) -> pd.DataFrame:

    df = load_csv(path)

    required = {
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Faltan columnas obligatorias: {sorted(missing)}"
        )

    # Keep only completed matches with valid scores
    df = df.dropna(subset=["HomeTeam", "AwayTeam", "FTHG", "FTAG"]).copy()

    df["FTHG"] = pd.to_numeric(df["FTHG"], errors="coerce")
    df["FTAG"] = pd.to_numeric(df["FTAG"], errors="coerce")
    df = df.dropna(subset=["FTHG", "FTAG"])

    df = df[(df["FTHG"] >= 0) & (df["FTAG"] >= 0)].copy()

    df["FTR"] = "D"
    df.loc[df["FTHG"] > df["FTAG"], "FTR"] = "H"
    df.loc[df["FTHG"] < df["FTAG"], "FTR"] = "A"

    return df.reset_index(drop=True)
