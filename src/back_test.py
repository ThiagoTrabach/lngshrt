import src.trade as trade
import src.metrics as metrics


def back_test(parametros, df, data_inicio, data_final):

    param = {'portfolio_max_size': parametros[0],
             'dickey-fuller': parametros[1],
             'fisher': parametros[2],
             'meia-vida': parametros[3],
             'media_n': parametros[4],
             'desvio-padrao': parametros[5],
             'periodo': parametros[6],
             'variancia_beta': parametros[7],
             'prop_financeiro': parametros[8],
             'dagostino-person': 0.05}

    df_filtered = trade.filter_dataframe(df, param)

    operacoes = trade.run_trades(df_filtered, data_inicio, data_final, param['portfolio_max_size'])

    return operacoes, param



def back_test_async(i, parametros, df, data_inicio, data_final):

    operacoes, param = back_test(parametros, df, data_inicio, data_final)
    results = metrics.get_metrics(operacoes, parametros[0] * 25000)

    output = {'iteracao': i}
    output.update(param)
    output.update(results)

    return output

