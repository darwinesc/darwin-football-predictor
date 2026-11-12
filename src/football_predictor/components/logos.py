import pandas as pd

def merge_team_logos(df: pd.DataFrame, df_badges: pd.DataFrame) -> pd.DataFrame:

    # Remove duplicates rows
    df_badges = df_badges.drop_duplicates(subset=['nombre'], keep='first')

    home_badges = df_badges.rename(columns={
        "nombre": "HomeTeam",
        "escudo_url": "HomeLogo"
    })

    away_badges = df_badges.rename(columns={
        "nombre": "AwayTeam",
        "escudo_url": "AwayLogo"
    })

    # Check unique rows and create a logos of Home Teams
    if df_badges['nombre'].is_unique:
        df = df.merge(home_badges[["HomeTeam","HomeLogo"]], on="HomeTeam", how="left", validate="many_to_one")

    df = df.merge(away_badges[["AwayTeam", "AwayLogo"]], on="AwayTeam", how="left", validate="many_to_one")
    

    return df