import unittest
import main
import pandas as pd
import numpy as np
import io
import sys

'''
Тестировать все функции - бессмысленно, так как очень много "грязных" функций, которые работают на ввод
и вывод, за бизнес-логику отвечает лишь малая часть программы
'''

class Tests(unittest.TestCase):
    
    ind = pd.DatetimeIndex(['2017-01-01', '2017-01-02', '2017-01-03', '2017-01-04'])
    
    def setUp(self):
        main.pairs = ['btcusdt']
        #ind = pd.DatetimeIndex(['2017-01-01', '2017-01-02', '2017-01-03', '2017-01-04'])
        df = pd.DataFrame({'High':[2,3,4,5], 'Open': [1.5,2.5,3.5,4.5], 'Close':[1.75,2.75,3.75,4.75], 'Low':[1,2,3,4]}, index = self.ind)
        main.pairs_dfs = {main.pairs[0]:df}

    def test_count_mas(self):
        self.assertEqual(main.count_mas('btcusdt', 3).tolist()[3], 3.75)
        self.assertEqual(main.count_mas('btcusdt', 3).tolist()[2], 2.75)
        self.assertEqual(pd.isna(main.count_mas('btcusdt', 3).tolist()[0]), True)
        self.assertEqual(pd.isna(main.count_mas('btcusdt', 3).tolist()[1]), True)

    def test_print(self):
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     #  and redirect stdout.
        main.ma_log(3)                                     # Call function.
        sys.stdout = sys.__stdout__                     # Reset redirect.
        self.assertEqual(capturedOutput.getvalue(), 'Скользящие средние:\n\nПара btcusdt: [nan, nan, 2.75, 3.75]\n\n')

    def test_candles_eval(self):
        result = '{"e":"kline","E":0,"s":"BTCUSDT","k":{"t":1624894620000,"T":1624894679999,"s":"BTCUSDT","i":"1m","f":936941011,"L":936941261,"o":"0","c":"0","h":"0","l":"0","v":"7.65673400","n":251,"x":false,"q":"264338.26880285","V":"4.22223000","Q":"145773.05557859","B":"0"}}'
        #print (main.candles_eval(result))
        df1 = pd.DataFrame({'High':[2.0,3.0,4.0,5.0], 'Open': [1.5,2.5,3.5,4.5], 'Close':[1.75,2.75,3.75,4.75], 'Low':[1.0,2.0,3.0,4.0]}, index = self.ind)
        df2 = pd.DataFrame({'High':[0.0], 'Open': [0.0], 'Close':[0.0], 'Low':[0.0]}, index = pd.DatetimeIndex(['1970-01-01']))
        self.assertEqual(main.candles_eval(result).values.tolist(), pd.concat([df1, df2]).values.tolist())
        
if __name__ == '__main__':
    unittest.main()
