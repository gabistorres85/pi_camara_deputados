from sqlalchemy import text
from src.database.connection import get_engine


def create_tables():
    engine = get_engine()

    with engine.connect() as conn:

        # =========================
        # 🔹 SCHEMA
        # =========================
        conn.execute(text("""
            CREATE SCHEMA IF NOT EXISTS dw;
        """))

        # =========================
        # 🔹 DIM DEPUTADO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_deputado (
                id_deputado INT PRIMARY KEY,
                nom_NomeCivil VARCHAR(80),
                nom_Sexo VARCHAR(10)
                dat_DataNasc DATE,
                dat_DataFalecimento DATE,
                nom_UFNasc VARCHAR(5),
                nom_MunicipioNasci VARCHAR(50)
            );
        """))

        # =========================
        # 🔹 DIM PARTIDO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_partido (
                id_Partido INT PRIMARY KEY,
                nom_SiglaPartido VARCHAR(20)
            );
        """))

        # =========================
        # 🔹 DIM MANDATO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_mandato (
                id_Mandato INT PRIMARY KEY,
                id_Deputado INT,
                id_Partido INT,
                id_legislatura INT,
                nom_UFRepresenta VARCHAR(2)
            );
        """))

        # =========================
        # 🔹 DIM PROPOSICAO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_proposicao (
                id_proposicao INT PRIMARY KEY,
                cod_Tipo VARCHAR(50),
                nom_TipoProposicao VARCHAR(50),
                num_NumeroProp INT,
                num_ano INT,
                nom_Ementa TEXT,
                nom_regime VARCHAR(50),
                dat_Apresentacao DATE
            );
        """))

        # =========================
        # 🔹 DIM TEMPO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_tempo (
                data DATE PRIMARY KEY,
                ano INT,
                mes INT,
                dia INT,
                trimestre INT
            );
        """))

        # =========================
        # 🔹 DIM TEMA
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_tema (
                id_tema INT,
                tema VARCHAR(100)
            );
        """))

        # =========================
        # 🔹 DIM AUTOR
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_autor (
                id_Autor INT,
                nom_Autor VARCHAR(100),
                cod_TipoAutor VARCHAR(15)
            );
        """))

        # =========================
        # 🔹 FATO VOTACAO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.fato_votacao (
                id_votacao VARCHAR(20) PRIMARY KEY,
                id_Orgao INT,
                dat_DataVotacao DATE,
                dat_DataRegistro DATE,
                ind_Aprovado INT
            );
        """))

        # =========================
        # 🔹 FATO VOTO DEPUTADO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.fato_voto_deputado (
                id_Votacao VARCHAR(20),
                id_Deputado INT,
                nom_Voto VARCHAR(50),

                PRIMARY KEY (id_Votacao, id_Deputado)
            );
        """))

        # =========================
        # 🔹 FATO ORIENTACAO PARTIDO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.fato_orientacao_partido (
                id_Votacao VARCHAR(20),
                id_Partido INT,
                nom_Orientacao VARCHAR(50),

                PRIMARY KEY (id_votacao, id_partido)
            );
        """))

        # =========================
        # 🔹 BRIDGE VOTACAO PROPOSICAO
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.bridge_votacao_proposicao (
                id_votacao VARCHAR(20),
                id_proposicao INT,

                PRIMARY KEY (id_votacao, id_proposicao)
            );
        """))

        # =========================
        # 🔹 BRIDGE PROPOSICAO TEMA 
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.bridge_proposicao_tema (
                id_tema INT,
                id_proposicao INT,

                PRIMARY KEY (id_tema, id_proposicao)
            );
        """))

        # =========================
        # 🔹 BRIDGE PROPOSICAO AUTOR 
        # =========================
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.bridge_proposicao_autor (
                id_Proposicao INT,
                id_Autor INT,

                PRIMARY KEY (id_Proposicao, id_Autor)
            );
        """))

        conn.commit()

    print("✅ DW completo criado (dim + fato)!")

if __name__ == "__main__":
    create_tables()