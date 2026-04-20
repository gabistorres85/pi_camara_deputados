from pathlib import Path
import pandas as pd


class DataLoader:
    def __init__(self, camada: str, caminho_base: str = '../data'):
        self.base_dir = Path().resolve()
        self.base_path = self.base_dir / caminho_base / camada
        self.camada = camada

    def carregar_parquets(self) -> dict:
        """
        Carrega todos os parquets da camada e retorna um dicionário de DataFrames
        {nome_da_tabela: DataFrame}
        """

        print(f"\n📂 Lendo dados da camada {self.camada}: {self.base_path}\n")

        if not self.base_path.exists():
            raise FileNotFoundError(f"❌ Caminho não encontrado: {self.base_path}")

        dfs = {}

        for pasta in self.base_path.iterdir():
            if pasta.is_dir():
                try:
                    arquivos_parquet = list(pasta.glob("*.parquet"))

                    if not arquivos_parquet:
                        print(f"⚠️ {pasta.name}: nenhum parquet encontrado")
                        continue

                    df = pd.concat(
                        [pd.read_parquet(arq) for arq in arquivos_parquet],
                        ignore_index=True
                    )

                    dfs[pasta.name] = df

                    print(f"✅ {pasta.name}: {df.shape[0]} linhas, {df.shape[1]} colunas")

                except Exception as e:
                    print(f"❌ Erro ao processar {pasta.name}: {e}")

        print("\n🎯 Carregamento finalizado.")
        return dfs

    def listar_tabelas(self) -> list:
        """
        Lista as tabelas disponíveis na camada
        """
        if not self.base_path.exists():
            raise FileNotFoundError(f"❌ Caminho não encontrado: {self.base_path}")

        return [pasta.name for pasta in self.base_path.iterdir() if pasta.is_dir()]

    def carregar_tabela(self, nome_tabela: str) -> pd.DataFrame:
        """
        Carrega apenas uma tabela específica
        """

        caminho_tabela = self.base_path / nome_tabela

        if not caminho_tabela.exists():
            raise FileNotFoundError(f"❌ Tabela não encontrada: {nome_tabela}")

        arquivos_parquet = list(caminho_tabela.glob("*.parquet"))

        if not arquivos_parquet:
            raise ValueError(f"⚠️ Nenhum parquet encontrado em {nome_tabela}")

        df = pd.concat(
            [pd.read_parquet(arq) for arq in arquivos_parquet],
            ignore_index=True
        )

        print(f"✅ {nome_tabela}: {df.shape[0]} linhas, {df.shape[1]} colunas")

        return df