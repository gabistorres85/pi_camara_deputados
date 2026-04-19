
import pandas as pd

class DataLoader:

    def save_parquet(self, df: pd.DataFrame, path: str, partition_cols=None):
        if df.empty:
            print("DataFrame vazio. Nada foi salvo.")
            return

        df.to_parquet(
            path,
            index=False,
            partition_cols=partition_cols
        )

        print(f"Arquivo salvo em: {path}")