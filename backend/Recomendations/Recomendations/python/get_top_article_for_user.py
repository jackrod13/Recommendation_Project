import os
import sys
import pandas as pd

def log(msg):
    print(f"[DEBUG] {msg}", file=sys.stderr)

interactions_path = os.path.join(os.path.dirname(__file__), 'users_interactions (1).csv')
log(f"Loading CSV from: {interactions_path}")

try:
    df = pd.read_csv(interactions_path)
except Exception as e:
    log(f"Failed to load CSV: {e}")
    sys.exit()

log(f"CSV loaded. Rows: {len(df)}")

event_rank = {
    "VIEW": 1,
    "LIKE": 2,
    "FOLLOW": 3,
    "BOOKMARK": 4,
    "COMMENT CREATED": 5
}
df["eventScore"] = df["eventType"].map(event_rank)

try:
    user_id = sys.argv[1]
    log(f"Searching for userId: {user_id}")

    df["personId"] = df["personId"].astype(str)
    user_data = df[df["personId"] == user_id]
    log(f"Matching rows: {len(user_data)}")

    if user_data.empty:
        print("")  # empty output = no match
    else:
        top_row = user_data.sort_values("eventScore", ascending=False).iloc[0]
        log(f"Top interaction: contentId={top_row['contentId']}, eventType={top_row['eventType']}")
        print(int(top_row["contentId"]))  # ⬅️ ONLY this goes to stdout!

except Exception as e:
    log(f"Script error: {e}")
    print("")
