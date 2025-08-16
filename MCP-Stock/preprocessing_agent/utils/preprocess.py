import pandas as pd

def align_timeframes(raw_data: dict) -> pd.DataFrame:
    dfs = []
    for symbol, entries in raw_data.items():
        df = pd.DataFrame(entries)
        df["symbol"] = symbol
        dfs.append(df)
    merged = pd.concat(dfs, ignore_index=True)
    return merged.sort_values(by=["date", "symbol"])

def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["daily_return"] = df.groupby("symbol")["close"].pct_change()
    return df.dropna()

def normalize_volume(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["normalized_volume"] = df.groupby("symbol")["volume"].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    return df