import os
import joblib
import pandas as pd

# === 1. Load the saved model ===
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'contentModel.sav'))
tfidf_matrix, tfidf, cosine_sim = joblib.load(model_path)

# === 2. Load the article metadata ===
df_movies = pd.read_csv('path/to/shared_articles.csv')  # <-- update path
df_movies = df_movies[df_movies['eventType'] == 'CONTENT SHARED'].reset_index(drop=True)

# === 3. Recommendation function ===
def get_recommendations(content_index, sim_matrix, n=10, messages=True):
    sim_scores = list(enumerate(sim_matrix[content_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar = sim_scores[1:n+1]
    rec_dict = {i[0]: i[1] for i in top_similar}

    if messages:
        print(f"The top recommended indices are: {list(rec_dict.keys())}")
        print(f"Their similarity scores are:     {list(rec_dict.values())}")

    return rec_dict

# === 4. Prompt user to enter a contentId ===
try:
    user_input = input("Enter a contentId: ").strip()
    user_content_id = int(user_input)

    # Find the index of the contentId in df_movies
    if user_content_id in df_movies['contentId'].values:
        idx = df_movies[df_movies['contentId'] == user_content_id].index[0]
        recs = get_recommendations(idx, cosine_sim, n=5)

        print(f"\nIf you liked: {df_movies.at[idx, 'title']}\nYou may also like:\n")
        for rec_idx, score in recs.items():
            print(f"• {df_movies.at[rec_idx, 'title']} (score: {score:.3f})")
    else:
        print(f"\ncontentId {user_content_id} not found.")
        print("Here are a few contentIds you can try:")
        print(df_movies['contentId'].sample(5).to_list())

except ValueError:
    print("Please enter a valid numeric contentId.")


