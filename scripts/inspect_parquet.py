import duckdb
df = duckdb.sql("SELECT * FROM read_parquet('data/snapshots/2026-05-08/0040.parquet')").df()
print("rows:", len(df))
print("cols:", list(df.columns))
print(df[["city", "kind", "bin_label", "midpoint", "best_bid", "best_ask"]].head(5).to_string(index=False))
