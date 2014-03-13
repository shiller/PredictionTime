import ConfigParser
import os


def readConfigFile(pathToConfig, tool):
        
    valueToKey = {}
    
    parser = ConfigParser.ConfigParser()
    
    # make case sensitive for [key]-call
    parser.optionxform = str

    parser.read(pathToConfig)
    
    for key in parser.options(tool):
        valueToKey[key] = parser.get(tool, key)
    
    return valueToKey


paramToValue = readConfigFile("/home/shiller/PredictionTools/config/ToolParam.conf", "General")

TOOL_CONFIG = "%(TOOL_CONFIG)s" % paramToValue
PTM_CONFIG = "%(PTM_CONFIG)s" % paramToValue

PATH_TO_TOOLS = "%(PATH_TO_TOOLS)s" % paramToValue
TOOLS_INPUT = "%(TOOLS_INPUT)s" % paramToValue
TOOLS_OUTPUT = "%(TOOLS_OUTPUT)s" % paramToValue
REFERENCE_TXT = "%(REFERENCE_TXT)s" % paramToValue
FEATURE_MATRIX = "%(FEATURE_MATRIX)s" % paramToValue
REFERENCE_MATRIX = "%(REFERENCE_MATRIX)s" % paramToValue
PATH_TO_TMP =  "%(PATH_TO_TMP)s" % paramToValue
PATH_TO_TRAIN = "%(PATH_TO_TRAIN)s" % paramToValue
PATH_TO_TRAIN_REF = "%(PATH_TO_TRAIN_REF)s" % paramToValue
PATH_TO_TEST_REF = "%(PATH_TO_TEST_REF)s" % paramToValue
PATH_TO_R_AB = "%(PATH_TO_R_AB)s" % paramToValue
PATH_TO_R_MATCHES = "%(PATH_TO_R_MATCHES)s" % paramToValue
PATH_TRAIN_TMP = "%(PATH_TRAIN_TMP)s" % paramToValue




# clear method to empty directories and clean up
def cleanUp():
    #if dir is not empty delete files
    dirPath = [TOOLS_INPUT, TOOLS_OUTPUT, PATH_TO_TRAIN, PATH_TRAIN_TMP, PATH_TO_TMP, PATH_TO_TEST_REF]
    #iterate through list and delete files, if dir not empty
    for folder in dirPath:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                
                print e
            

    return







