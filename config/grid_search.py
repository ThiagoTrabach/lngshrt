import numpy as np

class parameters:
    PORTFOLIO_MAX_SIZE = np.arange(5,8,1)
    DICKEY_FULLER = np.arange(3,10,1)
    FISHER = np.arange(0,0.9,0.1)
    MEIA_VIDA = [10,25,70,100]
    MEDIA_N = np.arange(0.5, 3.5, 0.5)
    DESVIO_PADRAO = np.arange(2, 2.6, 0.1)
    PERIODO = [100,200]
    VARIANCIA_BETA = np.arange(0.01,1, 0.5)
    DAGOSTINO_PERSON = 0.05
    PROP_FINANCEIRO = np.arange(2, 6, 1)