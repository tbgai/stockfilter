# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:46:36 2019

@author: jingzl

parse config data
"""
import yaml


class ConfigParser( object ):
    
    base_stock = []
    second_derivative = False
    output_pic = False
    result_days = 100

    def __init__(self):
        pass

    def parse( self, filename ):
        
        f = open( filename, 'r' ).read()
        configs = yaml.safe_load( f )
        if configs:
            #print( configs )
            #print( type(configs ) )
            
            self.base_stock = configs['base']['base_stock']
            self.second_derivative = configs['algorithm']['second_derivative']
            self.output_pic = configs['output']['picture']
            self.result_days = configs['output']['result_days']
            
            return True
        else:
            return False

    def getBaseStock( self ):
        return self.base_stock
    
    def getSecondDerivative( self ):
        return self.second_derivative
    
    def getOutputPic( self ):
        return self.output_pic

    def getResultDays( self ):
        return self.result_days
    
