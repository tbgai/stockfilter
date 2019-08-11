# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 16:47:39 2019

@author: jingzl
"""
import numpy as np
import matplotlib.pyplot as plt


# stockfilter.py
CONFIG_FNAME = 'config.txt'
FACTOR_FNAME = 'factor.txt'
STOCK_FNAME = 'stock.csv'

# 生成斜率因子
def createFactor( ls ):
    
    factorls = ls
    
    return factorls
    

# 读取股票参数基准配置
def parseConfig( fname ):
    ls = np.loadtxt( fname, dtype=np.float, delimiter=',' )
    # 生成曲线
    plt.plot( ls )
    plt.savefig( 'test', dpi=600 )
    # 创建斜率因子
    return createFactor( ls )

# 读取待过滤的股票数据
def parseStockData():
    pass

# 过滤比较
def stockFilter():
    pass


def main():
    factorls = []
    factorls = parseConfig( CONFIG_FNAME )
    print( factorls[0] )
    
    parseStockData()
    stockFilter()


main()






