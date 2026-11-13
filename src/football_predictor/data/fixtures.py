import pandas as pd

FIXTURES_URL = (
    "https://raw.githubusercontent.com/"
    "oladeeayo/open-matchday/master/data/"
    "ENG_1_premier-league/fixtures_2627.csv"
)

def load_fixtures():

    df = pd.read_csv(FIXTURES_URL)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    return df