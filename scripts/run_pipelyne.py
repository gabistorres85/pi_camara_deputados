from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from camara_deputados.ingestion.data_loader import DataLoader
from database.load_postgree import PostgresLoader


def main():

    print("🚀 INICIANDO PIPELINE GOLD → DW\n")

    gold = DataLoader('gold')
    loader = PostgresLoader()

    # 🔹 carregar dados da gold
    dfs = gold.carregar_parquets()

    # =========================
    # 🔹 DIMENSÕES
    # =========================
    print("\n📦 CARREGANDO DIMENSÕES\n")

    loader.load_dim_deputado(dfs['dim_deputado'])
    loader.load_dim_partido(dfs['dim_partido'])
    loader.load_dim_mandato(dfs['dim_mandato'])
    loader.load_dim_partido_bloco(dfs['dim_partido_bloco'])
    loader.load_dim_periodo(dfs['dim_periodo'])
    loader.load_dim_tema(dfs['dim_tema'])
    loader.load_dim_autor(dfs['dim_autor'])

    
    

    # =========================
    # 🔹 FATOS
    # =========================
    print("\n📊 CARREGANDO FATOS\n")

    loader.load_fato_voto_deputado(dfs['fato_voto_deputado'])
    loader.load_fato_orientacao(dfs['fato_orientacao'])
    loader.load_fato_proposicao(dfs['fato_proposicao'])

    print("\n🔥 PIPELINE FINALIZADO COM SUCESSO 🔥")

    
if __name__ == "__main__":
    main()
