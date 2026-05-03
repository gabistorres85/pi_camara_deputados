from sqlalchemy import text
from src.database.connection import get_engine


class PostgresLoader:

    def __init__(self):
        self.engine = get_engine()

    def load(self, df, table_name, schema="dw", if_exists="append"):

        print(f"📥 Carregando {table_name}...")

        df.to_sql(
            table_name,
            self.engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            method="multi"
        )

        print(f"✅ {table_name} carregada com {len(df)} registros")
    
    def remove_duplicates(self, df, subset):
        return df.drop_duplicates(subset=subset)
    
    # =========================
    # 🔹 DIM DEPUTADO 
    # =========================

    def load_dim_deputado(self, df):

        df = self.remove_duplicates(df, ["id_Deputado"])

        self.load(df, "dim_deputado")

    # =========================
    # 🔹 DIM PARTIDO 
    # =========================

    def load_dim_partido(self, df):

        df = self.remove_duplicates(df, ["id_Partido"])

        self.load(df, "dim_partido")

    # =========================
    # 🔹 DIM MANDATO 
    # =========================

    def load_dim_mandato(self, df):

        df = self.remove_duplicates(df, ["id_Mandato"])

        self.load(df, "dim_mandato")

    # =========================
    # 🔹 DIM PROPOSICAO 
    # =========================
    
    def load_dim_proposicao(self, df):

        df = self.remove_duplicates(df, ["id_proposicao"])

        self.load(df, "dim_proposicao")

    # =========================
    # 🔹 DIM TEMPO 
    # =========================

    def load_dim_tempo(self, df):

        df = self.remove_duplicates(df,['data'])

        self.load(df, "dim_tempo")

    # =========================
    # 🔹 DIM TEMA 
    # =========================
    
    def load_dim_tema(self, df):

        df = self.remove_duplicates(df, ["id_tema"])

        self.load(df, "dim_tema")

    # =========================
    # 🔹 DIM AUTOR 
    # =========================
    
    def load_dim_autor(self, df):

        df = self.remove_duplicates(df, ["id_Autor"])

        self.load(df, "dim_autor")

    # =========================
    # 🔹 FATO VOTACAO
    # =========================
    
    def load_fato_votacao(self, df):

        df = self.remove_duplicates(df, ["id_votacao"])

        self.load(df, "fato_votacao")
    
    
    # =========================
    # 🔹 FATO VOTO DEPUTADO
    # =========================
    
    def load_fato_voto_deputado(self, df):

        df = self.remove_duplicates(df, [["id_Deputado",'id_Votacao']])

        self.load(df, "fato_voto_deputado")
        
    # =========================
    # 🔹 FATO ORIENTACAO PARTIDO
    # =========================
    
    def load_fato_orientacao_partido(self, df):

        df = self.remove_duplicates(df, [["id_Deputado",'id_Votacao']])

        self.load(df, "fato_orientacao_partido")
        
    
    # =========================
    # 🔹 BRIDGE VOTACAO PROPOSICAO
    # =========================
    
    def load_bridge_votacao_proposicao(self, df):

        df = self.remove_duplicates(df, [["id_votacao",'id_proposicao']])

        self.load(df, "bridge_votacao_proposicao")
        
    # =========================
    # 🔹 BRIDGE PROPOSICAO TEMA 
    # =========================
    
    def load_bridge_proposicao_tema(self, df):

        df = self.remove_duplicates(df, [["id_tema",'id_proposicao']])

        self.load(df, "bridge_proposicao_tema")

    # =========================
    # 🔹 BRIDGE PROPOSICAO TEMA 
    # =========================
    
    def load_bridge_proposicao_autor(self, df):

        df = self.remove_duplicates(df, [["id_Proposicao",'id_Autor']])

        self.load(df, "bridge_proposicao_autor")

