import src.data_loader as dl
import src.cross_validation as cv
import src.telegram as telegram
import config.grid_search as gs
import pandas as pd
import os
import sys
from dotenv import load_dotenv

load_dotenv()

send_to_telegram = True
data_origin = 'sheet'

try:
    if send_to_telegram:
        telegram.send('{} START: Backtest'.format(telegram.emoji.play))

    # load Parameters
    SHEET_PATH = os.getenv('SHEET_PATH')
    PORTFOLIO_MAX_SIZE = gs.parameters.PORTFOLIO_MAX_SIZE
    DICKEY_FULLER = gs.parameters.DICKEY_FULLER
    FISHER = gs.parameters.FISHER
    MEIA_VIDA = gs.parameters.MEIA_VIDA
    MEDIA_N = gs.parameters.MEDIA_N
    DESVIO_PADRAO = gs.parameters.DESVIO_PADRAO
    PERIODO = gs.parameters.PERIODO
    VARIANCIA_BETA = gs.parameters.VARIANCIA_BETA
    DAGOSTINO_PERSON = gs.parameters.DAGOSTINO_PERSON

    #load data
    if data_origin == 'sheet':
        df = dl.sheet_importer(SHEET_PATH)
    elif data_origin == 'database':
        df = 'foo'

    # generate grid
    grid = cv.generate_grid(PORTFOLIO_MAX_SIZE, DICKEY_FULLER, FISHER, MEIA_VIDA,  MEDIA_N,  DESVIO_PADRAO, PERIODO, VARIANCIA_BETA)

    # Get grid search run info
    if send_to_telegram:
        telegram.send('{} RUN: Estimate Time to Complete'.format(telegram.emoji.hourglass))

    cv.grid_search_info(df, grid, parallel=True, send_to_telegram=send_to_telegram)

    # Run grid search
    if send_to_telegram:
        telegram.send('{} RUN: Grid Search'.format(telegram.emoji.hourglass))

    results = cv.grid_search(df, grid, parallel=True, verbose=True, send_to_telegram=send_to_telegram)


    # save results
    df_results = pd.DataFrame(results)
    df_results.to_pickle("./outputs/results.pkl")

    if send_to_telegram:
        telegram.send('{} END: Succcess'.format(telegram.emoji.check))

except:
    if send_to_telegram:
        telegram.send('{} END: Failure'.format(telegram.emoji.cross))
        telegram.send("{} ERROR: {}".format(telegram.emoji.double_exclamation,sys.exc_info()))