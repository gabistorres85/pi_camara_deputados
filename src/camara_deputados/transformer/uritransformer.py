import pandas as pd
import re


class UriTransformer:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    # 🔹 Extrai ID
    def _extrair_id_valor(self, uri):
        if pd.isnull(uri):
            return None

        match = re.search(r'/(\d+)(?:\?|$)', str(uri))

        if match:
            return int(match.group(1))

        return None

    # 🔹 Extrai tipo + id
    def _extrair_tipo_id_valor(self, uri):
        if pd.isnull(uri):
            return (None, None)

        match = re.search(r'/([^/]+)/(\d+)', str(uri))

        if match:
            return (match.group(1), int(match.group(2)))

        return (None, None)

    # 🔹 Extrair ID (1 coluna)
    def extrair_id(self, coluna_uri: str, nova_coluna: str = None):

        if coluna_uri not in self.df.columns:
            return self

        coluna_destino = nova_coluna if nova_coluna else coluna_uri

        self.df[coluna_destino] = (
            self.df[coluna_uri]
            .apply(self._extrair_id_valor)
            .astype("Int64")
        )

        return self

    # 🔹 Extrair IDs (múltiplas colunas) — CORRIGIDO
    def extrair_ids(self, colunas: dict):

        for coluna_uri, nova_coluna in colunas.items():

            if coluna_uri not in self.df.columns:
                continue

            coluna_destino = nova_coluna if nova_coluna else coluna_uri

            self.df[coluna_destino] = (
                self.df[coluna_uri]
                .apply(self._extrair_id_valor)
                .astype("Int64")
            )

        return self

    # 🔥 Extrair tipo + id (1 coluna) — CORRIGIDO
    def extrair_tipo_e_id(self, coluna_uri: str, col_tipo: str, col_id: str):

        if coluna_uri not in self.df.columns:
            return self

        resultado = self.df[coluna_uri].apply(self._extrair_tipo_id_valor)

        # 🔥 garante expansão correta
        resultado = pd.DataFrame(resultado.tolist(), columns=[col_tipo, col_id])

        self.df[[col_tipo, col_id]] = resultado
        self.df[col_id] = self.df[col_id].astype("Int64")

        return self

    # 🔥 Extrair múltiplos tipo + id — CORRIGIDO
    def extrair_tipos_e_ids(self, colunas: dict):

        for coluna_uri, (col_tipo, col_id) in colunas.items():
            self.extrair_tipo_e_id(coluna_uri, col_tipo, col_id)

        return self

    def get_df(self):
        return self.df