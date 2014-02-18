import random
import re
import os
import csv

import Util
import PredictionToolReader
# import ConfigParser




#sequence modifying for toolINPUT
def getModSequences(tool, sequence, modToMod):
    
    modSequence = sequence
    if tool == "BioLCCC":
        
        for mod in modToMod.keys():
            if modSequence.find(mod) > -1:
                modSequence = modSequence.replace(mod, modToMod[mod])
        
        modSequence = "H-" + modSequence + "-NH2"
        
    if tool == "SSRCalc":
        for mod in modToMod.keys():
            if modSequence.find(mod) > -1:
                modSequence = modSequence.replace(mod, modToMod[mod])
        
        modSequence = modSequence
                                      
    if tool == "Elude":
        for mod in modToMod.keys():
            if modSequence.find(mod) > -1:
                modSequence = modSequence.replace(mod, modToMod[mod])
                
        modSequence = "-." + modSequence + ".-"
             
    return modSequence


# write toolinput out of config file of ptm
def writeToolInput(matrix, out, tool):
    pathToConfig = Util.PTM_CONFIG
    
    # read config, tool
    modToMod = Util.readConfigFile(pathToConfig, tool)
        
    toolInputFile = open(out+tool+".txt", 'w')
    # ignore header(=matrix[0])
    for row in matrix[1:]:
        sequence = row[0]
        modSequence = getModSequences(tool, sequence, modToMod)
        toolInputFile.write(modSequence+"\n")  

    toolInputFile.close()    

# read reference file and create matrix
def readReference(path):
    matrix = []
    #if path=file dann
    if os.path.isfile(path):
        with open(path, 'r') as output:
            content = output.readlines()
          
            for fileLine in content:
                modFileLine = fileLine.strip()
                data = re.split('\t', modFileLine)
                matrix.append(data)
#             
#     # else: lese alles im verzeichnis ein
#     print "hallo"
    elif os.path.isdir(path):
        dirContent = os.listdir(path)
        for fName in dirContent:
            if "~" in fName: continue
            absolute_path = os.path.join(path, fName)
            with open(absolute_path, 'r') as output:
                content = output.readlines()
         
                for fileLine in content:
                    modFileLine = fileLine.strip()
                    data = re.split('\t', modFileLine)
                    matrix.append(data)
#         
#     
    return matrix


# def randomGenerator(n, 30):
#     
#     counts = len(output)
#     
    

def createSampleFile(PATH_TO_REFERENCE):

    paramToValue = Util.readConfigFile(Util.TOOL_CONFIG, "General")
    path = PATH_TO_REFERENCE
    
    
    #read train file
    trainmat = readReference(path)
    #create dict out of reffile
    output = dict([(seq[0], seq[1]) for seq in trainmat])
    output_test = output.copy()

    # chose x-size peptides for testfile
    random_train = dict(random.sample(output.items(), int(paramToValue["trainsize"]))) 
    # createMatrix out of REFERENCE_TXT and add row with test also in train 0/1 or not
    for seq in random_train.keys():
        output_test.pop(seq)
    
    print output_test

     
    #TODO: fix static path     
    #write file train
    randTrain = open("/home/shiller/PredictionTools/train_tmp/train_tmp.txt", 'w')
    for key in random_train.keys():
        randTrain.write(str(key) + "\t" + str(random_train[key]) + "\n");
     
    #write file test 
    outpTest =  open("/home/shiller/PredictionTools/test_ref/test.txt", 'w')
    for key in output_test.keys():
        outpTest.write(str(key) + "\t" + str(output_test[key]) + "\n");
    
    #write file in tooloutput seq 0 oder seq 1 in train/testfile
