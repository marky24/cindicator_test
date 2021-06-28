from websocket import create_connection
import json
import multiprocessing
from threading import Thread
import time
import ast
from datetime import datetime
import streamlit as st
import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation
import os
from matplotlib import pyplot as plt
import configparser

pairs = ['btcusdt', 'ethusdt', 'bnbbtc']
pairs_dfs = {pair:pd.DataFrame(columns = ['High', "Open", 'Close', 'Low']) for pair in pairs}

def count_mas(pair, window):
    """
    Function that count rolling average for pair with window
    INPUT:
        pair(str)  - Name of cryptocurrencie pair
        window(int)- Window parameter for rolling average counting
    """
    windows = pairs_dfs[pair]['Close'].rolling(window)
    ma = windows.mean()
    return ma

def ma_log(window):
    """
    Procedure that print logs to console with rolling average info
    INPUT:
        window(int)- Window parameter for rolling average counting
    """
    print ("Скользящие средние:")
    print ()
    for pair in pairs_dfs:
        print ("Пара {}: {}".format(pair, count_mas(pair, window).tolist()))
        print ()

def logs(window):
    """
    Procedure that print logs to console
    INPUT:
        window(int)- Window parameter for rolling average counting
    """
    clear = lambda: os.system('clear')
    clear()
    ma_log(window)
        
def candles_eval(result):
    """
    Procedure that parse api result to dict pairs_dfs 
    INPUT:
        result(str)- web socket response for charts request
    """
    result = json.loads(result)
    pair = result['s'].lower()
    x = result['E']
    x = datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S')
    open =  float(result['k']['o'])
    high =  float(result['k']['h'])
    low =   float(result['k']['l'])
    close = float(result['k']['c'])
    
    pairs_dfs[pair] = pd.concat([pairs_dfs[pair], \
                                pd.DataFrame([[high,open,close,low]], \
                                             index = [pd.to_datetime(x)], \
                                             columns = ['High', "Open", 'Close', 'Low'])])
    return pairs_dfs[pair] #Return just for testing
    
def web_socket_work():
    """
    Procedure that parse api results to dict pairs_dfs 
    """
    ws = create_connection("wss://stream.binance.com:9443/ws")
    ws.send(json.dumps({"method": "SUBSCRIBE","params": \
                        list(map(lambda x: x+'@kline_1m', pairs)),"id": 1}))
    time.sleep(2)
    result = ws.recv()
    time.sleep(2)
    while True:
        result = ws.recv()
        #print (result)
        candles_eval(result)
    ws.close()

def plotting(window):
    '''
    Procedure that plot candel charts and moving averages on them
    INPUT:
        window(int)- Window parameter for rolling average counting
    '''
    pair_ax = {pair:None for pair in pairs_dfs}
    def animate(ival):
        ax_list = fig.axes
        for pair in pairs_dfs:
            data = pairs_dfs[pair]
            ax_ =  pair_ax[pair]
            mpf.plot(data, ax=ax_, type='candle', mav=window)
            plt.pause(0.1)
            plt.draw()
            plt.pause(0.1)

    fig = mpf.figure(style='charles',figsize=(20,10))
    index_ = 1
    for pair in pairs_dfs:
        ax1 = fig.add_subplot(2,2,index_)
        pair_ax[pair] = ax1
        index_ = index_ + 1
    ani = animation.FuncAnimation(fig, animate, interval=250)
    plt.show()   
    
def parameters_load():
    """
    Function that choose method of parameters load
    RETURN
        IsConsole(bool) True, if chose console input, false, if config input
    """
    while True:
        print ("Введете необходимые параметры для работы программы с консоли или из конфиг файла?")
        print ("Введите 1 для консоли и 2 для конфиг файла")
        IsConsole = int(input())
        if IsConsole == 1:
            IsConsole = True
        elif IsConsole == 2:
            IsConsole = False
        else:
            print ('Вы ввели что-то не то')
            continue
        return IsConsole

def greetings():
    print ('Программа запущена...')

def console_input():
    """
    Function that choose method of parameters load
    RETURN
        IsConsole(bool) True, if chose console input, false, if config input
    """
    print ('Выберите ширину окна скользящего среднего')
    ma_window = int(input())
    print ('Надо ли помимо логов выводить график свечек и скользящего среднего? (Да/Нет)')
    IsPlotNeedStr = str(input())
    IsPlotNeed = False
    if IsPlotNeedStr.lower() == 'да':
        IsPlotNeed = True
    elif IsPlotNeedStr.lower() == 'нет':
        IsPlotNeed = False
    else:
        print ('Вы ввели что-то не то')
        main()
    return ma_window, IsPlotNeed

def config_input():
    """
    Function that read data from config and return it
    RETURN:
        window(int) - window size for rolling average computation
        IsPlotNeed(bool) - True if you need plotting and False if you dont need it
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return int(config['window']['value']), bool(config['IsPlotNeed']['value'])

def log_for_thread(window):
    '''
    Dummy procedure for correct multithreading work
    '''
    while True:
        logs(window)
        time.sleep(1)

def start ():
    '''
    Function that prepare all data for algorithm work
    Return:
        window(int) - window size for rolling average computation
        IsPlotNeed(bool) - True if you need plotting and False if you dont need it
    '''
    greetings()
    IsConsole = parameters_load()
    IsPlotNeed = False
    if IsConsole:
        window, IsPlotNeed = console_input()
    if not IsConsole:
        window, IsPlotNeed = config_input()
    return window, IsPlotNeed

def main():
    '''
    Main function
    '''
    window, IsPlotNeed = start()
    t = Thread(target = web_socket_work, daemon = True)
    t.start()
    time.sleep(6)
    logThread = Thread(target = log_for_thread, args = (window,), daemon = True)
    logThread.start()
    time.sleep(6)
    if (IsPlotNeed):
        plotting(window)
    while True:
        continue
        
if __name__ =="__main__":
    main()
