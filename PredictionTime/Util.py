import ConfigParser


TOOL_CONFIG = "/home/shiller/PredictionTools/config/ToolParam.conf"
PTM_CONFIG = "/home/shiller/PredictionTools/config/PTM.conf"

PATH_TO_TOOLS = "/home/shiller/PredictionTools/"
TOOLS_INPUT = "/home/shiller/PredictionTools/input/"
TOOLS_OUTPUT = "/home/shiller/PredictionTools/output/"
REFERENCE_TXT = "/home/shiller/PredictionTools/reference/Reference.txt"
FEATURE_MATRIX = "/home/shiller/PredictionTools/Feature_Reference.mat"
REFERENCE_MATRIX = "/home/shiller/PredictionTools/R_Reference.mat"
PATH_TO_REFERENCE = "/home/shiller/PredictionTools/reference/"
PATH_TO_TMP =  "/home/shiller/PredictionTools/tmp/"
PATH_TO_TRAIN = "/home/shiller/PredictionTools/train/"
PATH_TO_TRAIN_REF = "/home/shiller/PredictionTools/train_ref/"
PATH_TO_TEST_REF = "/home/shiller/PredictionTools/test_ref/"
PATH_TO_R = "/home/shiller/git/RetentionRepo/PredictionTime/regression.R"
PATH_TRAIN_TMP = "/home/shiller/PredictionTools/train_tmp/"

def readConfigFile(pathToConfig, tool):
        
    valueToKey = {}
    
    parser = ConfigParser.ConfigParser()
    parser.read(pathToConfig)
    
    for key in parser.options(tool):
        valueToKey[key] = parser.get(tool, key)
    
    return valueToKey





