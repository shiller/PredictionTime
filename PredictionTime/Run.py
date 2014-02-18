import Util
import PredictionToolExecuter
import PredictionToolWriter
import PredictionToolReader



# read all refTrainingFiles
allRefMat = PredictionToolWriter.readReference(Util.PATH_TO_TRAIN_REF)
# write concatenated trainfile as Reference.txt
PredictionToolReader.writeMatrix(allRefMat, Util.REFERENCE_TXT)
# take REFERENCE_TXT and create train & test files if PATH_TO_TEST+empty)

# create random_train_set
PredictionToolWriter.createSampleFile(Util.PATH_TO_REFERENCE)
# create toolinput for train 
trainMatrix = PredictionToolReader.createMatrix(Util.PATH_TRAIN_TMP)
trainMatrix = PredictionToolReader.modifyRetentionTimes(trainMatrix)
tools = ["Elude", "SSRCalc", "BioLCCC"]
for tool in tools:
    PredictionToolWriter.writeToolInput(trainMatrix, Util.PATH_TO_TRAIN, tool)
 
 
# # create toolinput for test
# #create test file content out of train put in PATH_TO_TEST_REF
testMatrix = PredictionToolReader.createMatrix(Util.PATH_TO_TEST_REF)
testMatrix = PredictionToolReader.modifyRetentionTimes(testMatrix)
tools = ["Elude", "SSRCalc", "BioLCCC"]
for tool in tools:
    PredictionToolWriter.writeToolInput(testMatrix, Util.TOOLS_INPUT, tool)
    PredictionToolExecuter.factory(tool)
 
toolMatrix = PredictionToolReader.createMatrix(Util.TOOLS_OUTPUT)
 
modToolMatrix = PredictionToolReader.modifyRetentionTimes(toolMatrix)
PredictionToolReader.writeMatrix(modToolMatrix, Util.REFERENCE_MATRIX)
 

