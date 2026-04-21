import pandas as pd
import re


class UriTransformer:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def extrair_id(self, coluna_uri: str, nova_coluna: str):
        """
        Extrai o ID numérico da URI e retorna como Int64 (compatível com BIGINT)
        """

        def extrair(uri):
            if pd.isnull(uri):
                return None

            match = re.search(r'/(\d+)(?:\?|$)', str(uri))

            if match:
                return int(match.group(1))

            return None

        self.df[nova_coluna] = (
            self.df[coluna_uri]
            .apply(extrair)
            .astype("Int64")  # tipo inteiro com suporte a nulos
        )

        return self

    def get_df(self):
        return self.df