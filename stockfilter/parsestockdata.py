# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:40:42 2019

@author: jingzl

parse stock data from tushare interface
"""
import tushare as ts

class ParseStockData( object ):
    
    def __init__( self ):
        pass
    
    def getStockData( self ):
        # tushare的股票数据获取
        print(ts.get_hist_data('600848',start='2019-08-29',end='2019-08-30'))
        #print("parse stock data")



# 获取所有股票信息
def getAllStockData():
    pass



