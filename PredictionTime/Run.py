import Util
import PredictionToolExecuter
import PredictionToolWriter
import PredictionToolReader
import FileReader


Util.cleanUp()
# create RMatrix with matches of modified phosphosites 
FileReader.modifyPeptides()
#  read matches (modified) or all files in dir
allRefMat = PredictionToolWriter.readReference(Util.PATH_TO_TRAIN_REF)

#  TODO: take MATCHES.txt and create train & test files if PATH_TO_TEST+empty)
#  create random_trainset and testset with RT
PredictionToolWriter.createSampleFile(Util.PATH_TO_TRAIN_REF)
#  create toolinput for train 


# create matrix out of file; HEADER! oder mit writeMatrix, dann header weg
trainMatrix = PredictionToolWriter.readReference(Util.PATH_TRAIN_TMP)   
trainMatrix = PredictionToolReader.modifyRetentionTimes(trainMatrix)

tools = ["Elude", "SSRCalc", "BioLCCC"]
for tool in tools:
    PredictionToolWriter.writeTrainInput(trainMatrix, Util.PATH_TO_TMP, tool) #neue spalte einfuegen mit ID als modifi.Seq mit RT und toolinputseq zeigt auf modifi.Seq
    
 # create toolinput for test; HEADER!
testMatrix = PredictionToolWriter.readReference(Util.PATH_TO_TEST_REF)
testMatrix = PredictionToolReader.modifyRetentionTimes(testMatrix)
tools = ["Elude", "SSRCalc", "BioLCCC"]
for tool in tools:
    PredictionToolWriter.writeToolInput(testMatrix, Util.TOOLS_INPUT, tool)
    PredictionToolExecuter.factory(tool)
    
toolMatrix = PredictionToolReader.createMatrix(Util.TOOLS_OUTPUT)
    
modToolMatrix = PredictionToolReader.modifyRetentionTimes(toolMatrix)
PredictionToolReader.writeMatrix(modToolMatrix, Util.REFERENCE_MATRIX)
    

