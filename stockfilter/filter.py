# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:32:58 2019

@author: jingzl

stock filter algorithm method
"""

class StockFilter():
    
    def __init__( self ):
        pass

    def filter( self ):
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


