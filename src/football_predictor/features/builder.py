import pandas as pd


def build_features(df, min_games=1):
    """
    Build leakage-free pre-match features.

    Required columns:
        HomeTeam, AwayTeam, FTHG, FTAG, FTR, Date

    Returns:
        features: DataFrame with pre-match team statistics
        team_stats: Final cumulative statistics per team
    """
    required = {
        "HomeTeam", "AwayTeam","FTHG", "FTAG", "FTR", "Date"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    data = df.copy()
    data["Date"] = pd.to_datetime(
        data["Date"], dayfirst=True, errors="raise"
    )
    data = data.sort_values("Date", kind="stable").reset_index(drop=True)

    stats = {}
    rows = []

    def get_stats(team):
        s = stats.get(team, {
            "games": 0,
            "goals_for": 0,
            "goals_against": 0,
        })
        games = s["games"]

        return {
            "games": games,
            "attack": s["goals_for"] / games if games else 0.0,
            "defense": s["goals_against"] / games if games else 0.0,
        }

    for _, match in data.iterrows():
        home = match["HomeTeam"]
        away = match["AwayTeam"]

        # Features use only matches played before this match.
        hs = get_stats(home)
        aws = get_stats(away)

        rows.append({
            "Date": match["Date"],
            "HomeTeam": home,
            "AwayTeam": away,
            "home_games": hs["games"],
            "away_games": aws["games"],
            "home_attack": hs["attack"],
            "home_defense": hs["defense"],
            "away_attack": aws["attack"],
            "away_defense": aws["defense"],
            "result": match["FTR"],
        })

        # Update cumulative statistics only after creating features.
        hg = int(match["FTHG"])
        ag = int(match["FTAG"])

        for team, gf, ga in (
            (home, hg, ag),
            (away, ag, hg),
        ):
            if team not in stats:
                stats[team] = {
                    "games": 0,
                    "goals_for": 0,
                    "goals_against": 0,
                }

            stats[team]["games"] += 1
            stats[team]["goals_for"] += gf
            stats[team]["goals_against"] += ga

    features = pd.DataFrame(rows)

    team_stats = {
        team: {
            **values,
            "attack": (
                values["goals_for"] / values["games"]
                if values["games"] else 0.0
            ),
            "defense": (
                values["goals_against"] / values["games"]
                if values["games"] else 0.0
            ),
        }
        for team, values in stats.items()
    }

    if min_games > 0:
        features = features[
            (features["home_games"] >= min_games)
            & (features["away_games"] >= min_games)
        ].reset_index(drop=True)

    return features, team_stats