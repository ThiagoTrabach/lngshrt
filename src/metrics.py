
def metric_mdd(dataframe, dotacao_inicial):

    df = dataframe
    resultado_acumulado = df.resultado.cumsum() + dotacao_inicial
    mdd = 0
    pico = resultado_acumulado.iloc[0]

    for i in resultado_acumulado:
        if i > pico:
            pico = i
        dd = (pico - i) / pico

        if dd > mdd:
            mdd = dd

    return round(mdd, 3)


def get_metrics(dataframe, dotacao_inicial):

    df = dataframe
    n_operacoes = df.shape[0]

    retorno = df.resultado.sum()

    win_rate = round(sum(df.resultado > 0) / df.shape[0], 2)

    pay_off = round(abs(df.resultado[df.resultado > 0].mean() / df.resultado[df.resultado < 0].mean()), 3)

    mdd = metric_mdd(df, dotacao_inicial)

    recovery_factor = round(abs(df.resultado[df.resultado > 0].sum() / df.resultado[df.resultado < 0].sum()), 3)

    return ({'n_operacoes': n_operacoes,
             'retorno': retorno,
             'win_rate': win_rate,
             'pay_off': pay_off,
             'mdd': mdd,
             'recovery_factor': recovery_factor})