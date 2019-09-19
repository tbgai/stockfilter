# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:32:58 2019

@author: jingzl

stock filter algorithm method
"""
import time
import numpy as np
import matplotlib.pyplot as plt
import xlrd
from stockfilter.stockquery import StockQuery

class StockFilter( object ):
    
    basestock = []
    second_derivative = False
    output_pic = False
    result_days = 100
    
    def __init__( self, basestock, second_derivative, output_pic, result_days ):
        self.basestock = basestock
        self.second_derivative = second_derivative
        self.output_pic = output_pic
        self.result_days = result_days

    def filter( self  ):
        
        #print( self.basestock )
        
        print( "开始处理".center( 50, '-' ) ) 
        
        
        
        '''
        提前计算出基础数据的一阶导，二阶导数据
        
        1. 获取股票列表数据，进行循环
        2. 通过股票代码，获取单个股票的最近30天数据
        3. 对股票进行一阶导、二阶导计算
        4. 进行相关性分析比较
        5. 将过滤出来的股票数据的一阶导和二阶导数据绘制输出，同时绘制基础数据的一阶导/二阶导
        6. 再次获取过滤出来的股票最近100天的数据，绘制曲线输出
        7. 处理下一个股票
        '''
        
        start = time.perf_counter()
        
        # 股票处理循环
        for i in range(3000):
            a = '■' * (int)(i/3000 * 100)
            b = '□' * (int)(100-(i/3000.0 * 100))
            c = (i / 3000) * 100
            dur = time.perf_counter() - start
            print( "\r{:^3.0f}%[{}{}]{:.2f}s".format(c,a,b,dur), end='' )
            time.sleep(0.01)
        
        
        
        
        
        print( "\n"+"处理结束".center( 50, '-' ) )
        
        #stockquery = StockQuery()
        #stockquery.getStockBasicData()
        
        
        #print("stock filter")

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

