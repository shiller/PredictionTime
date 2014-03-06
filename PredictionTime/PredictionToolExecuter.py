# this class will execute the tools, create/overwrite outputFilesToolname.txt (besser: filename = TOOL+zeitangabe) 

import os
import subprocess 
import re

from pyteomics import biolccc

import Util
import SSRCalcTest
from lxml.html.builder import PARAM

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
    cmd = (cmd + " -t " + general["trainDirectory"] + paramToValue["trainFile"] + " -e " + general["testDirectory"] + paramToValue["ioFile"] + " -o " + general["outputDirectory"] + paramToValue["ioFile"] + " " + paramToValue["verbose"])
    p = subprocess.Popen([cmd], stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    ## TODO: wenn fehler, dann print
#     print out, err
    
#     takes output and connect with input rt
    output_RT_fh = open(Util.TOOLS_OUTPUT+"Elude.txt", 'r')
    content = output_RT_fh.readlines()
    output_RT_fh.close()
    
    #remove header
    output_RT = content[3:]
    output_set = {}
    
    for seq in output_RT:
        unimod = seq.split("\t")[0]
        unimod= unimod.strip()
        rt = seq.split("\t")[1]
        rt = rt.strip()
        output_set[unimod] = rt


    testRef_RT = open(Util.PATH_TO_TMP+"Elude_test_reference.txt", 'r')
    test_set = {}
#TODO: verknuepfe mir meine zwei sachen  modseq : rt fuer output
    for line in testRef_RT:
        sseq = line.split('\t')[1]
        sseq = sseq.strip()
        unimod = line.split('\t')[0] #key: toolinput
        unimod = unimod.strip()
        test_set[unimod] = sseq #returns value
    testRef_RT.close()    

    # write Tooloutputfile    
    elude = open(Util.TOOLS_OUTPUT+"Elude.txt", 'w')
    for key in output_set.keys():
        #rt = output_set[key]
        seq = test_set[key]
        seq = "."+ seq + "." # for PredictionToolReader.getSequence
        key = key.strip()
        elude.write("\t".join((  str(seq), str(output_set[key])) )) #Ausgabe: value testRef_RT = modSeq mit phosphos, RT Zeit  
        elude.write("\n")
    elude.close(), #os.unlink(Util.TOOLS_OUTPUT+"Elude.txt") #delete output because of Reference_R.mat
    
    
 
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
    
    
    # calculate RT and write tmp_output
    with open(general["testDirectory"]+paramToValue["ioFile"], 'r') as output:
        content = output.readlines()     
        for fileLine in content:
            sequence = fileLine.strip() 
            retentionTime = biolccc.calculateRT(sequence, chemBasis, myChromoConditions)
            fobjOut.write(sequence + "\t" + str(retentionTime) + "\n")
    fobjOut.close()
            
    # take output and connect with input rt
    output_RT_fh = open(Util.TOOLS_OUTPUT+"BioLCCC.txt", 'r')
    content = output_RT_fh.readlines()
    output_RT = content
    output_RT_fh.close()
    output_set = {}
     
    for seq in output_RT:
        seq = seq.strip()
        data = re.split('\t', seq)
        if len(data) != 2:
            print "ERROR in len data", data
            exit(-1)
        unimod = data[0]
        rt = data[1]
        output_set[unimod] = rt
 
    testRef_RT = open(Util.PATH_TO_TMP+"BioLCCC_test_reference.txt", 'r')
    test_set = {}
# verknuepfe mir meine zwei sachen  modseq : rt fuer output
    for line in testRef_RT:
        sseq = line.split('\t')[1]
        sseq = sseq.strip()
        unimod = line.split('\t')[0] #key: toolinput
        unimod = unimod.strip()
        test_set[unimod] = sseq #returns value
    testRef_RT.close()    
 
    os.unlink(Util.TOOLS_OUTPUT+"BioLCCC.txt")
    # write Tooloutput    
    biolc = open(Util.TOOLS_OUTPUT+"BioLCCC.txt", 'w')
    for key in output_set.keys():
        #rt = output_set[key]
        seq = test_set[key]
        seq = "-"+ seq + "-" # for PredictionToolReader.getSequence
        key = key.strip()
        biolc.write("\t".join((  str(seq), str(output_set[key])) )) #Ausgabe: value testRef_RT = modSeq mit phosphos, RT Zeit  
        biolc.write("\n")
            
            
            
    

    