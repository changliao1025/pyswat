from pyswat.simulation.swat_main import swat_main

from pyswat.pyswat_read_model_configuration_file import swat_read_model_configuration_file
from pyswat.classes.pycase import pyswat


aParameter_watershed = ['SFTMP','SMTMP']
aParameter_subbasin = ['CH_K2','CH_N2']
aParameter_hru = ['CN2']

aParameter = ['SFTMP']#,'SMTMP','CH_K2','CH_N2','cn2']

aValue = [1.0]#,2.0,0.5,3, 7]

sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/pyswat/pyswat/shared/swat_simulation.xml'
#step 1
aConfig = swat_read_model_configuration_file(sFilename_configuration_in)
aConfig['sFilename_model_configuration'] = sFilename_configuration_in
oModel = pyswat(aConfig)
swat_main(oModel)  #, sCase_in = sCase, iFlag_mode_in= iFlag_mode, aParameter_in = aParameter, aValue_in = aValue)