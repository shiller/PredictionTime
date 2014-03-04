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
    cmd = (cmd + " -t " + general["trainDirectory"] + paramToValue["trainFile"] + " -e " + general["testDirectory"] + paramToValue["ioFile"] + " -o " + general["outputDirectory"] + paramToValue["ioFile"] + paramToValue["verbose"])
    p = subprocess.Popen([cmd], stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    ## TODO: wenn fehler, dann print
#     print out, err
#     p.wait()
    
#     takes output and connect with input rt
    output_RT = open(Util.TOOLS_OUTPUT+"Elude.txt-v", 'r')
    content = output_RT.readlines()
    #remove header
    output_RT = content[3:]
    output_set = {}
    
    for seq in output_RT:
        print seq
        sseq = seq.split("\t")[0]
        sseq= sseq.strip()
        rt = seq.split("\t")[1]
        rt = rt.strip()
        output_set[seq] = rt
        print output_set[seq], " = ", sseq, rt 

    testRef_RT = open(Util.PATH_TO_TMP+"Elude_test_reference.txt", 'r')
    test_set = {}
#TODO: verknuepfe mir meine zwei sachen  modseq : rt fuer output
    for seq in testRef_RT:
#   #key=toolinputseq; value=modSeq
        sseq = seq.split('\t')[1]
        sseq = sseq.strip()
        modSeq = seq.split('\t')[0]
        modSeq = modSeq.strip()
        test_set[modSeq] = sseq
    testRef_RT.close()    

    # write Tooloutput    
    elude = open(Util.TOOLS_OUTPUT+"Elude.txt", 'w')
    for seq in output_set.keys():
        elude.write("\t".join((str(test_set[seq]), str(output_set[seq])))) #Ausgabe: value testRef_RT = modSeq mit phosphos, RT Zeit  
        elude.write("\n")
    elude.close()
    
 
def executeSSRcalc(tool):  

    paramToValue = Util.readConfigFile(Util.TOOL_CONFIG, "SSRCalc")
    general = Util.readConfigFile(Util.TOOL_CONFIG, "General")    
    #TODO: test train file; was wenn test=train bzw train !=test... ergibt fehler, wenn INPUTFILE nicht da, dabei sollte der das doch erstellen
    
    test_seq_file = general["testDirectory"]+paramToValue["ioFile"]

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
    
    fobjOut = open(general["outputDirectory"]+paramToValue["ioFile"], 'w')    

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
    
    
    
    with open(general["testDirectory"]+paramToValue["ioFile"], 'r') as output:
        content = output.readlines()     
        for fileLine in content:
            sequence = fileLine.strip() 
            retentionTime = biolccc.calculateRT(sequence, chemBasis, myChromoConditions)
            fobjOut.write(sequence + "\t" + str(retentionTime) + "\n")

    fobjOut.close() 
    