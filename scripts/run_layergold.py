import pandas as pd
from camara_deputados.ingestion.data_loader import DataLoader
from camara_deputados.extraction.write import DataWrite
from camara_deputados.modeling.modeling import DataModeling
from camara_deputados.transformer.transformer import DataTransformer

# instâncias
silver = DataLoader('silver')
salva = DataWrite()
transformer = DataTransformer()
modeling = DataModeling(transformer)

# carrega dados
dfs_silver = silver.carregar_parquets()


def normalizar_nome(df, col):
    pass


# 🔥 FUNÇÃO ADICIONADA
def limpar_colunas_merge(df):
    df = df.copy()

    cols_data = [c for c in df.columns if 'data_extracao' in c]

    if 'data_extracao' in df.columns:
        cols_remover = [c for c in cols_data if c != 'data_extracao']
        df = df.drop(columns=cols_remover, errors='ignore')
    else:
        for col in cols_data:
            df = df.rename(columns={col: 'data_extracao'})
            break

    df = df.loc[:, ~df.columns.duplicated()]

    return df


# -------------------------------------
# DIM DEPUTADO
# -------------------------------------
df_deputado = dfs_silver['silver_deputado']

mapping_deputado = {
    'id_deputado': ('id_deputado', 'int'),
    'nome': ('nome', 'str'),
    'sexo': ('sexo', 'str'),
    'dat_nasc': ('dat_nasc', 'date'),
    'dat_falecimento': ('dat_falecimento', 'date'),
    'uf_nasc': ('uf_nasc', 'str'),
    'municipio_nasc': ('municipio_nasc', 'str')
}

dim_deputado = transformer.rename_and_cast(df_deputado, mapping_deputado)

dim_deputado = modeling.criar_dim(
    df=dim_deputado,
    colunas=[v[0] for v in mapping_deputado.values()],
    chave_duplicidade=['id_deputado']
)

salva.save_parquet(dim_deputado, 'dim_deputado', 'gold')


# -------------------------------------
# DIM PARTIDO
# -------------------------------------
mapping_partido = {'nom_sigla_partido': ('sigla_partido', 'str')}

dim_partido = transformer.rename_and_cast(df_deputado, mapping_partido)

dim_partido['sigla_partido'] = dim_partido['sigla_partido'].str.upper().str.strip()

dim_partido = modeling.criar_dim(
    df=dim_partido,
    colunas=['sigla_partido'],
    gerar_id=True,
    colunas_id=['sigla_partido'],
    nome_id='id_partido',
    chave_duplicidade=['sigla_partido']
)

salva.save_parquet(dim_partido, 'dim_partido', 'gold')


# -------------------------------------
# DIM MANDATO
# -------------------------------------
df_mandato = dfs_silver['silver_deputado'][[
    'id_mandato',
    'nom_sigla_partido',
    'nom_uf_representa',
    'id_legislatura',
    'id_deputado'
]].rename(columns={
    'nom_sigla_partido': 'sigla_partido',
    'nom_uf_representa': 'uf_representante'
})

df_mandato['sigla_partido'] = df_mandato['sigla_partido'].str.upper().str.strip()

df_mandato = df_mandato.merge(dim_partido, on='sigla_partido', how='left')

dim_mandato = modeling.criar_dim(
    df=df_mandato[[
        'id_mandato',
        'sigla_partido',
        'uf_representante',
        'id_legislatura',
        'id_deputado',
        'id_partido'
    ]],
    colunas=[
        'id_mandato',
        'sigla_partido',
        'uf_representante',
        'id_legislatura',
        'id_deputado',
        'id_partido'
    ],
    chave_duplicidade=['id_mandato']
)

salva.save_parquet(dim_mandato, 'dim_mandato', 'gold')


# -------------------------------------
# DIM PARTIDO BLOCO
# -------------------------------------
df_partido_bloco = dfs_silver['silver_orientacao'][[
    'nom_sigla_partido_bloco'
]].rename(columns={'nom_sigla_partido_bloco': 'nom_sigla'})

df_partido_bloco['nom_sigla'] = df_partido_bloco['nom_sigla'].str.upper().str.strip()

dim_partido_bloco = modeling.criar_dim(
    df=df_partido_bloco,
    colunas=['nom_sigla'],
    gerar_id=True,
    colunas_id=['nom_sigla'],
    nome_id='id_partido_bloco',
    chave_duplicidade=['nom_sigla']
)

salva.save_parquet(dim_partido_bloco, 'dim_partido_bloco', 'gold')


# -------------------------------------
# DIM TEMA
# -------------------------------------
df_tema = dfs_silver['silver_temas_proposicao'][[
    'cod_tema',
    'nom_tema'
]].rename(columns={
    'cod_tema': 'id_tema',
    'nom_tema': 'nome_tema'
})

dim_tema = modeling.criar_dim(
    df=df_tema,
    colunas=['id_tema', 'nome_tema'],
    chave_duplicidade=['id_tema']
)

salva.save_parquet(dim_tema, 'dim_tema', 'gold')


# -------------------------------------
# DIM AUTOR
# -------------------------------------
df_autor = dfs_silver['silver_autores'].rename(columns={
    'nom_autor': 'nome_autor',
    'nom_tipo_autor': 'tipo_autor',
    'cod_tipo_autor': 'cod_tipo'
})

dim_autor = modeling.criar_dim(
    df=df_autor[['id_autor', 'tipo_autor', 'nome_autor', 'cod_tipo']],
    colunas=['id_autor', 'tipo_autor', 'nome_autor', 'cod_tipo'],
    chave_duplicidade=['id_autor']
)

salva.save_parquet(dim_autor, 'dim_autor', 'gold')


