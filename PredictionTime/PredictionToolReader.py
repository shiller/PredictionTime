import os
import re



check = 0

# tool and sequence to looking for
def getSequence(tool, modSequence):
    sequence=" "
    
    if tool == "BioLCCC":
        sequence = modSequence.split("-")[1]
        
    elif tool == "SSRCalc":
        sequence = modSequence.split("\s+")[0]
                                  
    elif tool == "Elude":
        sequence = modSequence.split(".")[1]
      
    else:
        sequence = modSequence
   
    return sequence


def removeHeader(tool, content):
    if tool == "Elude":
        content = content[3:]
        
    if tool == "Reference":
        content = content[1:]

    return content
    

# Author: Sarah Hiller
# This createMatrix.py returns a matrix out of [calculated] toolOUTPUT
# Return: matrix[sequence, retention time 1, ..., retention time n]
#     methods:
#         writeMatrix(matrix) tabdelimitted to an external file .txt
#         createMatrix(pathOUT) searches for input data and creates a matrix with sequences and the rt
#         modifyRetentionTimes(matrix) modifies created matrix; rounds and trims rt


# create matrix out of dict with tools given in filename(s) of path; Elude.txt, Elude.mat
def createMatrix(path):
    dirContent = os.listdir(path)
    
    validContentLines = 0   
    tools = []
    toolIndex = 0 
    # initialize dict
    sequenceToRetentionTimes = {}
        
    header = [] 
    header.append("Sequences")
    # initialize header
    for fName in dirContent:
        if "~" in fName: continue  
        tool = fName.split(".")[0]
        header.append(tool+" RT [min]")
    
    #join filepath to read file content
    for fName in dirContent: 
        if "~" in fName: continue 
        tool = fName.split(".")[0]
        absolute_path = os.path.join(path, fName)
        content = []
        if check:
            print "Tool: "+tool
            print toolIndex       

        #    progress        
        # content of all files PATH in an unformatted array; index+=1 after every file/tool
        if os.path.isfile(absolute_path):
            with open(absolute_path, 'r') as output:
                content = output.readlines()
                content = removeHeader(tool, content)
                
                # content not empty, then parse and format; toolname (column) append on header
                if len(content) != 0:
                    tools.append(tool)                    
                    
                    # split content (sequences, rt, ...) of file; space, tab delimitted; data=list/array
                    for fileLine in content:
                        modFileLine = fileLine.strip()
                        data = re.split('\s+', modFileLine)
                        
                        modSequence = data[0]
                        rt = data[1]
                       
                        # get clean sequence (depends on tool how to trim) 
                        sequence = getSequence(tool, modSequence)   
                        
                        # check if sequence in dict, else add initialized row
                        if sequence in sequenceToRetentionTimes:
                            retentionTimes = sequenceToRetentionTimes[sequence] 
                            retentionTimes[toolIndex] = rt
                         
                        if sequence not in sequenceToRetentionTimes:
                            # initialize row; retention time of valid tools
                            validTools = len(header) - 1
                            retentionTimes = [-1] * validTools #create column(s)
                            retentionTimes[toolIndex] = rt #assign rt to toolindex
                            # fill dict; add rt[] to "sequence"
                            sequenceToRetentionTimes[sequence] = retentionTimes

                    validContentLines += 1
                              
        toolIndex += 1
    # create matrix as return value    
    matrix = []
    matrix.append(header)
    
    # append in matrix sequence, retentionTime value(s)
    for sequence in sequenceToRetentionTimes:
        row = []
        row.append(sequence) #just one value for a row
        
        for retentionTime in sequenceToRetentionTimes[sequence]:
            row.append(retentionTime) #one or more values (depends on validTools)
        matrix.append(row)
    
    return matrix
    
    # Exception file contents
    if validContentLines % len(tools) != 0:
        print "Exception File Contents (different length)"


#modifies matrix content
def modifyRetentionTimes(matrix):
    #round on .4 and fill with 0
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            firstChar = str(matrix[row][column])[0]
            #print firstChar
            if firstChar.isdigit():
                modRt = '{:.4f}'.format(round(float(matrix[row][column]), 4))
                matrix[row][column] = modRt
     
    return matrix


#write matrix in file format tab delimited      
def writeMatrix(matrix, out):
    #create file
    matFileOut = open(out, 'w')
    
    for row in matrix:
        rowStr = ""
        for column in range(len(row)):
            rowStr += str(row[column]) + '\t'
        matFileOut.write(rowStr.strip())   
        matFileOut.write('\n')
        
    matFileOut.close()
 




   
