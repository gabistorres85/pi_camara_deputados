import pandas as pd
import re


class DataTransformer:
    """
    Classe única de transformação de dados (stateless).
    Todos os métodos recebem e retornam DataFrame.
    """

    # =========================
    # 🔹 RENAME + CAST + SELECT
    # =========================
    def rename_and_cast(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        df = df.copy()

        rename_map = {
            old: new for old, (new, _) in mapping.items()
            if old in df.columns
        }

        df = df.rename(columns=rename_map)

        for _, (new_col, dtype) in mapping.items():

            if new_col not in df.columns:
                continue

            try:
                if dtype == "int":
                    df[new_col] = pd.to_numeric(df[new_col], errors="coerce").astype("Int64")

                elif dtype == "float":
                    df[new_col] = pd.to_numeric(df[new_col], errors="coerce")

                elif dtype == "date":
                    df[new_col] = pd.to_datetime(df[new_col], errors="coerce")

                elif dtype == "str":
                    df[new_col] = df[new_col].astype("string")

                elif dtype == "bool":
                    df[new_col] = df[new_col].astype("boolean")

                else:
                    df[new_col] = df[new_col].astype(dtype)

            except Exception as e:
                print(f"[rename_and_cast] Erro na coluna '{new_col}': {e}")

        colunas_final = list(rename_map.values())

        return df[colunas_final]

    # =========================
    # 🔹 EXPLODE + NORMALIZE
    # =========================
    def explode_and_extract(
        self,
        df: pd.DataFrame,
        column: str,
        keys: list,
        rename_map: dict = None
    ) -> pd.DataFrame:

        df = df.copy()

        if column not in df.columns:
            return df

        df[column] = df[column].apply(
            lambda x: x if isinstance(x, list)
            else [x] if isinstance(x, dict)
            else []
        )

        df = df.explode(column)

        df[column] = df[column].apply(
            lambda x: x if isinstance(x, dict) else {}
        )

        normalized = pd.json_normalize(df[column])

        for key in keys:
            if key not in normalized.columns:
                normalized[key] = pd.NA

        normalized = normalized[keys]

        if rename_map:
            normalized = normalized.rename(columns=rename_map)

        df = df.drop(columns=[column]).reset_index(drop=True)

        df = pd.concat([df, normalized], axis=1)

        return df

    # =========================
    # 🔹 URI → ID
    # ========================= 
    def _extrair_id(self, uri):
        if pd.isnull(uri):
            return None

        match = re.search(r'/(\d+)(?:\?|$)', str(uri))
        return int(match.group(1)) if match else None

    def extrair_ids(self, df: pd.DataFrame, colunas: dict) -> pd.DataFrame:
        df = df.copy()

        for coluna_uri, nova_coluna in colunas.items():

            if coluna_uri not in df.columns:
                continue

            df[nova_coluna] = (
                df[coluna_uri]
                .apply(self._extrair_id)
                .astype("Int64")
            )

        return df

    # =========================
    # 🔹 URI → TIPO + ID
    # =========================
    def _extrair_tipo_id(self, uri):
        if pd.isnull(uri):
            return (None, None)

        match = re.search(r'/([^/]+)/(\d+)', str(uri))
        return (match.group(1), int(match.group(2))) if match else (None, None)

    def extrair_tipos_e_ids(self, df: pd.DataFrame, colunas: dict) -> pd.DataFrame:
        df = df.copy()

        for coluna_uri, (col_tipo, col_id) in colunas.items():

            if coluna_uri not in df.columns:
                continue

            resultado = df[coluna_uri].apply(self._extrair_tipo_id)

            resultado = pd.DataFrame(
                resultado.tolist(),
                columns=[col_tipo, col_id]
            )

            df[[col_tipo, col_id]] = resultado
            df[col_id] = df[col_id].astype("Int64")

        return df

    # =========================
    # 🔹 GERAÇÃO DE ID (HASH)
    # =========================
    def gerar_id_hash(self, df: pd.DataFrame, colunas: list, nome_id: str) -> pd.DataFrame:
        import hashlib

        df = df.copy()

        for col in colunas:
            if col not in df.columns:
                raise ValueError(f"Coluna '{col}' não existe no DataFrame")

        def _hash(row):
            valores = '|'.join([
                str(row[col]).strip().upper() if pd.notna(row[col]) else ''
                for col in colunas
            ])
            return hashlib.md5(valores.encode()).hexdigest()

        df[nome_id] = df.apply(_hash, axis=1)

        return df

    # =========================
    # 🔹 TRATAR LISTAS
    # =========================
    def split_and_explode(
        self,
        df: pd.DataFrame,
        coluna: str,
        nova_coluna: str,
        sep: str = ","
    ) -> pd.DataFrame:

        df = df.copy()

        if coluna not in df.columns:
            return df

        df[coluna] = (
            df[coluna]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.strip()
        )

        df[nova_coluna] = df[coluna].str.split(sep)

        df = df.explode(nova_coluna)

        df[nova_coluna] = df[nova_coluna].str.strip()

        df = df[df[nova_coluna] != ""]

        return df