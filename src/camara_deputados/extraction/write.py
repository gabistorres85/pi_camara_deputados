
import pandas as pd
import os
from datetime import datetime

class DataWrite:

    def __init__(self):
        # pega raiz do projeto (subindo a partir do arquivo atual)
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../..")
        )

    def save_bronze(self, df, dataset, layer="bronze"):
        
        path = os.path.join(
            self.project_root,
            "data",
            layer,
            dataset,
            f"{dataset}.parquet"
        )

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if "data_extracao" not in df.columns:
            df["data_extracao"] = datetime.now()

        df.to_parquet(path, index=False)

        print(f"💾 Salvo em: {path}")
   