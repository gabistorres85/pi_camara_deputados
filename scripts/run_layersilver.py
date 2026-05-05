from camara_deputados.ingestion.data_loader import DataLoader
from camara_deputados.extraction.write import DataWrite
from camara_deputados.transformer.transformer import DataTransformer

bronze = DataLoader('bronze')
salva = DataWrite()
transformer = DataTransformer()


def criar_silver_deputado(dfs_bronze):
    df = dfs_bronze['deputado_detalhamento']
    mapping = {
        'id': ('id_mandato', 'int'),
        'nomeCivil': ('nome', 'str'),
        'sexo': ('sexo', 'str'),
        'dataNascimento': ('dat_nasc', 'date'),
        'dataFalecimento': ('dat_falecimento', 'date'),
        'ufNascimento': ('uf_nasc', 'str'),
        'municipioNascimento': ('municipio_nasc', 'str'),
        'escolaridade': ('nom_escolaridade', 'str'),
        'ultimoStatus.siglaPartido': ('nom_sigla_partido', 'str'),
        'ultimoStatus.siglaUf': ('nom_uf_representa', 'str'),
        'ultimoStatus.idLegislatura': ('id_legislatura', 'int'),
        'ultimoStatus.email': ('nom_email', 'str'),
        'ultimoStatus.nomeEleitoral': ('nom_nome_eleitoral', 'str'),
        'ultimoStatus.situacao': ('nom_situacao', 'str'),
        'ultimoStatus.condicaoEleitoral': ('nom_condicao_eleitoral', 'str'),
        'source_id': ('id_deputado', 'int'),
    }
    df = transformer.rename_and_cast(df, mapping)
    salva.save_parquet(df, 'silver_deputado', 'silver')
    return df


def criar_silver_frente_deputado(dfs_bronze):
    df = dfs_bronze['deputado_frentes']
    mapping = {
        'id': ('id_frente', 'int'),
        'titulo': ('nom_titulo', 'str'),
        'idLegislatura': ('id_legislatura', 'int'),
        'source_id': ('id_deputado', 'int'),
    }
    df = transformer.rename_and_cast(df, mapping)
    salva.save_parquet(df, 'silver_frente_deputado', 'silver')
    return df


def criar_silver_proposicao(dfs_bronze):
    df = dfs_bronze['proposicoes_detalhamento']
    mapping = {
        'id': ('id_proposicao', 'int'),
        'siglaTipo': ('nom_tipo_proposicao', 'str'),
        'codTipo': ('cod_tipo', 'int'),
        'numero': ('num_numero_prop', 'int'),
        'ano': ('num_ano', 'int'),
        'ementa': ('nom_ementa', 'str'),
        'dataApresentacao': ('dat_apresentacao', 'date'),
        'uriAutores': ('uri_autor', 'str'),
        'keywords': ('nom_keywords', 'str'),
        'statusProposicao.siglaOrgao': ('nom_sigla_orgao', 'str'),
        'statusProposicao.uriUltimoRelator': ('uri_relator', 'str'),
        'statusProposicao.regime': ('nom_regime', 'str'),
        'statusProposicao.descricaoTramitacao': ('nom_tipo_tramitacao', 'str'),
        'statusProposicao.codTipoTramitacao': ('cod_tipo_tramitacao', 'int'),
        'statusProposicao.descricaoSituacao': ('cod_tipo_situacao', 'str'),
        'statusProposicao.codSituacao': ('cod_situacao', 'int'),
        'statusProposicao.url': ('nom_link_proposicao', 'str'),
    }
    df = transformer.rename_and_cast(df, mapping)

    uri_map = {
        'uri_autor': ('nom_tipo_autor', 'id_autor'),
        'uri_relator': ('nom_tipo_relator', 'id_relator'),
    }
    df = transformer.extrair_tipos_e_ids(df, uri_map)
    salva.save_parquet(df, 'silver_proposicao', 'silver')
    return df


def criar_silver_autores(dfs_bronze):
    df = dfs_bronze['proposicoes_autores']
    mapping = {
        'uri': ('uri_autor', 'str'),
        'nome': ('nom_autor', 'str'),
        'codTipo': ('cod_tipo_autor', 'int'),
        'tipo': ('nom_tipo_autor', 'str'),
        'ordemAssinatura': ('num_ordem_assinatura', 'int'),
        'proponente': ('ind_proponente', 'str'),
        'source_id': ('id_proposicao', 'int'),
        'data_extracao': ('dat_extracao', 'date'),
    }
    df = transformer.rename_and_cast(df, mapping)

    df = transformer.extrair_tipos_e_ids(
        df,
        {'uri_autor': ('nom_tipo_autor', 'id_autor')}
    )
    salva.save_parquet(df, 'silver_autores', 'silver')
    return df