# -------------------------------------
# FATO VOTO DEPUTADO
# -------------------------------------
df_voto_deputado = dfs_silver['silver_votos_deputados']

df_votacao = dfs_silver['silver_votacao_proposicao'][[
    'id_votacao',
    'id_proposicao'
]]

df_voto_deputado = df_voto_deputado.merge(
    df_votacao,
    on='id_votacao',
    how='left'
)

df_voto_deputado = limpar_colunas_merge(df_voto_deputado)

df_voto_deputado['nom_voto'] = df_voto_deputado['nom_voto'].str.upper().str.strip()

df_voto_deputado = df_voto_deputado.rename(columns={
    'dat_data_registro': 'dat_registro'
})

salva.save_parquet(df_voto_deputado.drop_duplicates(), 'fato_voto_deputado', 'gold')


# -------------------------------------
# FATO ORIENTACAO
# -------------------------------------
df_orientacao = dfs_silver['silver_orientacao']

# 🔹 seleciona só o necessário da silver
df_orientacao = df_orientacao[[
    'id_votacao',
    'nom_orientacao_voto',
    'id_tipo_lideranca',
    'nom_sigla_partido_bloco',
    'des_uri_partido_bloco',
    'data_extracao'
]]

# 🔹 padroniza sigla
df_orientacao['nom_sigla_partido_bloco'] = (
    df_orientacao['nom_sigla_partido_bloco']
    .str.upper()
    .str.strip()
)

# 🔹 dim partido bloco (somente colunas necessárias)
df_partido_bloco_fato = dim_partido_bloco[[
    'nom_sigla',
    'id_partido_bloco'
]]

# 🔹 merge limpo
df_orientacao = df_orientacao.merge(
    df_partido_bloco_fato,
    left_on='nom_sigla_partido_bloco',
    right_on='nom_sigla',
    how='left'
)

# 🔹 remove coluna auxiliar do merge
df_orientacao = df_orientacao.drop(columns=['nom_sigla_partido_bloco', 'nom_sigla'])

# 🔹 colunas finais da fato
cols_fato_orientacao = [
    'id_votacao',
    'nom_orientacao_voto',
    'id_partido_bloco',
    'data_extracao'
]

df_orientacao = df_orientacao[
    [col for col in cols_fato_orientacao if col in df_orientacao.columns]
]

# 🔹 salva
salva.save_parquet(df_orientacao, 'fato_orientacao', 'gold')


# -------------------------------------
# FATO PROPOSICAO
# -------------------------------------
df_proposicao = dfs_silver['silver_proposicao']

# 🔹 seleciona só colunas necessárias da proposição
df_proposicao = df_proposicao[[
    'id_proposicao',
    'nom_tipo_proposicao',
    'cod_tipo',
    'num_numero_prop',
    'num_ano',
    'nom_ementa',
    'dat_apresentacao',
    'nom_keywords',
    'nom_regime',
    'nom_tipo_tramitacao',
    'data_extracao'
]]

# 🔹 tema (já correto)
df_tema_fato = dfs_silver['silver_temas_proposicao'][[
    'id_proposicao',
    'cod_tema'
]]

# 🔹 autor (🔥 só o necessário)
df_autor_fato = dfs_silver['silver_autores'][[
    'id_proposicao',
    'id_autor'
]]

# 🔹 merges limpos
df_proposicao = df_proposicao.merge(df_tema_fato, on='id_proposicao', how='left')
df_proposicao = df_proposicao.merge(df_autor_fato, on='id_proposicao', how='left')

# 🔹 rename final (mantém padrão)
df_proposicao = df_proposicao.rename(columns={
    'nom_tipo_proposicao': 'tipo_proposicao',
    'num_numero_prop': 'num_proposicao',
    'nom_tipo_tramitacao': 'nom_tramitacao'
})

# 🔹 colunas finais da fato
cols_fato_proposicao = [
    'id_proposicao',
    'tipo_proposicao',
    'cod_tipo',
    'num_proposicao',
    'num_ano',
    'dat_apresentacao',
    'nom_regime',
    'nom_tramitacao',
    'id_autor',
    'cod_tema',
    'data_extracao'
]

df_proposicao = df_proposicao[[col for col in cols_fato_proposicao if col in df_proposicao.columns]]


salva.save_parquet(df_proposicao, 'fato_proposicao', 'gold')
salva.save_parquet(df_proposicao, 'fato_proposicao', 'gold')
print("\n📦 ESTRUTURA DAS TABELAS (DIM + FATO)")
print("=" * 60)

# -------------------
# DIMENSÕES
# -------------------
print("\n🔹 DIMENSÕES")
print("-" * 60)

print("dim_deputado:")
print(dim_deputado.columns.tolist())
print("-" * 40)

print("dim_partido:")
print(dim_partido.columns.tolist())
print("-" * 40)

print("dim_mandato:")
print(dim_mandato.columns.tolist())
print("-" * 40)

print("dim_partido_bloco:")
print(dim_partido_bloco.columns.tolist())
print("-" * 40)

print("dim_tema:")
print(dim_tema.columns.tolist())
print("-" * 40)

print("dim_autor:")
print(dim_autor.columns.tolist())
print("-" * 40)


# -------------------
# FATOS
# -------------------
print("\n🔸 FATOS")
print("-" * 60)

print("fato_voto_deputado:")
print(df_voto_deputado.columns.tolist())
print("-" * 40)

print("fato_orientacao:")
print(df_orientacao.columns.tolist())
print("-" * 40)

print("fato_proposicao:")
print(df_proposicao.columns.tolist())
print("-" * 40)

print("=" * 60)