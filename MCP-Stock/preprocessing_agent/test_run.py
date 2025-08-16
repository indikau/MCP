import json
from utils.preprocess import align_timeframes, calculate_returns, normalize_volume

# Load mock data
with open("tests\input_schema.json") as f:
    raw_data = json.load(f)

# Run preprocessing steps
df = align_timeframes(raw_data)
df = calculate_returns(df)
df = normalize_volume(df)

# Print result
print(df.head())