# Anime Recommendation System — AnimeVerse

A dark neon anime dashboard inspired by the uploaded visual reference. Includes dashboard metrics, charts, anime library, filters and a content-based recommendation engine.

## Run on macOS
```bash
cd anime_recommendation_system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown in Terminal (normally http://localhost:8501).

## Files
- `app.py` — Streamlit dashboard and GUI
- `recommender.py` — TF-IDF + cosine similarity recommendation logic
- `data/anime.csv` — starter anime dataset
- `requirements.txt` — dependencies

The included dataset is for demonstration and can be replaced with a larger CSV containing: `title, genres, synopsis, rating, members, episodes`.
