import itertools
import multiprocessing as mp
import src.back_test as bt
import src.telegram as telegram
import pandas as pd
import math
import time

results = []

def generate_grid(portfolio_max_size, dickey_fuller, fisher, meia_vida,  media_n,  desvio_padrao, periodo, variancia_beta):

    grid = list(itertools.product(portfolio_max_size, dickey_fuller, fisher, meia_vida, media_n, desvio_padrao, periodo, variancia_beta))

    return grid


def grid_search_info(dataframe, grid, parallel = False, send_to_telegram = False):

    df = dataframe
    threads = 1

    if parallel == True:
        threads = mp.cpu_count()

        start_time = time.time()

        res = grid_search(df, grid[:threads], parallel=True)

        tempo_trade = time.time() - start_time

    else:
        parametros = grid[0]

        start_time = time.time()

        bt.back_test(parametros, df, df.data.min(), df.data.max())

        tempo_trade = time.time() - start_time

    df_results = pd.DataFrame(res)
    memoria_gb = (df_results.memory_usage(deep=True).sum() / 10 ** 9) * (len(grid)/threads)
    tempo_iteracao = round(tempo_trade, 2)
    tempo_segundos = (len(grid)/threads) * tempo_trade
    tempo_horas = round(tempo_segundos / (60 * 60), 2)
    tempo_dias = round(tempo_segundos / (60 * 60 * 24), 2)

    print('Total de iterações: {}'.format(len(grid)))
    print('Uso de memória: {} Gb'.format(memoria_gb))
    print('-------------------------')
    print('Quantidade de iterações em um ciclo: {}'.format(threads))
    print('Tempo de um ciclo: {} segundos'.format(tempo_iteracao))
    print('-------------------------')
    print('Tempo previsto da busca: {} horas'.format(tempo_horas))
    print('Tempo previsto da busca: {} dias'.format(tempo_dias))
    print('-------------------------')

    if send_to_telegram:
        telegram.send('Total de iterações: {}'.format(len(grid)))
        telegram.send('Uso de memória: {} Gb'.format(memoria_gb))
        telegram.send('-------------------------')
        telegram.send('Quantidade de iterações em um ciclo: {}'.format(threads))
        telegram.send('Tempo de um ciclo: {} segundos'.format(tempo_iteracao))
        telegram.send('-------------------------')
        telegram.send('Tempo previsto da busca: {} horas'.format(tempo_horas))
        telegram.send('Tempo previsto da busca: {} dias'.format(tempo_dias))
        telegram.send('-------------------------')



def collect_result(result):
    '''Define callback function to collect the output in `results` '''
    global results
    results.append(result)


def grid_search(dataframe, grid, parallel = True, verbose = False, send_to_telegram = False):

    # limpa os resultados
    global results
    results = []

    df = dataframe

    # calcula as posicoes para printar
    threads = mp.cpu_count()
    grid_size = len(grid)
    ciclos = math.ceil(grid_size / threads)
    cortes = 10 # número de cortes para printar log
    step = 1 if ciclos < cortes else round(ciclos / cortes)
    print_i = [round(threads * i, 0) for i in range(0, ciclos, step)]


    start_time = time.time()

    if verbose:
        print('--- Inicio do Grid Search ---')
        if send_to_telegram:
            telegram.send('--- Inicio do Grid Search ---')


    if parallel:

        pool = mp.Pool(mp.cpu_count())

        for i, parametros in enumerate(grid):
            pool.apply_async(bt.back_test_async, args=(i, parametros, df, df.data.min(), df.data.max()),
                             callback=collect_result)

            # loga a evolucao
            if i in print_i:
                if verbose:
                    print('{}%'.format(round(i / grid_size * 100, 1)))
                    if send_to_telegram:
                        telegram.send('{}%'.format(round(i/grid_size*100,1)))

        # Step 4: Close Pool and let all the processes complete
        pool.close()
        pool.join()  # postpones the execution of next line of code until all processes in the queue are done.

    else:
        pass

    tempo_execucao = round(time.time() - start_time, 2)

    if verbose:
        print('--- Fim do Grid Search ---')
        print('Total de iterações realizadas: {}'.format(grid_size))
        print('Tempo de execução: {} segundos'.format(tempo_execucao))
        if send_to_telegram:
            telegram.send('--- Fim do Grid Search ---')
            telegram.send('Total de iterações realizadas: {}'.format(grid_size))
            telegram.send('Tempo de execução: {} segundos'.format(tempo_execucao))

    return(results)