
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle
import os

# Load interactions
df = pd.read_csv("../data/users_interactions.csv")

# Map event types to numeric ratings
event_type_map = {
    "VIEW": 1,
    "LIKE": 2,
    "FOLLOW": 3,
    "BOOKMARK": 4,
    "COMMENT CREATED": 5
}
df["eventType"] = df["eventType"].map(event_type_map)

# Drop NaNs and filter
df = df.dropna(subset=["eventType", "personId", "contentId"])

# Create pivot table
user_item_matrix = df.pivot_table(index="personId", columns="contentId", values="eventType", fill_value=0)

# Create mappings
user_mapper = {user: i for i, user in enumerate(user_item_matrix.index)}
item_mapper = {item: i for i, item in enumerate(user_item_matrix.columns)}
item_inv_mapper = {i: item for item, i in item_mapper.items()}

# Create sparse matrix
X = csr_matrix(user_item_matrix.values)

# Save model
model_path = "collaborative_model.sav"
with open(model_path, "wb") as f:
    pickle.dump((X, user_mapper, item_inv_mapper), f)

print(f"✅ Collaborative model saved to {model_path}")
