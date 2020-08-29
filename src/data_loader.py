import pandas as pd


def sheet_importer(file_path):

    df = pd.read_excel(file_path)

    data_inicio = df.data.min()
    data_final = df.data.max()

    df = sheet_formatter(df)

    print('Intervalo do dataset: {} a {}'.format(data_inicio, data_final))
    print('Shape: {}'.format(df.shape))

    return(df)


def sheet_formatter(df):
    df['pares_invertidos'] = df.pares.apply(lambda x: x[-x.find('|'):] +'|' + x[:x.find('|')] )

    df = df[['data', 'pares', 'pares_invertidos', 'ativo_dep', 'ativo_ind', 'dickey-fuller', 'adf',
       'prop_financeiro', 'fisher', 'meia-vida', 'desvio-padrao', 'periodo',
       'ok', 'vol_financ', 'manter', 'variancia_beta', 'dagostino-person',
       'media_n', 'data_saida', 'in_dep', 'in', 'in.1', 'out', 'out.1', 'res',
       'res.1', 'resultado']]


    return(df)