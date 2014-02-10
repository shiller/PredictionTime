import re
import Util
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
    
    with open(path, 'r') as output:
        content = output.readlines()
        
        for fileLine in content:
            modFileLine = fileLine.strip()
            data = re.split('\t', modFileLine)
            
            matrix.append(data)
    return matrix

