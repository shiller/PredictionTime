import ConfigParser

TOOL_CONFIG = "/home/shiller/PredictionTools/config/ToolParam.conf"
PTM_CONFIG = "/home/shiller/PredictionTools/config/PTM.conf"

PATH_TO_TOOLS = "/home/shiller/PredictionTools/"
TOOLS_INPUT = "/home/shiller/PredictionTools/input/"
TOOLS_OUTPUT = "/home/shiller/PredictionTools/output/"
FEATURE_MATRIX = "/home/shiller/PredictionTools/Elude_Reference.mat"
REFERENCE_MATRIX = "/home/shiller/PredictionTools/R_Reference.mat"


def readConfigFile(pathToConfig, tool):
        
    valueToKey = {}
    
    parser = ConfigParser.ConfigParser()
    parser.read(pathToConfig)
    
    for key in parser.options(tool):
        valueToKey[key] = parser.get(tool, key)
    
    return valueToKey

