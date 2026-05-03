from pathlib import Path
import pandas as pd


class DataLoader:
    def __init__(self, camada: str, caminho_base: str = 'data'):
        self.camada = camada

        # 🔥 resolve base_dir corretamente (script + notebook)
        try:
            base_dir = Path(__file__).resolve()
        except NameError:
            base_dir = Path().resolve()

        # 🔼 sobe até encontrar a pasta /data
        self.base_dir = self._find_project_root(base_dir)

        self.base_path = self.base_dir / caminho_base / camada

        print(f"📍 Caminho resolvido: {self.base_path}")

    def _find_project_root(self, start_path: Path) -> Path:
        for parent in [start_path] + list(start_path.parents):
            if (parent / 'data').exists():
                return parent
        raise FileNotFoundError("❌ Pasta 'data' não encontrada no projeto.")

    def carregar_parquets(self) -> dict:
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
        if not self.base_path.exists():
            raise FileNotFoundError(f"❌ Caminho não encontrado: {self.base_path}")

        return [pasta.name for pasta in self.base_path.iterdir() if pasta.is_dir()]

    def carregar_tabela(self, nome_tabela: str) -> pd.DataFrame:
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
    