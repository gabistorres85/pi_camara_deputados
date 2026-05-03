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

# -------------------------------------
# DIM DEPUTADO
# -------------------------------------
df_deputado = dfs_silver['silver_deputado']

mapping_deputado = {
    'id_Deputado': ('id_deputado', 'int'),
    'nom_NomeCivil': ('nome', 'str'),
    'nom_Sexo': ('sexo', 'str'),
    'dat_DataNasc': ('dat_nasc', 'date'),
    'dat_DataFalecimento': ('dat_falecimento', 'date'),
    'nom_UFNasc': ('uf_nasc', 'str'),
    'nom_MunicipioNasci': ('municipio_nasc', 'str')
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
mapping_partido = {'nom_SiglaPartido': ('sigla_partido', 'str')}

dim_partido = transformer.rename_and_cast(df_deputado, mapping_partido)

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
mapping_mandato = {
    'id_Mandato': ('id_mandato', 'int'),
    'nom_SiglaPartido': ('sigla_partido', 'str'),
    'nom_UFRepresenta': ('uf_representante', 'str'),
    'id_legislatura': ('id_legislatura', 'int'),
    'id_Deputado': ('id_deputado', 'int')
}

dim_mandato = transformer.rename_and_cast(df_deputado, mapping_mandato)

dim_mandato = dim_mandato.merge(dim_partido, on='sigla_partido', how='left')

dim_mandato = modeling.criar_dim(
    df=dim_mandato,
    colunas=[v[0] for v in mapping_mandato.values()] + ['id_partido'],
    chave_duplicidade=['id_mandato']
)

salva.save_parquet(dim_mandato, 'dim_mandato', 'gold')

# -------------------------------------
# DIM PROPOSICAO
# -------------------------------------
df_proposicao = dfs_silver['silver_proposicao']

mapping_proposicao = {
    "id_Proposicao": ('id_proposicao', 'int'),
    "cod_Tipo": ('cod_tipo', 'str'),
    "nom_TipoProposicao": ('tipo_proposicao', 'str'),
    "num_NumeroProp": ('num_proposicao', 'int'),
    "num_Ano": ('num_ano', 'int'),
    "nom_Ementa": ('nom_ementa', 'str'),
    "nom_regime": ('nom_regime', 'str'),
    "dat_Apresentacao": ('dat_apresentacao', 'date')
}

dim_proposicao = transformer.rename_and_cast(df_proposicao, mapping_proposicao)

dim_proposicao = modeling.criar_dim(
    df=dim_proposicao,
    colunas=[v[0] for v in mapping_proposicao.values()],
    chave_duplicidade=['id_proposicao']
)

salva.save_parquet(dim_proposicao, 'dim_proposicao', 'gold')

# -------------------------------------
# DIM PARTIDO BLOCO
# -------------------------------------
df_pb = dfs_silver['silver_orientacao'][[
    'id_PartidoBloco',
    'nom_SiglaPartidoBloco'
]].drop_duplicates()

df_pb = df_pb.rename(columns={
    'id_PartidoBloco': 'id_partido_bloco',
    'nom_SiglaPartidoBloco': 'nom_sigla'
})

dim_pb = modeling.criar_dim(
    df_pb,
    colunas=['id_partido_bloco', 'nom_sigla']
)

salva.save_parquet(dim_pb, 'dim_partido_bloco', 'gold')

# -------------------------------------
# FATO VOTACAO
# -------------------------------------
df_votacao = dfs_silver['silver_votacao_proposicao']

df_votacao['ind_Aprovado'] = df_votacao['ind_Aprovado'].map({
    'Sim': 1,
    'Não': 0
})

mapping_votacao = {
    "id_Votacao": ("id_votacao", "str"),
    "id_Orgao": ("id_orgao", "int"),
    "id_Proposicao": ("id_proposicao", "int"),
    "dat_DataVotacao": ("dat_votacao", "date"),
    "dat_DataRegistro": ("dat_registro", "date"),
    "nom_Descricao": ("nom_descricao", "str"),
    "ind_Aprovado": ("ind_aprovado", "int"),
}

fato_votacao = transformer.rename_and_cast(df_votacao, mapping_votacao)

fato_votacao = fato_votacao.drop_duplicates()

salva.save_parquet(fato_votacao, 'fato_votacao', 'gold')

# -------------------------------------
# FATO VOTO DEPUTADO
# -------------------------------------
df_voto_deputado = dfs_silver['silver_votos_deputados']

df_voto_deputado['nom_Voto'] = df_voto_deputado['nom_Voto'].str.upper()

mapping_voto_deputado = {
    "id_Votacao": ("id_votacao", "str"),
    "id_Deputado": ("id_deputado", "int"),
    "nom_Voto": ("nom_voto", "str"),
    "dat_DataRegistro": ("dat_registro", "date"),
}

fato_voto_deputado = transformer.rename_and_cast(
    df_voto_deputado,
    mapping_voto_deputado
)

fato_voto_deputado = fato_voto_deputado.drop_duplicates()

salva.save_parquet(
    fato_voto_deputado,
    'fato_voto_deputado',
    'gold'
)

# -------------------------------------
# FATO ORIENTACAO
# -------------------------------------
df_orientacao = dfs_silver['silver_orientacao']

mapping_orientacao = {
    "id_Votacao": ("id_votacao", "str"),
    "id_PartidoBloco": ("id_partido_bloco", "int"),
    "nom_OrientacaoVoto": ("nom_orientacao", "str"),
}

fato_orientacao = transformer.rename_and_cast(
    df_orientacao,
    mapping_orientacao
)

fato_orientacao = fato_orientacao.merge(
    dim_pb,
    on='id_partido_bloco',
    how='left'
)

salva.save_parquet(
    fato_orientacao,
    'fato_orientacao',
    'gold'
)

# -------------------------------------
# VALIDAÇÕES
# -------------------------------------
print("🔍 VALIDAÇÕES")

print("Votos sem votação:",
      len(fato_voto_deputado[
          ~fato_voto_deputado['id_votacao'].isin(fato_votacao['id_votacao'])
      ]))

print("Orientações sem votação:",
      len(fato_orientacao[
          ~fato_orientacao['id_votacao'].isin(fato_votacao['id_votacao'])
      ]))