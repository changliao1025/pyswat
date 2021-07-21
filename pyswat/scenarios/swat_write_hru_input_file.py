#this function is used to write the input file
import os
import sys
import numpy as np

from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string


#in order to write a new hru file, we need to know the parameters to be replaced.
#the user need to be familiar with the structure of the input file
#ideally, the input variable should have dictionary data type so a list of variable can be repalced together

def swat_write_hru_input_file(oModel_in):
    """
    write the input files from the new parameter generated by PEST to each hru file
    """
    aVariable = oModel_in.aVariable
    nvariable = len(aVariable)
    if(nvariable<1):
        #there is nothing to be replaced at all
        print("There is nothing to be updated!")
        return
    else:
        pass    
    
    iFlag_simulation = oModel_in.iFlag_simulation
    iFlag_calibration = oModel_in.iFlag_calibration

    
    sWorkspace_simulation_case = oModel_in.sWorkspace_simulation_case
    sWorkspace_simulation_copy =  oModel_in.sWorkspace_simulation_copy

    sWorkspace_calibration_case = oModel_in.sWorkspace_calibration_case
    sWorkspace_pest_model = sWorkspace_calibration_case

    sWorkspace_data_project = oModel_in.sWorkspace_data_project
   

    sFilename_watershed_configuration = sWorkspace_data_project + slash \
    + 'auxiliary' + slash  + 'subbasin' + slash \
    + 'watershed_configuration.txt'

    #check whether file exist
    if os.path.isfile(sFilename_watershed_configuration):
        pass
    else:
        print('The file does not exist: ' + sFilename_watershed_configuration)
        return
    aSubbasin_hru  = text_reader_string( sFilename_watershed_configuration, cDelimiter_in = ',' )
    
    aSubasin = aSubbasin_hru[:,0].astype(int)
    aHru = aSubbasin_hru[:,1].astype(int)

    nsubbasin = len(aSubasin)
    nhru = sum(aHru)

    sFilename_hru_info = sWorkspace_data_project + slash + 'auxiliary' + slash \
      + 'hru' + slash + 'hru_info.txt'
    if os.path.isfile(sFilename_hru_info):
        pass
    else:
        print('The file does not exist: ')
        return
    aHru_info = text_reader_string(sFilename_hru_info)
    aHru_info = np.asarray(aHru_info)
    nhru = len(aHru_info)
    aHru_info= aHru_info.reshape(nhru)

    sFilename_hru_combination = sWorkspace_data_project + slash + 'auxiliary' + slash \
      + 'hru' + slash + 'hru_combination.txt'
    if os.path.isfile(sFilename_hru_combination):
        pass
    else:
        print('The file does not exist: ')
        return
    aHru_combination = text_reader_string(sFilename_hru_combination)
    aHru_combination = np.asarray(aHru_combination)
    
    nhru_type = len(aHru_combination)
    aHru_combination= aHru_combination.reshape(nhru_type)

    # we need to identify a list of files that are HRU defined, you can add others later
    aExtension = ('.chm','.gw','.hru','.mgt','.sdr', '.sep', '.sol')
    #now we can add corresponding possible variables
    

    aCHM =[]
    aGW = []
    aHRU =[]
    aMGT = ['cn2']
    aSDR = []
    aSEP =[]
    aSOL=['awc']

    aExtension = np.asarray(aExtension)
    nFile_type= len(aExtension)

    #the parameter is located in the different files
    aParameter_table = np.empty( (nFile_type)  , dtype = object )

    #need a better way to control this 
    for iVariable in range(nvariable):
        sVariable = aVariable[iVariable]

        if sVariable in aCHM:
            pass
        else:
            if sVariable in aGW:
                pass
            else:
                if sVariable in aHRU:
                    pass
                else:
                    if sVariable in aMGT:
                        if( aParameter_table[3] is None  ):
                            aParameter_table[3] = sVariable
                        else:
                            aParameter_table[3].append(sVariable)                             
                    else:
                        if sVariable in aSDR:
                            pass
                        else: 
                            if sVariable in aSEP:
                                pass
                            else:
                                if sVariable in aSOL:
                                    if( aParameter_table[6] is None  ):
                                        aParameter_table[6] = sVariable
                                    else:
                                        aParameter_table[6].append(sVariable) 
                                else:
                                    pass
                        
        

    

    aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) )
    aParameter_count = np.full( (nFile_type) , 0 , dtype = int )
    aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )
    aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) )
  
    #then we need to define what parameters may be calibrated
    #this list should include all possible parameters in the parameter file
  
    #read parameter file
    if iFlag_simulation == 1:
        sFilename_parameter = sWorkspace_simulation_case + slash + 'hru.para'
    else:
        iFlag_debug = 0
        
        sPath_current = os.getcwd()


        sFilename_parameter = sPath_current + slash + 'hru.para'
    #check whetheher the file exist or not
    if os.path.isfile(sFilename_parameter):
        pass
    else:
        print('The file does not exist: '+sFilename_parameter)
        return

    aData_all = text_reader_string(sFilename_parameter, cDelimiter_in =',')
    aDummy = aData_all[0,:]
    nParameter = len(aDummy) - 1
    aParameter_list = aDummy[1: nParameter+1]

    aParameter_value = (aData_all[1:nhru,1: nParameter+1]).astype(float)
    aParameter_value = np.asarray(aParameter_value)
    
    for p in range(0, nParameter):
        para = aParameter_list[p]
        for i in range(0, nFile_type):
            aParameter_tmp = aParameter_table[i]
            if aParameter_tmp is not None:
                if para in aParameter_tmp:
                    aParameter_count[i]= aParameter_count[i]+1
                    aParameter_flag[i]=1

                    if(aParameter_count[i] ==1):
                        aParameter_index[i] = [p]
                        aParameter_user[i]= [para]
                    else:
                        aParameter_index[i] = np.append(aParameter_index[i],[p])
                        aParameter_user[i] = np.append(aParameter_user[i],[para])
                    continue

    sWorkspace_source_case = sWorkspace_simulation_copy
    sWorkspace_target_case = sWorkspace_simulation_case
    if iFlag_simulation == 1:
        pass
    else:
        sPath_current = os.getcwd()
        if (os.path.normpath(sPath_current)  == os.path.normpath(sWorkspace_pest_model)):
            print('this is the parent, no need to copy anything')
            return
        else:
            print('this is a child')
            sWorkspace_source_case = sWorkspace_simulation_copy
            sWorkspace_target_case = sWorkspace_simulation_case

    iHru_index = 0 
    for iSubbasin in range(0, nsubbasin):
        #subbasin string
        sSubbasin = "{:05d}".format( iSubbasin + 1)
        nhru = aHru[ iSubbasin]
        #loop through all hru in this subbasin
        for iHru in range(0, nhru):
            #hru string
            sHru = "{:04d}".format( iHru + 1)
            #find the hry type 
            sHru_code = aHru_info[iHru_index]
            iIndex = np.where(aHru_combination == sHru_code)
            iHru_index = iHru_index + 1
            for iFile_type in range(0, nFile_type):
                #check whether these is parameter chanage or not
                sExtension = aExtension[iFile_type]
                iFlag = aParameter_flag[iFile_type]
                if( iFlag == 1):
                    sFilename = sSubbasin + sHru + sExtension
                    sFilename_hru = sWorkspace_source_case + 'TxtInOut' + slash + sFilename 
                    #open the file to read
                    ifs=open(sFilename_hru, 'r')   
                    sLine = ifs.readline()
                    #open the new file to write out
                    sFilename_hru_out = sWorkspace_target_case + slash + sFilename
                    #do we need to remove linnk first, i guess it's better to do so
                    if os.path.isfile(sFilename_hru_out):
                        #remove it 
                        os.remove(sFilename_hru_out)
                    else:
                        pass
                    ofs=open(sFilename_hru_out, 'w') 
                    #because of the python interface, pest will no longer interact with model files directly
                    #starting from here we will                             
                    aValue = aParameter_value[iIndex[0], :]
                    while sLine:
                        aParameter = aParameter_user[iFile_type]
                       
                        for i in range(0, aParameter_count[iFile_type]):
                            #sKey = aParameter[i]
                            if 'cn2' in sLine.lower() : 
                                dummy = 'cn2' + "{:02d}".format(iSubbasin) \
                                + "{:02d}".format(iHru) 
                                dummy1 = np.array(aParameter_index[3])
                                dummy2 = np.array(aParameter_user[3])
                                dummy_index1 = np.where(dummy2 == 'cn2')
                                dummy_index2 = dummy1[dummy_index1][0]
                                sLine_new = "{:16.2f}".format(  aValue[0][dummy_index2]  )     + '    | pest parameter CN2 \n'
                                ofs.write(sLine_new)
                                
                            else:
                                if ' Ave. AW Incl. Rock' in sLine :
                                     #get substring
                                    sLine_sub = sLine[27:]
                                    dummy = sLine_sub.split()                
                                    nSoil_layer  = len(dummy)
                                    sLine_new = '{0: <27}'.format(' Ave. AW Incl. Rock: ')
                                    dummy1 = np.array(aParameter_index[6])
                                    dummy2 = np.array(aParameter_user[6])
                                    dummy_index1 = np.where(dummy2 == 'awc')
                                    dummy_index2 = dummy1[dummy_index1][0]
                                    for j in range(nSoil_layer):
                                        sLine_new = sLine_new +  "{:12.2f}".format(  aValue[0][dummy_index2]  ) 
                                    sLine_new = sLine_new + '\n'
                                    ofs.write(sLine_new)
                                    
                                else:
                                    ofs.write(sLine)
                        sLine = ifs.readline() 
                    #close files
                    ifs.close()
                    ofs.close()
                else:
                    #this file does not need to changed
                    pass

    print('Finished writing hru file!')

