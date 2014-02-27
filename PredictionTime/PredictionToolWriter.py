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
    
    toolInputRefFile = open(Util.PATH_TO_TMP+tool+"_test_reference.txt", 'w')
    # ignore header(=matrix[0])
    for row in matrix:
        sequence = row[0]
        modSequence = getModSequences(tool, sequence, modToMod)
        toolInputRefFile.write(modSequence + "\t" + sequence + "\n")  

    toolInputRefFile.close() 
    
        
    toolInputFile = open(out+tool+".txt", 'w')
    # ignore header(=matrix[0])
    for row in matrix:
        sequence = row[0]
        modSequence = getModSequences(tool, sequence, modToMod)
        toolInputFile.write(modSequence+ "\n")  

    toolInputFile.close()   
    
    
def writeTrainInput(matrix, out, tool):
    pathToConfig = Util.PTM_CONFIG
    
    # read config, tool
    modToMod = Util.readConfigFile(pathToConfig, tool)
        
    toolTrainRefFile = open(out+tool+"_train_reference.txt", 'w')
    # ignore header(=matrix[0])
    #write train_ref_file for checking the RTs
    for row in matrix:
        sequence = row[0]
        rt_given = row[1]
        modSequence = getModSequences(tool, sequence, modToMod)
        toolTrainRefFile.write(modSequence + "\t" + sequence + "\t" + rt_given + "\n") 

    toolTrainRefFile.close() 
    
    toolInputFile = open(Util.PATH_TO_TRAIN+tool+".txt", 'w')
    # ignore header(=matrix[0])
    #write trainToolinputfile
    for row in matrix:
        sequence = row[0]
        rt_given = row[1]
        modSequence = getModSequences(tool, sequence, modToMod)
        if tool != "BioLCCC":
            toolInputFile.write(modSequence + "\t" + rt_given + "\n") 
        else:
            toolInputFile.write(modSequence + "\n") 

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


def createSampleFile(PATH_TO_REFERENCE):

    paramToValue = Util.readConfigFile(Util.TOOL_CONFIG, "General")
    path = Util.PATH_TO_TRAIN_REF
    
    
    #read train file S4
    trainmat = readReference(path)
    #create dict out of reffile
    #trainmat[1:] ignore header
    output = dict([(seq[0], seq[1]) for seq in trainmat[1:]])
    output_test = output.copy()

    # chose x-size peptides for testfile
    random_train = dict(random.sample(output.items(), int(paramToValue["trainsize"]))) 
    # createMatrix out of REFERENCE_TXT and add row with test also in train 0/1 or not
    for seq in random_train.keys():
        output_test.pop(seq)
         
    #TODO: fix static path     
    #write file train
    randTrain = open(Util.PATH_TRAIN_TMP+"train_tmp.txt", 'w')
    for key in random_train.keys():
        randTrain.write(str(key) + "\t" + str(random_train[key]) + "\n")
     
    #write file test 
    outpTest =  open(Util.PATH_TO_TEST_REF+"test.txt", 'w')
    for key in output_test.keys():
        outpTest.write(str(key) + "\t" + str(output_test[key]) + "\n")
    

