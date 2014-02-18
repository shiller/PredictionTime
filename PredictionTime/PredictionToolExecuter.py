# this class will execute the tools, create/overwrite outputFilesToolname.txt (besser: filename = TOOL+zeitangabe) 

import os
import subprocess 

from pyteomics import biolccc

import SSRCalcTest
import Util
from lxml.html.builder import PARAM
import SSRCalcTest

def factory(tool):
    if tool == "Elude":
        print "start " + tool
        executeElude(tool)
        
    if tool == "SSRCalc":
        print "start " + tool
        executeSSRcalc(tool)
        
    if tool == "BioLCCC":
        print "start " + tool
        executeBioLCCC(tool)

def executeElude(tool):
    
    #TODO: test train file; was wenn test=train bzw train !=test...
    paramToValue = Util.readConfigFile(Util.TOOL_CONFIG, tool)
    general = Util.readConfigFile(Util.TOOL_CONFIG, "General")
    
    cmd = "%(cmd)s" % Util.readConfigFile(Util.TOOL_CONFIG, tool)
    cmd = (cmd + " -t " + general["traindirectory"] + paramToValue["trainfile"] + " -e " + general["testdirectory"] + paramToValue["iofile"] + " -o " + general["outputdirectory"] + paramToValue["iofile"] + paramToValue["verbose"])
    p = subprocess.Popen([cmd], stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    ## TODO: wenn fehler, dann print
    print cmd
    print err
    
 
def executeSSRcalc(tool):  

    paramToValue = Util.readConfigFile(Util.TOOL_CONFIG, "SSRCalc")
    general = Util.readConfigFile(Util.TOOL_CONFIG, "General")    
    test_seq_file = open(general["testdirectory"]+paramToValue["iofile"], 'r')  

    #TODO: test train file; was wenn test=train bzw train !=test... ergibt fehler, wenn INPUTFILE nicht da, dabei sollte der das doch erstellen
    
    test_seq_file = general["testdirectory"]+paramToValue["iofile"]

    inputfh = open(test_seq_file, 'r')
    test_seq = inputfh.readlines()

    ionpAgent = "%(ion_pairing_agent)s" % paramToValue
    poreS = float("%(pore_size)s" % paramToValue)
    pH = float("%(ph)s" % paramToValue)
    SSRCalcTest.calculate_RT(test_seq, ionpAgent, poreS, pH)
    
##wenn fehler, dann print fehler


def executeBioLCCC(tool):
    
  ##wenn fehler, dann print fehler
    
    general = Util.readConfigFile(Util.TOOL_CONFIG, "General")
    paramToValue = Util.readConfigFile(Util.TOOL_CONFIG, tool)
    
    fobjOut = open(general["outputdirectory"]+paramToValue["iofile"], 'w')    

    # read values from configfile
    # myChromoConditions
    myChromoConditions = biolccc.standardChromoConditions
    
    if ("columnLength" in paramToValue):
        myChromoConditions['columnLength'] = float("%(columnLength)s" % paramToValue)
    elif("columnDiameter"in paramToValue):    
        myChromoConditions['columnDiameter'] = float("%(columnDiameter)s" % paramToValue)
    elif("columnPoreSize"in paramToValue): 
        myChromoConditions['columnPoreSize'] = float("%(columnPoreSize)s" % paramToValue)
    elif("secondSolventConcentrationA"in paramToValue): 
        myChromoConditions['secondSolventConcentrationA'] = float("%(secondSolventConcentrationA)s" % paramToValue)
    elif("secondSolventConcentrationB"in paramToValue): 
        myChromoConditions['secondSolventConcentrationB'] = float("%(secondSolventConcentrationB)s" % paramToValue)
    elif("gradient"in paramToValue): 
        myChromoConditions['gradient'] = biolccc.Gradient("%initialConcentrationB", "%finalConcentrationB", "%time" % paramToValue)
    elif("flowRate"in paramToValue): 
        myChromoConditions['flowRate'] = float("%(flowRate)s" % paramToValue)
        
    
    # calculateRT
    continueGradient=bool("%(continuegradient)s" % paramToValue)
    numinterpolationspoints=int("%(numinterpolationspoints)s" % paramToValue)
    chem_basis_map = {}
    chem_basis_map["rpAcnFaRod"] = biolccc.rpAcnFaRod
    chem_basis_map["rpAcnTfaChain"] = biolccc.rpAcnTfaChain
    chemBasis = chem_basis_map["%(chembasis)s" %paramToValue]
    
    
    
    with open(general["testdirectory"]+paramToValue["iofile"], 'r') as output:
        content = output.readlines()     
        for fileLine in content:
            sequence = fileLine.strip() 
            retentionTime = biolccc.calculateRT(sequence, chemBasis, myChromoConditions)
            fobjOut.write(sequence + "\t" + str(retentionTime) + "\n")

    fobjOut.close() 
    