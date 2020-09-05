import numpy as np

class parameters:
    PORTFOLIO_MAX_SIZE = np.arange(2,4,1)
    DICKEY_FULLER = np.arange(3,4,1)
    FISHER = np.arange(-0.5,-0.4,0.1)
    MEIA_VIDA = [10,25]
    MEDIA_N = np.arange(0.5, 0.6, 0.1)
    DESVIO_PADRAO = np.arange(2, 2.1, 0.1)
    PERIODO = [100]
    VARIANCIA_BETA = np.arange(0.01, 0.12, 0.1)
    DAGOSTINO_PERSON = 0.05