import pandas as pd

def load_data():
    data = {
        "HomeTeam": ["Arsenal","Liverpool","Man United","Chelsea","Arsenal","Liverpool",
                     "Chelsea","Man City","Tottenham","Arsenal","Man City","Chelsea"],
        "AwayTeam": ["Chelsea","Man City","Tottenham","Liverpool","Man United","Chelsea",
                     "Arsenal","Liverpool","Man United","Tottenham","Arsenal","Man City"],
        "FTHG": [2,1,0,3,1,2,1,2,3,2,4,1],
        "FTAG": [1,1,2,0,1,1,2,2,1,0,2,3],
    }

    df = pd.DataFrame(data)

    def get_result(row):
        if row["FTHG"] > row["FTAG"]:
            return "H"
        elif row["FTHG"] < row["FTAG"]:
            return "A"
        return "D"

    df["FTR"] = df.apply(get_result, axis=1)
    return df
