
from sqlalchemy import text
from database.connection import get_engine


# =========================
# 🔹 AJUSTE DE TIPOS (FIX GLOBAL)
# =========================
def ajustar_tipos_postgres(df):
    df = df.copy()

    for col in df.columns:
        # Converte pandas "string" → object (compatível com PostgreSQL)
        if str(df[col].dtype) == "string":
            df[col] = df[col].astype(object)

    return df


class PostgresLoader:

    def __init__(self):
        self.engine = get_engine()

    # =========================
    # 🔹 LOAD GENÉRICO
    # =========================
    def load(self, df, table_name, schema="dw", truncate=True):

        print(f"📥 Carregando {table_name}...")

        # 🔥 Ajusta tipos antes de enviar para o banco
        df = ajustar_tipos_postgres(df)

        if truncate:
            with self.engine.begin() as conn:
                conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name}"))

        df.to_sql(
            table_name,
            self.engine,
            schema=schema,
            if_exists="append",
            index=False,
            method="multi"
        )

        print(f"✅ {table_name} carregada com {len(df)} registros")

    def remove_duplicates(self, df, subset):
        return df.drop_duplicates(subset=subset)

    # =========================
    # 🔹 DIMENSÕES
    # =========================

    def load_dim_deputado(self, df):
        df = self.remove_duplicates(df, ["id_deputado"])
        self.load(df, "dim_deputado")

    def load_dim_partido(self, df):
        df = self.remove_duplicates(df, ["id_partido"])
        self.load(df, "dim_partido")

    def load_dim_mandato(self, df):
        df = self.remove_duplicates(df, ["id_mandato"])
        self.load(df, "dim_mandato")

    def load_dim_partido_bloco(self, df):
        df = self.remove_duplicates(df, ["id_partido_bloco"])
        self.load(df, "dim_partido_bloco")

    def load_dim_periodo(self, df):
        df = df.dropna(subset=["data"])  # evita erro de PK nula
        df = self.remove_duplicates(df, ["data"])
        self.load(df, "dim_periodo")
            
    def load_dim_tema(self, df):
        df = self.remove_duplicates(df, ["id_tema"])
        self.load(df, "dim_tema") 
    
    def load_dim_autor(self, df):
        df = self.remove_duplicates(df, ["id_autor"])
        self.load(df, "dim_autor")       

    # =========================
    # 🔹 FATOS
    # =========================

    def load_fato_votacao(self, df):
        df = self.remove_duplicates(df, ["id_votacao"])
        self.load(df, "fato_votacao")

    def load_fato_voto_deputado(self, df):
        df = self.remove_duplicates(df, ["id_votacao", "id_deputado"])
        self.load(df, "fato_voto_deputado")

    def load_fato_orientacao(self, df):
        df = self.remove_duplicates(df, ["id_votacao", "id_partido_bloco"])
        self.load(df, "fato_orientacao")
        
    def load_fato_proposicao(self, df):
        df = self.remove_duplicates(df, ["id_proposicao"])
        self.load(df, "fato_proposicao")


  