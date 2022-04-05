from collections import _OrderedDictKeysView
import os
from pprint import pp 
import sys #used to add system path

import datetime
import json
import numpy as np
import pyearth.toolbox.date.julian as julian
from swaty.auxiliary.text_reader_string import text_reader_string
from swaty.classes.pycase import swatcase

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def swaty_read_model_configuration_file(sFilename_configuration_in , \
    iFlag_standalone_in=None, iCase_index_in = None, sDate_in = None,\
        iYear_start_in = None,\
            iMonth_start_in = None,\
                iDay_start_in = None, \
        iYear_end_in = None,\
            iMonth_end_in = None,\
                iDay_end_in = None, \
          sWorkspace_input_in =None, \
              sWorkspace_output_in =None ,\
              aParameter_in=None  ):

    if not os.path.isfile(sFilename_configuration_in):
        print(sFilename_configuration_in + ' does not exist')
        return
    
    # Opening JSON file
    with open(sFilename_configuration_in) as json_file:
        aConfig = json.load(json_file)   

    sModel = aConfig['sModel'] 
    sRegion = aConfig['sRegion']

    if sWorkspace_input_in is not None:
        sWorkspace_input = sWorkspace_input_in
    else:
        sWorkspace_input = aConfig['sWorkspace_input']
        pass
    if sWorkspace_output_in is not None:
        sWorkspace_output = sWorkspace_output_in
    else:
        sWorkspace_output = aConfig['sWorkspace_output']
        pass
 

    
    if iFlag_standalone_in is not None:        
        iFlag_standalone = iFlag_standalone_in
    else:       
        iFlag_standalone = int( aConfig['iFlag_standalone'])
    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = aConfig['sDate']
        pass
    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        iCase_index = int( aConfig['iCase_index'])
        
    
    if iYear_start_in is not None:        
        iYear_start = iYear_start_in
    else:       
        iYear_start  = int( aConfig['iYear_start'])

    if iMonth_start_in is not None:        
        iMonth_start = iYear_end_in
    else:       
        iMonth_start  = int( aConfig['iMonth_start'])

    if iDay_start_in is not None:        
        iDay_start = iDay_start_in
    else:       
        iDay_start  = int( aConfig['iDay_start'])
    
    if iYear_end_in is not None:        
        iYear_end = iYear_end_in
    else:       
        iYear_end  = int( aConfig['iYear_end'])
    
    if iMonth_end_in is not None:        
        iMonth_end = iMonth_end_in
    else:       
        iMonth_end  = int( aConfig['iMonth_end'])

    if iDay_end_in is not None:
        iDay_end = iDay_end_in
    else:       
        iDay_end  = int( aConfig['iDay_end'])

    if aParameter_in is not None:
        iFlag_paramter = 1
        aParameter = aParameter_in
    else:       
        iFlag_paramter = 0
        

    #by default, this system is used to prepare inputs for modflow simulation.
    #however, it can also be used to prepare gsflow simulation inputs.

    #based on global variable, a few variables are calculate once
    #calculate the modflow simulation period
    #https://docs.python.org/3/library/datetime.html#datetime-objects
    
    aConfig['iFlag_standalone'] = iFlag_standalone
    aConfig['iCase_index'] = iCase_index
    aConfig['sDate'] = sDate
    aConfig['sWorkspace_input'] = sWorkspace_input
    aConfig['sWorkspace_output'] = sWorkspace_output
    dummy1 = datetime.datetime(iYear_start, iMonth_start, iDay_start)
    dummy2 = datetime.datetime(iYear_end, iMonth_end, iDay_end)
    julian1 = julian.to_jd(dummy1, fmt='jd')
    julian2 = julian.to_jd(dummy2, fmt='jd')

    nstress =int( julian2 - julian1 + 1 )  
    aConfig['lJulian_start'] =  julian1
    aConfig['lJulian_end'] =  julian2
    aConfig['nstress'] =   nstress     
   
    sFilename_swat = aConfig['sFilename_swat']   

    if 'nhru' in aConfig:
        pass
    

    #data
    oSwat = swatcase(aConfig)

    #we need to initialize the discretization
    sFilename_soil_info = oSwat.sFilename_soil_info
    aSoil_info = np.array(text_reader_string(sFilename_soil_info)).astype(int)

    if iFlag_paramter ==1:
        for i in range(len(aParameter)):
            pParameter = aParameter[i]
            sName = pParameter.sName
            iType = pParameter.iParameter_type
            iIndex_subbasin = pParameter.iIndex_subbasin
            iIndex_hru = pParameter.iIndex_hru
            iIndex_soil_layer = pParameter.iIndex_soil_layer
            dValue = pParameter.dValue_current
            iFlag_found =0
            if iType == 1:                
                for j in range(oSwat.nParameter_watershed):
                    pPara = oSwat.aParameter_watershed[j]
                    sName1 = pPara.sName
                    if sName.lower() == sName1.lower():
                        #replace
                        oSwat.aParameter_watershed[j].dValue_current = dValue
                        iFlag_found = 1
                        break
                
                #if iFlag_found == 0:
                #    #this one is not in the list yet
                #    pass
                    
            else:
                if iType == 2: #subbasin level
                    #get name index
                                       
                    for j in np.arange(oSwat.nsubbasin ):
                        iIndex_name = oSwat.aSubbasin[j].aParameter_subbasin_name.index(sName) 
                        pPara = oSwat.aSubbasin[j].aParameter_subbasin[iIndex_name]
                        sName1 = pPara.sName
                        iIndex1 = pPara.iIndex_subbasin
                        if  iIndex_subbasin == iIndex1:
                            #replace
                            oSwat.aSubbasin[j].aParameter_subbasin[iIndex_name].dValue_current = dValue
                            iFlag_found = 1
                            break
                    pass
                else: #hru level
                    if iType == 3:
                        for j in np.arange(oSwat.nhru ):
                            iIndex_name = oSwat.aHru[j].aParameter_hru_name.index(sName) 
                            pPara = oSwat.aHru[j].aParameter_hru[iIndex_name]
                            sName1 = pPara.sName
                            iIndex1 = pPara.iIndex_hru
                            if  iIndex_hru == iIndex1:
                                #replace
                                oSwat.aSubbasin[j].aParameter_subbasin[iIndex_name].dValue_current = dValue
                                iFlag_found = 1
                                break
                        pass
                    else: #soil layer
                        for j in np.arange(oSwat.nhru ):
                            for k in np.arange(oSwat.aHru[j].nSoil_layer):
                                iIndex_name = oSwat.aHru[j].aSoil[k].aParameter_soil_name.index(sName) 
                                pPara = oSwat.aHru[j].aSoil[k].aParameter_soil[iIndex_name]
                                sName1 = pPara.sName
                                iIndex0 = pPara.iIndex_hru
                                iIndex1 = pPara.iIndex_soil_layer
                                if iIndex_hru ==iIndex0 and  iIndex_soil_layer == iIndex1:
                                    #replace
                                    oSwat.aHru[j].aSoil[k].aParameter_soil[iIndex_name].dValue_current = dValue
                                    iFlag_found = 1
                                    break
                        pass
                    pass #

            
        pass
    
    
    


   
    
    return oSwat