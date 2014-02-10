import PredictionToolReader
import PredictionToolWriter
import Util
import PredictionToolExecuter


    

# create Sample file from Elude training
# sampleMatrix = PredictionToolReader.createMatrix("/home/shiller/PredictionTools/reference/")
# sampleMatrix = PredictionToolReader.modifyRetentionTimes(sampleMatrix)
# PredictionToolReader.writeMatrix(sampleMatrix, "/home/shiller/PredictionTools/Elude_Reference.mat")

# read created referenceFile, create featureMatrix
featureMatrix = PredictionToolWriter.readReference(Util.FEATURE_MATRIX)
   
# write reference to tool input 
tools = ["Elude", "SSRCalc", "BioLCCC"]
for tool in tools:
    PredictionToolWriter.writeToolInput(featureMatrix, Util.TOOLS_INPUT, tool)
    PredictionToolExecuter.factory(tool)
  
# write reference matrix, input R
toolMatrix = PredictionToolReader.createMatrix(Util.TOOLS_OUTPUT)
modToolMatrix = PredictionToolReader.modifyRetentionTimes(toolMatrix)
PredictionToolReader.writeMatrix(modToolMatrix, Util.REFERENCE_MATRIX)
