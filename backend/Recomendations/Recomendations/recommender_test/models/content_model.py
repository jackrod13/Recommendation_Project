
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load articles
df = pd.read_csv("../data/shared_articles.csv")
df = df[df["eventType"] == "CONTENT SHARED"]

# Fill missing text
df["full_text"] = (df["title"].fillna("") + " " + df["text"].fillna("")).fillna("")

# Vectorize
tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
tfidf_matrix = tfidf.fit_transform(df["full_text"])

# Compute similarity
cosine_sim = cosine_similarity(tfidf_matrix)

# Save
model_path = "content_model.sav"
joblib.dump((tfidf_matrix, tfidf, cosine_sim), model_path)

print(f"✅ Content model saved to {model_path}")
