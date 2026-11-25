from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_anime(title, df, top_n=5):
    data = df.copy()
    data["features"] = data["genres"].fillna("").str.replace(",", " ", regex=False) + " " + data["synopsis"].fillna("")
    matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(data["features"])
    matches = data.index[data["title"].str.casefold() == title.casefold()].tolist()
    if not matches:
        return data.iloc[0:0].assign(similarity=[])
    idx = matches[0]
    scores = cosine_similarity(matrix[idx], matrix).flatten()
    order = [i for i in scores.argsort()[::-1] if i != idx][:top_n]
    result = data.iloc[order][["title","genres","synopsis","rating","members","episodes"]].copy()
    result["similarity"] = [round(float(scores[i])*100,1) for i in order]
    return result
