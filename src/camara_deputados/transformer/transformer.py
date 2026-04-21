import pandas as pd


class DataTransformer:
    """
    Classe de transformação de dados (orientada a objeto).
    Métodos recebem e retornam DataFrame.
    """

    def apply_types(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        df = df.copy()

        for col, dtype in mapping.items():
            if col not in df.columns:
                continue

            try:
                if dtype == "int":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

                elif dtype == "float":
                    df[col] = pd.to_numeric(df[col], errors="coerce")

                elif dtype == "date":
                    df[col] = pd.to_datetime(df[col], errors="coerce")

                elif dtype == "str":
                    df[col] = df[col].astype("string")

                else:
                    df[col] = df[col].astype(dtype)

            except Exception as e:
                print(f"[apply_types] Erro na coluna '{col}': {e}")

        return df

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
            lambda x: x if isinstance(x, list) else []
        )

        df = df.explode(column)

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

    def rename_and_cast(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        """
        Renomeia e aplica tipo nas colunas.

        Ex:
        mapping = {
            "id": ("id_deputado", "int"),
            "dataNascimento": ("dt_nascimento", "date")
        }
        """

        df = df.copy()

        # 🔹 renomeia tudo de uma vez (melhor prática)
        rename_map = {
            old: new for old, (new, _) in mapping.items()
            if old in df.columns
        }

        df = df.rename(columns=rename_map)

        # 🔹 aplica tipos
        for old_col, (new_col, dtype) in mapping.items():

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

                else:
                    df[new_col] = df[new_col].astype(dtype)

            except Exception as e:
                print(f"[rename_and_cast] Erro na coluna '{new_col}': {e}")

        return df

    def select_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        existing_cols = [col for col in columns if col in df.columns]
        return df[existing_cols].copy()

    def rename_columns(self, df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
        return df.rename(columns=rename_map)

    def drop_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        existing_cols = [col for col in columns if col in df.columns]
        return df.drop(columns=existing_cols)