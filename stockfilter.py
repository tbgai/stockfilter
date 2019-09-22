# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 16:47:39 2019

@author: jingzl
"""
# stockfilter.py
import os
#import shutil
from stockfilter import cons as ct
from stockfilter.configparser import ConfigParser
from stockfilter.filter import StockFilter


if __name__ == '__main__':
    
    config_file = os.path.dirname( os.path.realpath(__file__)) + ct.BASESTOCK_FNAME
    #print( config_file )
    config = ConfigParser()
    if config.parse( config_file ):
        
        basestock = config.getBaseStock()
        second_derivative = config.getSecondDerivative()
        delta_one = config.getDeltaOne()
        delta_two = config.getDeltaTwo()
        output_pic = config.getOutputPic()
        result_days = config.getResultDays()
        print("配置如下：")
        print("基准股票数据：" + str(basestock) )
        print("二阶导：" + str(second_derivative) )
        print("比较因子：" + str(delta_one) + " - " + str(delta_two) )
        print("输出图片：" + str(output_pic) )
        print("输出股票天数：" + str(result_days) )
        
        res = input( "请确认配置是否正确（Y/N）： " )
        if res[0] in [ 'Y', 'y' ]:
            sfilter = StockFilter( basestock, second_derivative, 
                                  delta_one, delta_two, output_pic, result_days )
            output_path = os.path.dirname( os.path.realpath(__file__))+ct.OUTPUT_DIR
            sfilter.setOutputPath( output_path )
            sfilter.filter()
        elif res[0] in [ 'N', 'n' ]:
            print( "程序退出..." )
        else:
            print( "输入错误！程序退出..." )

    else:
        print( "解析配置文件失败，请检查配置文件！" )
    
