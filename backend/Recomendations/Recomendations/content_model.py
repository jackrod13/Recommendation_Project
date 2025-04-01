import os
import joblib
import pandas as pd

# === 1. Load the saved model ===
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'contentModel.sav'))
tfidf_matrix, tfidf, cosine_sim = joblib.load(model_path)

# === 2. Load your article metadata ===
df_movies = pd.read_csv('path/to/shared_articles.csv')  # ← Update this path
df_movies = df_movies[df_movies['eventType'] == 'CONTENT SHARED'].reset_index(drop=True)

# === 3. Recommendation function ===
def get_recommendations(contentId, sim_matrix, n=10, messages=True):
    sim_scores = list(enumerate(sim_matrix[contentId]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar = sim_scores[1:n+1]
    rec_dict = {i[0]: i[1] for i in top_similar}

    if messages:
        print(f"The top recommended content IDs are: {list(rec_dict.keys())}")
        print(f"Their similarity scores are:     {list(rec_dict.values())}")

    return rec_dict

# === 4. Ask user for input ===
user_title = input("Enter an article title: ").strip()

# === 5. Find and recommend ===
if user_title in df_movies['title'].values:
    idx = df_movies[df_movies['title'] == user_title].index[0]
    recs = get_recommendations(idx, cosine_sim, n=5)

    print(f"\nIf you liked: {user_title}\nYou may also like:\n")
    for rec_idx, score in recs.items():
        print(f"• {df_movies.at[rec_idx, 'title']} (score: {score:.3f})")
else:
    print(f"\nTitle not found: \"{user_title}\"")
    print("Here are a few titles you can try:")
    for t in df_movies['title'].sample(5):
        print("•", t)

