
from sqlalchemy import text
from database.connection import get_engine
import pandas as pd



class PostgresLoader:

    def __init__(self):
        self.engine = get_engine()
        
        
    # =========================
    # 🔹 AJUSTE DE TIPOS (FIX GLOBAL)
    # =========================
    def ajustar_tipos_postgres(self, df):
        df = df.copy()

        for col in df.columns:
            # Converte pandas "string" → object (compatível com PostgreSQL)
            if str(df[col].dtype) == "string":
                df[col] = df[col].astype(object)

        return df

    def remove_duplicates(self, df, subset):
        before = len(df)
        df = df.drop_duplicates(subset=subset)
        after = len(df)

        if before != after:
            print(f"⚠️ Removidos {before - after} duplicados ({subset})")

        return df
    
    
    # =========================
    # 🔹 LOAD GENÉRICO
    # =========================


    def load(self, df, table_name, schema="dw", truncate=True):

        print(f"\n📥 Carregando {table_name}...")
        print(f"📊 Registros recebidos: {df.shape[0]} | Colunas: {df.shape[1]}")

        # 🔥 Ajusta tipos
        df = self.ajustar_tipos_postgres(df)

        try:
            with self.engine.begin() as conn:

                if truncate:
                    conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name}"))

                df.to_sql(
                    table_name,
                    conn,  # 🔥 mesma conexão
                    schema=schema,
                    if_exists="append",
                    index=False,
                    method="multi"
                )

            print(f"✅ {table_name} carregada com {len(df)} registros")

        except Exception as e:
            print(f"\n❌ ERRO ao carregar {table_name}")
            print(f"💥 Tipo do erro: {type(e).__name__}")
            print(f"📄 Mensagem: {str(e)}")

            # 🔥 erro real do banco (limpo)
            if hasattr(e, 'orig'):
                print("\n🎯 ERRO DO BANCO:")
                print(e.orig)

            # =========================
            # 🔎 DEBUG DE DADOS (AMOSTRA)
            # =========================
            print("\n🔍 Amostra dos dados enviados:")
            print(df.head(5))

            print("\n🔍 Tipos das colunas:")
            print(df.dtypes)

            # =========================
            # 🔥 TESTE LINHA A LINHA
            # =========================
            print("\n🧪 Tentando identificar linha problemática...")

            for i, row in df.head(1000).iterrows():  # 🔥 limite
                try:
                    row_df = pd.DataFrame([row])

                    row_df.to_sql(
                        table_name,
                        self.engine,
                        schema=schema,
                        if_exists="append",
                        index=False
                    )

                except Exception as row_error:
                    print(f"\n🚨 ERRO NA LINHA {i}")
                    print(row.to_dict())
                    print(f"💥 {row_error}")
                    break

                raise e  # 🔥 re-levanta erro


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
        
    def load_dim_proposicao(self, df):
        df = self.remove_duplicates(df, ["id_proposicao"])
        self.load(df, "dim_proposicao")
        
    def load_dim_legislatura(self, df):
        df = self.remove_duplicates(df, ["id_legislatura"])
        self.load(df, "dim_legislatura")        

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

          
    def load_fato_mandato(self, df):
        df = self.remove_duplicates(df, ["id_mandato"])
        self.load(df, "fato_mandato")

    def load_bridge_autor_deputado(self, df):
        df = self.remove_duplicates(df, ["id_autor"])
        self.load(df, "bridge_autor_deputado")