import sys
import os
import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np
from scipy.sparse import csr_matrix

# === [1] Load the model using full path ===
model_path = os.path.join(os.path.dirname(__file__), "collaborative_model.sav")

try:
    with open(model_path, "rb") as f:
        X, user_mapper, item_inv_mapper = pickle.load(f)

    # ✅ DEBUG: Print sample user IDs from model
    print("[DEBUG] Sample user IDs in model:", list(user_mapper.keys())[:10], file=sys.stderr)

except FileNotFoundError as e:
    print(f"[ERROR] File not found: {e}", file=sys.stderr)
    sys.exit(1)

# === [2] Recommend based on first article interacted with ===
def recommend(user_id, X, user_mapper, item_inv_mapper, k=5, metric="cosine"):
    if user_id not in user_mapper:
        print(f"[DEBUG] User ID {user_id} not in user_mapper", file=sys.stderr)
        return []

    user_index = user_mapper[user_id]
    user_vector = X[user_index]

    knn = NearestNeighbors(n_neighbors=k+1, metric=metric, algorithm="brute").fit(X)
    distances, indices = knn.kneighbors(user_vector, return_distance=True)

    rec_indices = indices[0][1:]  # Skip the user themself
    rec_items = []
    for idx in rec_indices:
        row = X[idx].toarray().flatten()
        top_items = row.argsort()[::-1][:k]
        for item_idx in top_items:
            rec_items.append(item_inv_mapper[item_idx])
            if len(rec_items) == k:
                break
        if len(rec_items) == k:
            break

    return rec_items

# === [3] Run via CLI ===
if __name__ == "__main__":
    try:
        user_id = sys.argv[1]
        recs = recommend(user_id, X, user_mapper, item_inv_mapper)
        if recs:
            print(",".join(map(str, recs)))
        else:
            print("", end="")  # empty output if no recs
    except Exception as e:
        print(f"[ERROR] Exception: {e}", file=sys.stderr)

        # ✅ DEBUG: Print 10 shared user IDs between model and CSV
    import pandas as pd
    import numpy as np

    try:
        df = pd.read_csv("users_interactions (1).csv")
        print("[DEBUG] Columns in CSV:", df.columns.tolist(), file=sys.stderr)

        # Use correct CSV column name
        column_name = "personId"

        # Compare using int64 (not string)
        csv_users = set(df[column_name].astype(np.int64).unique())
        model_users = set(user_mapper.keys())

        shared_users = list(model_users & csv_users)

        print("\n[DEBUG] 🔁 Shared users in model + CSV:", file=sys.stderr)
        for uid in shared_users[:10]:
            print(uid)
    except Exception as csv_err:
        print(f"[DEBUG] Couldn't parse CSV: {csv_err}", file=sys.stderr)

