#Football-predictor structure

football-predictor/
│
├── app/
│   └── streamlit_app.py
│
├── src/
|   └── football_predictor/
|        ├── data/
|        |   ├── __init__.py
|        |   └── loader.py
|        ├── features/
|        |   ├── __init__.py
|        |   └── builder.py
|        └── model
|            ├── __init__.py
|            └── builder.py
│
├── pyproject.toml
├── uv.lock
└── README.md


# Run
uv run streamlit run app/streamlit_app.py