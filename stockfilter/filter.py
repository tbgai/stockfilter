# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:32:58 2019

@author: jingzl

stock filter algorithm method
"""
import numpy as np
import matplotlib.pyplot as plt
import xlrd
from stockfilter.parsestockdata import ParseStockData

class StockFilter():
    
    def __init__( self ):
        pass

    def filter( self ):
        
        # 
        
        
        
        
        
        parsedata = ParseStockData()
        parsedata.getStockBasicData()
        
        
        print("stock filter")

    # 生成斜率因子
    def createFactor( ls ):
        factorls = []
        size = len(ls)
        i = 0
        for item in ls:
            if i == size-1:
                break;
            # ***
            factor = (ls[i+1]-ls[i])
            factorls.append( factor )
            i = i+1
        return factorls

# 对单个股票数据进行过滤
def filterStock():
    pass

# 对所有股票进行过滤
def filterAllStock():
    pass

# 生成斜率因子
def createFactor( ls ):
    factorls = []
    size = len(ls)
    i = 0;
    for item in ls:
        if i == size-1:
            break;
        # ***
        factor = (ls[i+1]-ls[i])
        factorls.append( factor )
        i = i+1
    return factorls
    

# 读取股票参数基准配置
def parseConfig( fname ):
    ls = np.loadtxt( fname, dtype=np.float, delimiter=',' )
    #print( ls )
    # 生成曲线
    #plt.plot( ls )
    #plt.savefig( 'base', dpi=600 )
    #plt.close()
    # 创建斜率因子
    # 两次求斜率
    fls = createFactor( ls )
    #print( fls )
    return createFactor( fls )

# 斜率因子比较
def compareFactor( basefls, fls ):
    if len(basefls) != len(fls):
        return False
    count = 0
    for i in range(len(basefls)):
        if abs(basefls[i]-fls[i]) < 1.2:
            count = count + 1
    if count == len(basefls):
        return True
    else:
        return False

# 读取待过滤的股票数据 过滤比较
def stockFilter( fname, factorls ):
    ilen = len( factorls )
    #print( ilen )
    data = xlrd.open_workbook( fname )
    # 目前只有一张表
    table = data.sheet_by_index(0)
    datels = table.col_values(0)
    stockdatals = table.col_values(4)
    # 0 为表头，删除
    del datels[0]
    del stockdatals[0]
    #print( datels )
    #print( stockdatals )
    sdatels = []
    for i in range(len(stockdatals)):
        # 取n个值，计算斜率因子
        if ( i+ilen+1 > len(stockdatals) ):
            break
        ls = stockdatals[i:i+ilen+2]
        # 两次求斜率
        flstmp = createFactor( ls )
        fls = createFactor( flstmp )
        #print( len(fls) )
        #print( fls )
        # 与基准斜率因子比较
        if compareFactor( factorls, fls ):
            sdatels.append( datels[i] )
            #plt.plot( ls )
            plt.plot( fls )
            plt.savefig( datels[i], dpi=600 )
            #plt.close()

    return sdatels

