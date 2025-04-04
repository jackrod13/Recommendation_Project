import sys
import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np
from scipy.sparse import csr_matrix

# Load the model
with open("collaborative_model.sav", "rb") as f:
    X, user_mapper, item_inv_mapper = pickle.load(f)

def recommend(user_id, X, user_mapper, item_inv_mapper, k=5, metric="cosine"):
    if user_id not in user_mapper:
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

# Run from command line
if __name__ == "__main__":
    try:
        user_id = sys.argv[1]
        recs = recommend(user_id, X, user_mapper, item_inv_mapper)
        print(",".join(map(str, recs)))
    except Exception as e:
        print("")
