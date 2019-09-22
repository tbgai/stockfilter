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
    delta_one = 1.0
    delta_two = 1.0
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
            self.delta_one = configs['algorithm']['delta_one']
            self.delta_two = configs['algorithm']['delta_two']
            self.output_pic = configs['output']['picture']
            self.result_days = configs['output']['result_days']
            
            return True
        else:
            return False

    def getBaseStock( self ):
        return self.base_stock
    
    def getSecondDerivative( self ):
        return self.second_derivative

    def getDeltaOne( self ):
        return self.delta_one
    
    def getDeltaTwo( self ):
        return self.delta_two
    
    def getOutputPic( self ):
        return self.output_pic

    def getResultDays( self ):
        return self.result_days
    
