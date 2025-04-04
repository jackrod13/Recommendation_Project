import os
import sys
import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd  # Optional, in case you use the CSV

# === 1. Load the saved model ===
model_path = os.path.join(os.path.dirname(__file__), 'collaborative_model.sav')
with open(model_path, 'rb') as f:
    X, item_mapper, item_inv_mapper = pickle.load(f)

# === Optional: Load user interactions CSV (if needed later) ===
# csv_path = os.path.join(os.path.dirname(__file__), 'users_interactions (1).csv')
# df_interactions = pd.read_csv(csv_path)

# === 2. Recommendation function ===
def recommend(itemId, X, item_mapper, item_inv_mapper, k=5, metric='cosine'):
    if itemId not in item_mapper:
        return []

    item_index = item_mapper[itemId]
    item_vector = X[item_index]

    knn = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric).fit(X)
    rec = knn.kneighbors(item_vector.reshape(1, -1), return_distance=True)

    rec_indices = rec[1][0][1:]  # skip the item itself
    rec_ids = [item_inv_mapper[idx] for idx in rec_indices]

    return rec_ids

# === 3. Accept itemId from command line ===
try:
    item_id = int(sys.argv[1])
    recs = recommend(item_id, X, item_mapper, item_inv_mapper)
    print(','.join(map(str, recs)))
except Exception as e:
    print("")
