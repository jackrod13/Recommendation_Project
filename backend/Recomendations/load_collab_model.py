import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np
from scipy.sparse import csr_matrix

# Load the model
with open('collaborative_model.sav', 'rb') as f:
    X, item_mapper, item_inv_mapper = pickle.load(f)

# Recommendation function
def recommend(itemId, X, item_mapper, item_inv_mapper, k=5, metric='cosine', messages=True):
    rec_ids = []

    item = item_mapper[itemId]
    item_vector = X[item]

    knn = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric).fit(X)
    rec = knn.kneighbors(item_vector.reshape(1, -1), return_distance=True)

    rec_indices = rec[1][0][1:]
    rec_distances = rec[0][0][1:]

    for idx in rec_indices:
        rec_ids.append(item_inv_mapper[idx])

    if messages:
        print(f'List of recommended item indices:\n{rec_indices}\n')
        print(f'List of recommended contentIds:\n{rec_ids}\n')
        print(f'Similarity distances:\n{rec_distances}\n')

    return rec_ids, rec_distances

# Example usage
if __name__ == '__main__':
    # Replace with a real contentId from your data
    example_article_id = list(item_mapper.keys())[0]
    rec_ids, rec_distances = recommend(example_article_id, X, item_mapper, item_inv_mapper)
