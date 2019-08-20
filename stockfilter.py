# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 16:47:39 2019

@author: jingzl
"""
import numpy as np
import matplotlib.pyplot as plt
import xlrd


# stockfilter.py
CONFIG_FNAME = 'config.txt'
FACTOR_FNAME = 'factor.txt'
STOCK_FNAME = 'stock.xlsx'

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
    plt.plot( ls )
    plt.savefig( 'base', dpi=600 )
    plt.close()
    # 创建斜率因子
    return createFactor( ls )

# 斜率因子比较
def compareFactor( basefls, fls ):
    if len(basefls) != len(fls):
        return False
    count = 0
    for i in range(len(basefls)):
        if abs(basefls[i]-fls[i]) < 1.0:
            count = count + 1
    if count == len(basefls):
        return True
    else:
        return False

# 读取待过滤的股票数据 过滤比较
def stockFilter( fname, factorls ):
    ilen = len( factorls )
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
        # 取10个值，计算斜率因子
        if ( i+ilen+1 > len(stockdatals) ):
            break
        ls = stockdatals[i:i+ilen+1]
        fls = createFactor( ls )
        #print( fls )
        # 与基准斜率因子比较
        if compareFactor( factorls, fls ):
            sdatels.append( datels[i] )
            plt.plot( ls )
            plt.savefig( datels[i], dpi=600 )
            #plt.close()

    return sdatels

def main():
    factorls = []
    factorls = parseConfig( CONFIG_FNAME )
    np.savetxt( FACTOR_FNAME, factorls, fmt='%.6f' )
    #print( factorls )
    sls = stockFilter( STOCK_FNAME, factorls )
    print( sls )

main()






