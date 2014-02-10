# this class will execute the tools, create/overwrite outputFilesToolname.txt (besser: filename = TOOL+zeitangabe) 

import Util
from pyteomics import biolccc
import os



def factory(tool):
    if tool == "Elude":
        executeElude(tool)
        
    if tool == "SSRCalc":
        executeSSRcalc(tool)
        
    if tool == "BioLCCC":
        executeBioLCCC(tool)

def executeElude(tool):
    cmd = "%(train)s %(test)s %(out)s %(verbose)s" % Util.readConfigFile(Util.TOOL_CONFIG, tool)
    os.system(cmd)    
 
 
def executeSSRcalc(tool):  
    # post method
    print "no SSRCalc" 

#callTool with standard settings of tool
def executeBioLCCC(tool):
    paramToValue = Util.readConfigFile(Util.TOOL_CONFIG, tool)
    
    fobjOut = open(paramToValue["out"], 'w')
    
    with open(paramToValue["test"], 'r') as output:
        content = output.readlines()
        
        for fileLine in content:
            sequence = fileLine.strip() 
            retentionTime = biolccc.calculateRT(sequence, biolccc.rpAcnFaRod, biolccc.standardChromoConditions)
            fobjOut.write(sequence + "\t" + str(retentionTime) + "\n")
    fobjOut.close() 



