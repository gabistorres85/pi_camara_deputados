from src.database.load_postgree import PostgresLoader
from src.camara_deputados.ingestion.data_loader import DataLoader
from sqlalchemy import text

gold = DataLoader('gold')
loader = PostgresLoader()

dfs_gold = gold.carregar_parquets()

df_dim_deputado = dfs_gold['dim_deputado']
df_dim_deputado = df_dim_deputado.drop_duplicates(subset=["id_Deputado"])

df_dim_deputado.head(1).to_sql(
    "dim_deputado",
    loader.engine,
    schema="dw",
    if_exists="append",
    index=False
)
