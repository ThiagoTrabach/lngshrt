import pandas as pd


def filter_dataframe(dataframe, parameters):
    df = dataframe

    param = parameters

    c1 = df['dickey-fuller'] >= param['dickey-fuller']
    c2 = df['fisher'] >= param['fisher']
    c3 = df['meia-vida'] <= param['meia-vida']
    c4 = df['media_n'].between(-param['media_n'], param['media_n'])
    c5 = (df['desvio-padrao'] <= - param['desvio-padrao']) | (df['desvio-padrao'] >= param['desvio-padrao'])
    c6 = df['periodo'] >= param['periodo']
    c7 = df['variancia_beta'] <= param['variancia_beta']
    c8 = df['dagostino-person'] >= param['dagostino-person']

    df_filtered = df[c1 & c2 & c3 & c4 & c5 & c6 & c7 & c7]

    return df_filtered


def run_trades(dataframe, data_inicial, data_final, portfolio_max_size):
    # Parametros de inicializacao
    df = dataframe
    data = data_inicial

    portfolio = pd.DataFrame(data=None, columns=df.columns)

    operacoes = pd.DataFrame(data=None, columns=df.columns)

    # itera diariamente
    while data <= data_final:
        #####
        # SAIDA
        #####
        ativos_saindo = portfolio[portfolio['data_saida'] == data]
        ativos_saindo_index = set(ativos_saindo.index)

        # remove do portfolio
        portfolio_index = set(portfolio.index)
        portfolio = portfolio.loc[list(portfolio_index - ativos_saindo_index)]

        # registra as operacoes concluidas
        operacoes = operacoes.append(ativos_saindo)

        ####
        # ENTRADA
        ####
        # carrega todos ativos entrantes
        ativos_entrantes = df[df.data == data]

        # filtrar os pares não validos
        portfolio_pares = set(portfolio.pares_invertidos).union(set(portfolio.pares))

        ativos_entrantes_pares = set(ativos_entrantes.pares)

        ativos_entrantes = ativos_entrantes[ativos_entrantes.pares.isin(list(ativos_entrantes_pares - portfolio_pares))]

        # ordena os ativos elegíveis
        # TODO: segundo nível do sort
        ativos_entrantes = ativos_entrantes.sort_values(by=['dickey-fuller'], ascending=False)

        # filtra de acordo com o tamanho maximo da carteira
        portfolio_slotes_disponiveis = portfolio_max_size - portfolio.shape[0]

        portfolio_slotes_disponiveis = portfolio_slotes_disponiveis if portfolio_slotes_disponiveis > 0 else 0

        ativos_entrantes = ativos_entrantes[:portfolio_slotes_disponiveis]

        # grava o novo portfolio
        portfolio = portfolio.append(ativos_entrantes)

        data += pd.DateOffset(1)

    return operacoes




