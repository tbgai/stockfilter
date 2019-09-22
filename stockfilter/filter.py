# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:32:58 2019

@author: jingzl

stock filter algorithm method
"""
import time
import numpy as np
import matplotlib.pyplot as plt
from stockfilter.stockquery import StockQuery


class StockFilter( object ):
    
    basestock = []
    basestock_num = 0
    second_derivative = False
    delta_one = 1.0
    delta_two = 1.0
    output_pic = False
    result_days = 100
    basefactor1 = [] # 基准数据的一阶导
    basefactor2 = [] # 基准数据的二阶导
    resultStock = [] # 过滤出来的股票列表
    output_path = ""
    
    def __init__( self, basestock, second_derivative, delta_one, delta_two, output_pic, result_days ):
        self.basestock = basestock
        self.basestock_num = len( basestock )
        self.second_derivative = second_derivative
        self.delta_one = delta_one
        self.delta_two = delta_two
        self.output_pic = output_pic
        self.result_days = result_days
    
    def setOutputPath( self, path ):
        self.output_path = path
    
    def filter( self  ):
        
        #print( self.basestock )
        
        print( "开始处理".center( 50, '-' ) )
        start = time.perf_counter()

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
        self.basefactor1 = self.createFactor( self.basestock )
        if ( self.second_derivative ):
            self.basefactor2 = self.createFactor( self.basefactor1 )

        stockquery = StockQuery()
        stocklist = stockquery.getStockBasicData()
        #print( stocklist )
        length = len(stocklist)
        #length = 1000
        # 股票处理循环
        for i in range(length):
            a = '■' * (int)(i/length * 100)
            b = '□' * (int)(100-(i/length * 100))
            c = (i / length) * 100
            
            dl = stockquery.getSingleStockData( stocklist[i], self.basestock_num )
            if len(dl) == self.basestock_num:
                # 处理
                if not self.second_derivative:
                    self.filterStockbyDerivativeOne( stockquery, stocklist[i], dl )
                else:
                    self.filterStockbyDerivativeTwo( stockquery, stocklist[i], dl )
            else:
                # 记录错误日志
                pass
                
            dur = time.perf_counter() - start
            print( "\r{:^3.0f}%[{}{}]{:.2f}s".format(c,a,b,dur), end='' )
            # 避免tushare接口调用频繁被禁
            time.sleep( 0.1 )
            
        # 输出股票代码到文件
        resary = np.array( self.resultStock )
        print( resary )
        np.savetxt( self.output_path+"stock.txt", resary, fmt='%s', delimiter=';' )
        print( "\n"+"处理结束".center( 50, '-' ) )

    def createFactor( self, ls ):
        # 斜率计算，求一阶导
        factorls = []
        size = len(ls)
        i = 0
        for item in ls:
            if i == size-1:
                break;
            # 斜率计算
            factor = (ls[i+1]-ls[i])
            factorls.append( factor )
            i = i+1
        return factorls

    def filterStockbyDerivativeOne( self, stockquery, stock_code, stockdata ):
        # 通过求导来对单个股票数据进行过滤
        fls = self.createFactor( stockdata )
        if self.compareFactor( self.basefactor1, fls ):
            self.resultStock.append( stock_code )
            '''
            绘制基准数与股票值的图
            绘制一阶导值得图
            绘制该股票仅100交易日图
            '''
            if self.output_pic:
                '''
                plt.cla()
                plt.title( stock_code+"与基准股票值比较", fontproperties="SimHei" )
                x = np.arange(self.basestock_num)
                plt.plot( x, self.basestock, "ro-", x, stockdata, "bo--" )
                plt.savefig( self.output_path+stock_code+".jpg", dpi=600 )
                '''
                
                dl = stockquery.getSingleStockData( stock_code, self.result_days )
                if len(dl) > 0:
                    plt.cla()
                    plt.title( stock_code+"最近"+str(self.result_days)+"个交易日", 
                              fontproperties="SimHei" )
                    x = np.arange( self.result_days )
                    plt.plot( x, dl, "bo-" )
                    plt.savefig( self.output_path+stock_code+"_"+str(self.result_days)+".jpg", dpi=600 )
                    
                
                plt.cla()
                plt.title( stock_code+"与基准模型一阶变化比较(最近"+str(self.basestock_num)
                                    +"个交易日)", fontproperties="SimHei" )
                x = np.arange(len(self.basefactor1))
                plt.plot( x, self.basefactor1, "ro-", x, fls, "bo--" )
                plt.savefig( self.output_path+stock_code+"_D1"+".jpg", dpi=600 )
                
            

    def filterStockbyDerivativeTwo( self, stockquery, stock_code, stockdata ):
        # 通过求二阶导来对股票进行过滤
        fls = self.createFactor( stockdata )
        fls2 = self.createFactor( fls )
        if self.compareFactor( self.basefactor2, fls2 ):
            self.resultStock.append( stock_code )
            '''
            绘制二阶导值得图
            绘制该股票仅100交易日图
            '''
            if self.output_pic:
                
                dl = stockquery.getSingleStockData( stock_code, self.result_days )
                if len(dl) > 0:
                    plt.cla()
                    plt.title( stock_code+"最近"+str(self.result_days)+"个交易日", 
                              fontproperties="SimHei" )
                    x = np.arange( self.result_days )
                    plt.plot( x, dl, "bo-" )
                    plt.savefig( self.output_path+stock_code+"_"+str(self.result_days)+".jpg", dpi=600 )
                    
                
                plt.cla()
                plt.title( stock_code+"与基准模型二阶变化比较(最近"+str(self.basestock_num)
                                    +"个交易日)", fontproperties="SimHei" )
                x = np.arange(len(self.basefactor1))
                plt.plot( x, self.basefactor1, "ro-", x, fls, "bo--" )
                plt.savefig( self.output_path+stock_code+"_D2"+".jpg", dpi=600 )
        
        

    def compareFactor( self, basefls, fls ):
        # 斜率因子比较
        if len(basefls) != len(fls):
            return False
        count = 0
        delta = self.delta_one
        if self.second_derivative:
            delta = self.delta_two
        for i in range(len(basefls)):
            if abs(basefls[i]-fls[i]) < delta:
                count = count + 1
        
        '''
        此处要求所有的节点数据均在设定的delta值内，这样做有很大局限性
        可能部分股票值的比值更好，但可能会被排除外
        这个地方待改进
        count < len(basefls)/2
        '''
        if count == len(basefls):
            return True
        else:
            return False
    
    
    


'''
# 过滤股票的自我历史数据比较
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
'''
