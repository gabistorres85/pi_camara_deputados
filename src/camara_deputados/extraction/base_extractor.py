class BaseExtractor:

    def __init__(self, api_client):
        self.api_client = api_client

    # 🔹 EXTRAÇÃO SIMPLES
    def extract(self, endpoint: str, desc: str = "Extract"):
        print(f"\n🚀 Iniciando extração: {desc}")

        df = self.api_client.get(endpoint)

        print(f"📦 Registros extraídos: {len(df)}")

        return df

    # 🔹 EXTRAÇÃO POR ID
    def extract_by_ids(self, ids, endpoint_template: str, desc: str = "Extract by ID"):
        lista_dfs = []

        for id in tqdm(ids, desc=desc):
            endpoint = endpoint_template.format(id=id)
            df = self.api_client.get(endpoint)

            if not df.empty:
                df["source_id"] = id
                lista_dfs.append(df)

        return pd.concat(lista_dfs, ignore_index=True) if lista_dfs else pd.DataFrame()

    # 🔹 EXTRAÇÃO POR PERÍODO (ANO)
    def extract_by_period(self, years, endpoint_template: str, desc: str = "Extract by period"):
        print(f"\n🚀 Iniciando extração: {desc}")
        print(f"📅 Período: {list(years)}")

        lista_dfs = []

        for year in tqdm(years, desc=desc):
            endpoint = endpoint_template.format(year=year)

            df = self.api_client.get(endpoint)

            if not df.empty:
                df["ano_ref"] = year  # 🔥 MUITO IMPORTANTE
                lista_dfs.append(df)

        if lista_dfs:
            df_final = pd.concat(lista_dfs, ignore_index=True)
        else:
            df_final = pd.DataFrame()

        print(f"📦 Total registros: {len(df_final)}")

        return df_final