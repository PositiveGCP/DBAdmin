# -*- coding: utf-8 -*-
# Author: Dante Bazaldua
import json, os

positivefile = 'pos_conf.json'

class PositiveAuth( object ):
    firebase = {}
    user = {}

    def configFileExists( self ):
        if os.path.isfile( positivefile ):
            return True
        return False

    def readJson( self ):
        try:
            if self.configFileExists():
                config = open('pos_conf.json','r')
                data = json.load( config )
                config.close()
                self.firebase   = data['firebase']
                self.user       = data['userdata']
                return True
            return False
        except:
            return False
