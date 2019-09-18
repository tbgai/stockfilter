# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:40:42 2019

@author: jingzl

parse stock data from tushare interface
"""
import tushare as ts

TUSHARE_TOKEN = '8af63d3d7f7ec3bc0e511a85b13d0cf01c57dd310bc1f8ed4b902ad3'

class ParseStockData( object ):
    
    def __init__( self ):
        pass
    
    def getStockData( self ):
        
        # 获取所有的股票列表信息
        pro = ts.pro_api( token=TUSHARE_TOKEN )
        # 查询当前所有正常上市交易的股票列表
        data = pro.query( 'stock_basic', exchange='', list_status='L', 
                         fields='ts_code, symbol, name')
        #print( data )
        #print( data.ix[0:3] )
        #print( data.columns )
        #print( data.ix[ 0:3, 1 ] )
        
        dl = data.ix[ 0:3, 1 ].values
        print( dl[1] )
        
        
        df = pro.query( 'daily', ts_code='000001.SZ', start_date='20190818',
                       end_date='20190918', fields='trade_date,close')
        #print( df )
        dl2 = df.ix[:,1].values
        print( dl2 )
        print( dl2[2] )
        



# 获取所有股票信息
def getAllStockData():
    pass