def criar_silver_temas_proposicao(dfs_bronze):
    df = dfs_bronze['proposicoes_temas']
    mapping = {
        'codTema': ('cod_tema', 'int'),
        'tema': ('nom_tema', 'str'),
        'relevancia': ('num_relevancia', 'int'),
        'source_id': ('id_proposicao', 'int'),
        'data_extracao': ('dat_extracao', 'date'),
    }
    df = transformer.rename_and_cast(df, mapping)
    salva.save_parquet(df, 'silver_temas_proposicao', 'silver')
    return df


def criar_silver_votacao_proposicao(dfs_bronze):
    df = dfs_bronze['proposicoes_votacoes']
    mapping = {
        'id': ('id_votacao', 'str'),
        'data': ('dat_data_votacao', 'date'),
        'dataHoraRegistro': ('dat_data_registro', 'date'),
        'uriOrgao': ('uri_orgao', 'str'),
        'descricao': ('nom_descricao', 'str'),
        'aprovacao': ('ind_aprovado', 'str'),
        'source_id': ('id_proposicao', 'int'),
    }
    df = transformer.rename_and_cast(df, mapping)
    df = transformer.extrair_ids(df, {'uri_orgao': 'id_orgao'})
    salva.save_parquet(df, 'silver_votacao_proposicao', 'silver')
    return df


def criar_silver_votacoes_detalhamento(dfs_bronze):
    df = dfs_bronze['votacoes_detalhamento']
    mapping = {
        'id': ('id_votacao', 'str'),
        'data': ('dat_data_votacao', 'date'),
        'dataHoraRegistro': ('dat_data_hora_registro', 'date'),
        'siglaOrgao': ('nom_sigla_orgao', 'str'),
        'idOrgao': ('id_orgao', 'int'),
        'idEvento': ('id_evento', 'int'),
        'descricao': ('des_descricao_votacao', 'str'),
        'aprovacao': ('ind_aprovacao', 'str'),
        'descUltimaAberturaVotacao': ('des_ultima_abertura', 'str'),
        'dataHoraUltimaAberturaVotacao': ('dat_ultima_abertura', 'date'),
        'efeitosRegistrados': ('des_efeitos', 'str'),
        'objetosPossiveis': ('des_objetos', 'str'),
        'ultimaApresentacaoProposicao.dataHoraRegistro': ('dat_ultima_apresentacao', 'date'),
        'ultimaApresentacaoProposicao.descricao': ('des_ultima_apresentacao_desc', 'str'),
        'ultimaApresentacaoProposicao.uriProposicaoCitada': ('des_uri_proposicao', 'str'),
    }
    df = transformer.rename_and_cast(df, mapping)
    salva.save_parquet(df, 'silver_votacoes_detalhamento', 'silver')
    return df


def criar_silver_orientacao(dfs_bronze):
    df = dfs_bronze['votacoes_orientacao']
    mapping = {
        'orientacaoVoto': ('nom_orientacao_voto', 'str'),
        'codTipoLideranca': ('id_tipo_lideranca', 'int'),
        'siglaPartidoBloco': ('nom_sigla_partido_bloco', 'str'),
        'codPartidoBloco': ('id_partido_bloco', 'int'),
        'uriPartidoBloco': ('des_uri_partido_bloco', 'str'),
        'source_id': ('id_votacao', 'str'),
        'data_extracao': ('dat_extracao', 'date'),
    }
    df = transformer.rename_and_cast(df, mapping)
    salva.save_parquet(df, 'silver_orientacao', 'silver')
    return df


def criar_silver_votos_deputados(dfs_bronze):
    df = dfs_bronze['votos_deputados']
    mapping = {
        'tipoVoto': ('nom_voto', 'str'),
        'dataRegistroVoto': ('dat_data_registro', 'date'),
        'deputado_.id': ('id_deputado', 'int'),
        'source_id': ('id_votacao', 'str'),
    }
    df = transformer.rename_and_cast(df, mapping)
    salva.save_parquet(df, 'silver_votos_deputados', 'silver')
    return df


def validar_autores_deputados(df_s_autores, df_s_deputado):
    if 'id_autor' not in df_s_autores.columns:
        raise ValueError('silver_autores não contém id_autor')
    if 'id_deputado' not in df_s_deputado.columns:
        raise ValueError('silver_deputado não contém id_deputado')

    autores_sao_deputados = df_s_autores['id_autor'].isin(df_s_deputado['id_deputado'])
    print("Autores que também são deputados:", autores_sao_deputados.sum())
    print("Autores que não são deputados:", (~autores_sao_deputados).sum())


def main():
    dfs_bronze = bronze.carregar_parquets()

    df_s_deputado = criar_silver_deputado(dfs_bronze)
    criar_silver_frente_deputado(dfs_bronze)
    criar_silver_proposicao(dfs_bronze)
    df_s_autores = criar_silver_autores(dfs_bronze)
    criar_silver_temas_proposicao(dfs_bronze)
    criar_silver_votacao_proposicao(dfs_bronze)
    criar_silver_votacoes_detalhamento(dfs_bronze)
    criar_silver_orientacao(dfs_bronze)
    criar_silver_votos_deputados(dfs_bronze)

    validar_autores_deputados(df_s_autores, df_s_deputado)


if __name__ == '__main__':
    main()