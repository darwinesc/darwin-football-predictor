import pandas as pd

def build_features(df):

    team_stats = {}
    teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()

    for team in teams:
        home = df[df["HomeTeam"] == team]
        away = df[df["AwayTeam"] == team]

        goals_for = home["FTHG"].sum() + away["FTAG"].sum()
        goals_against = home["FTAG"].sum() + away["FTHG"].sum()
        games = len(home) + len(away)

        team_stats[team] = {
            "attack": goals_for / games,
            "defense": goals_against / games
        }

    rows = []

    for _, row in df.iterrows():
        rows.append({
            "home_attack": team_stats[row["HomeTeam"]]["attack"],
            "home_defense": team_stats[row["HomeTeam"]]["defense"],
            "away_attack": team_stats[row["AwayTeam"]]["attack"],
            "away_defense": team_stats[row["AwayTeam"]]["defense"],
            "result": row["FTR"]
        })

    return pd.DataFrame(rows), team_stats
