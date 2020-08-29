import src.data_loader as dl
import src.cross_validation as cv
import src.telegram as telegram
import numpy as np
import pandas as pd
import os
import sys
from dotenv import load_dotenv


load_dotenv()

portfolio_max_size = np.arange(2,4,1)
dickey_fuller = np.arange(3,4,1)
fisher = np.arange(-0.5,-0.4,0.1)
meia_vida = [10,25]
media_n = np.arange(0.5, 0.6, 0.1)
desvio_padrao = np.arange(2, 2.1, 0.1)
periodo = [100]
variancia_beta = np.arange(0.01, 0.12, 0.1)
dagostino_person = 0.05

send_to_telegram = False

try:
    # load Parameters
    SHEET_PATH = os.getenv('SHEET_PATH')

    if send_to_telegram:
        telegram.send('{} FASE: Inicio do Backtest'.format(telegram.emoji.play))


    #load data
    df = dl.sheet_importer(SHEET_PATH)

    # generate grid
    grid = cv.generate_grid(portfolio_max_size, dickey_fuller, fisher, meia_vida,  media_n,  desvio_padrao, periodo, variancia_beta)

    # Get grid search run info
    if send_to_telegram:
        telegram.send('{} FASE: Estimativa de execução'.format(telegram.emoji.hourglass))

    cv.grid_search_info(df, grid, parallel=True, send_to_telegram=send_to_telegram)

    # Run grid search
    if send_to_telegram:
        telegram.send('{} FASE: Execução da Busca'.format(telegram.emoji.hourglass))

    results = cv.grid_search(df, grid, parallel=True, verbose=True, send_to_telegram=send_to_telegram)


    # save results
    df_results = pd.DataFrame(results)
    df_results.to_pickle("./outputs/results.pkl")

    if send_to_telegram:
        telegram.send('{} FASE: Fim do Backtest!'.format(telegram.emoji.check))

except:
    telegram.send("{} ERROR: {}".format(telegram.emoji.double_exclamation,sys.exc_info()))