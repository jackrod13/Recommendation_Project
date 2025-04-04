import os
import sys
import joblib
import pandas as pd

# === 1. Load the saved model ===
model_path = os.path.join(os.path.dirname(__file__), 'contentModel.sav')
tfidf_matrix, tfidf, cosine_sim = joblib.load(model_path)

# === 2. Load the article metadata (with updated filename) ===
csv_path = os.path.join(os.path.dirname(__file__), 'shared_articles (2).csv')
df_articles = pd.read_csv(csv_path)
df_articles = df_articles[df_articles['eventType'] == 'CONTENT SHARED'].reset_index(drop=True)

# === 3. Recommendation function ===
def get_recommendations(content_index, sim_matrix, n=5):
    sim_scores = list(enumerate(sim_matrix[content_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_similar = sim_scores[1:n+1]
    rec_indices = [i[0] for i in top_similar]
    return rec_indices

# === 4. Accept contentId from command line ===
try:
    user_content_id = int(sys.argv[1])

    if user_content_id in df_articles['contentId'].values:
        idx = df_articles[df_articles['contentId'] == user_content_id].index[0]
        rec_indices = get_recommendations(idx, cosine_sim)
        rec_content_ids = [int(df_articles.at[i, 'contentId']) for i in rec_indices]
        print(','.join(map(str, rec_content_ids)))
    else:
        print("")

except Exception as e:
    print("")
