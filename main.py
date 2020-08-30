import src.data_loader as dl
import src.cross_validation as cv
import src.telegram as telegram
import numpy as np
import pandas as pd
import os
import sys
from dotenv import load_dotenv

load_dotenv()

send_to_telegram = True

try:
    if send_to_telegram:
        telegram.send('{} START: Backtest'.format(telegram.emoji.play))

    # load Parameters
    SHEET_PATH = os.getenv('SHEET_PATH')
    PORTFOLIO_MAX_SIZE = eval(os.getenv('PORTFOLIO_MAX_SIZE'))
    DICKEY_FULLER = eval(os.getenv('DICKEY_FULLER'))
    FISHER = eval(os.getenv('FISHER'))
    MEIA_VIDA = eval(os.getenv('MEIA_VIDA'))
    MEDIA_N = eval(os.getenv('MEDIA_N'))
    DESVIO_PADRAO = eval(os.getenv('DESVIO_PADRAO'))
    PERIODO = eval(os.getenv('PERIODO'))
    VARIANCIA_BETA = eval(os.getenv('VARIANCIA_BETA'))
    DAGOSTINO_PERSON = eval(os.getenv('DAGOSTINO_PERSON'))

    #load data
    df = dl.sheet_importer(SHEET_PATH)

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
    telegram.send('{} END: Failure'.format(telegram.emoji.cross))
    telegram.send("{} ERROR: {}".format(telegram.emoji.double_exclamation,sys.exc_info()))