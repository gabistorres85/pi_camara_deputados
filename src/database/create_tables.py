
from sqlalchemy import text
from database.connection import get_engine


def create_tables():
    engine = get_engine()

    with engine.connect() as conn:

        # =========================
        # 🔥 RESET TOTAL
        # =========================
        conn.execute(text("""
            DROP SCHEMA IF EXISTS dw CASCADE;
            CREATE SCHEMA dw;
        """))

        # =========================
        # 🔹 DIM DEPUTADO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_deputado (
                id_deputado INT PRIMARY KEY,
                nome VARCHAR(80),
                sexo VARCHAR(10),
                dat_nasc DATE,
                dat_falecimento DATE,
                uf_nasc VARCHAR(5),
                municipio_nasc VARCHAR(50),
                data_extracao TIMESTAMP
            );
        """))

        # =========================
        # 🔹 DIM PARTIDO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_partido (
                id_partido VARCHAR(32) PRIMARY KEY,
                sigla_partido VARCHAR(20),
                data_extracao TIMESTAMP
            );
        """))

        # =========================
        # 🔹 DIM MANDATO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_mandato (
                id_mandato INT PRIMARY KEY,
                sigla_partido VARCHAR(20),
                uf_representante VARCHAR(2),
                id_legislatura INT,
                id_deputado INT,
                id_partido VARCHAR(32),
                data_extracao TIMESTAMP
            );
        """))
        
        # =========================
        # 🔹 DIM PROPOSICAO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_proposicao (
                id_proposicao INT PRIMARY KEY,
                cod_tipo VARCHAR(50),
                tipo_proposicao VARCHAR(50),
                num_proposicao INT,
                num_ano INT,
                nom_regime VARCHAR(50),
                dat_apresentacao DATE,
                nom_tramitacao VARCHAR(100),
                data_extracao TIMESTAMP
            );
        """))
        
        # =========================
        # 🔹 DIM PARTIDO BLOCO 
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_partido_bloco (
                id_partido_bloco VARCHAR(32) PRIMARY KEY,
                nom_sigla VARCHAR(50),
                data_extracao TIMESTAMP
            );
        """))
        
            
        # =========================
        # 🔹 DIM AUTOR
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_autor (
                id_autor VARCHAR(50) PRIMARY KEY,
                tipo_autor VARCHAR(100),
                nome_autor VARCHAR(100),
                id_deputado INT,
                cod_tipo VARCHAR(20),
                data_extracao TIMESTAMP
            );
        """))
        
        # =========================
        # 🔹 DIM PERIODO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_periodo (
                data DATE PRIMARY KEY,
                ano INT,
                mes INT,
                dia INT,
                trimestre INT,
                data_extracao TIMESTAMP
            );
        """))
        
         # =========================
        # 🔹 DIM LEGISLATURA
        # =========================
        conn.execute(text("""
           CREATE TABLE dw.dim_legislatura (
            id_legislatura INT PRIMARY KEY,
            data_extracao TIMESTAMP
            );
        """))


    
        # =========================
        # 🔹 FATO VOTO DEPUTADO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.fato_voto_deputado (
                id_votacao VARCHAR(20),
                id_deputado INT,
                id_proposicao INT,
                id_partido VARCHAR(40),
                id_legislatura INT,
                nom_voto VARCHAR(20),
                dat_registro DATE,
                data_extracao TIMESTAMP,

                PRIMARY KEY (id_votacao, id_deputado)
            );
        """))
        
        # =========================
        # 🔹 FATO VOTO MANDATO
        # =========================
        conn.execute(text("""
           CREATE TABLE dw.fato_mandato (
            id_mandato INT,
            id_deputado INT,
            id_partido VARCHAR(50),
            id_legislatura INT,
            data_extracao TIMESTAMP,

            PRIMARY KEY (id_mandato)
            );
        """))

        # =========================
        # 🔹 FATO ORIENTACAO (CORRIGIDA)
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.fato_orientacao (
                id_votacao VARCHAR(20),
                id_partido_bloco VARCHAR(32),
                nom_orientacao_voto VARCHAR(50),
                data_extracao TIMESTAMP,

                PRIMARY KEY (id_votacao, id_partido_bloco)
            );
        """))
        
       
        # =========================
        # 🔹 MINI FATO PROPOSICAO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.fato_proposicao (
                id_proposicao INT,
                id_autor INT,
                cod_tema VARCHAR(20),
                data_extracao TIMESTAMP,
                PRIMARY KEY (id_proposicao)
            );
        """))



        # =========================
        # 🔹 DIM TEMA 
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.dim_tema (
                id_tema INT PRIMARY KEY,
                nome_tema VARCHAR(100),
                data_extracao TIMESTAMP
                );
        """))
        
        # =========================
        # 🔹 BRIDGE AUTOR DEPUTADO
        # =========================
        conn.execute(text("""
            CREATE TABLE dw.bridge_autor_deputado (
                id_autor INT PRIMARY KEY,
                id_deputado INT,
                data_extracao TIMESTAMP
                );
        """))
        
 

        conn.commit()

    print("🔥 DW recriado com sucesso (modo destruição total ativado)")


if __name__ == "__main__":
    create_tables()
