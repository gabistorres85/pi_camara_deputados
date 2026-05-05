def ajustar_tipos_postgres(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in df.columns:
        dtype = df[col].dtype

        # 🔹 string pandas → object
        if str(dtype) == "string":
            df[col] = df[col].astype(object)

        # 🔹 datetime → garantir formato correto
        elif "datetime" in str(dtype):
            df[col] = pd.to_datetime(df[col], errors="coerce")

        # 🔹 inteiro nullable → int ou mantém
        elif str(dtype) == "Int64":
            df[col] = df[col].astype("Int64")

        # 🔹 boolean
        elif str(dtype) == "boolean":
            df[col] = df[col].astype(bool)

    return df