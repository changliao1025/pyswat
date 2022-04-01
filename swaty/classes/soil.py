import os,stat
import sys
import glob
import shutil

import numpy as np
from pathlib import Path
import tarfile
import subprocess
from shutil import copyfile
from abc import ABCMeta, abstractmethod
import datetime
from shutil import copy2
import json
from json import JSONEncoder
from swaty.classes.swatpara import swatpara
class SoilClassEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
         
        if isinstance(obj, swatpara):
            return json.loads(obj.tojson()) 
       
        if isinstance(obj, list):
            pass  
        return JSONEncoder.default(self, obj)
  

class pysoil(object):
    __metaclass__ = ABCMeta
    lIndex=-1
    iFlag_soil=0
    nSoil_layer = 1
    nParameter_soil=0
    aParameter_soil=None
    aParameter_soil_name = None

    def  __init__(self,aConfig_in):
        self.nParameter_soil = len(aConfig_in)
        self.aParameter_soil=list()
        self.aParameter_soil_name =list()
        for i in range(self.nParameter_soil):
            soil_dummy = aConfig_in[i]
            pParameter_soil = swatpara(soil_dummy)
            self.aParameter_soil.append(pParameter_soil)
            sName = pParameter_soil.sName
            if sName not in self.aParameter_soil_name:
                self.aParameter_soil_name.append(sName)

        return

    def tojson(self):
        aSkip = []      

        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
        sJson = json.dumps(obj,\
            sort_keys=True, \
                indent = 4, \
                    ensure_ascii=True, \
                        cls=SoilClassEncoder)
        return sJson 