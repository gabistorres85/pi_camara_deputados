import pandas as pd 

class DataModeling:

    def __init__(self, transformer):
        self.transformer = transformer

    def criar_dim(
        self,
        df: pd.DataFrame,
        colunas: list,
        gerar_id: bool = False,
        colunas_id: list = None,
        nome_id: str = None,
        chave_duplicidade: list = None
    ) -> pd.DataFrame:

        df_dim = df[colunas].copy()

        # 🔹 deduplicação
        if chave_duplicidade:
            df_dim = df_dim.drop_duplicates(subset=chave_duplicidade)
        else:
            df_dim = df_dim.drop_duplicates()

        # 🔹 geração de ID opcional
        if gerar_id:
            df_dim = self.transformer.gerar_id_hash(
                df_dim,
                colunas=colunas_id,
                nome_id=nome_id
            )

        return df_dim