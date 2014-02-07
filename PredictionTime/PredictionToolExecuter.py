# this class will execute the tools, create/overwrite outputFilesToolname.txt (besser: filename = TOOL+zeitangabe) 

import Util
 
#input for tools 
pathInput = Util.PATH_TO_TOOLS+"input/"
#output for tools; required for PredictionToolReader.createMatrix(path) 
pathOutput = Util.PATH_TO_TOOLS+"output/"

import Util
from pyteomics import biolccc
import os, re
import subprocess


#callTool with standard settings of tool

def callTool(tool):
    check = 0
    if tool == "BioLCCC":
        fnameRT = os.path.join(pathInput+tool+'.txt')
        fobjIn = open(fnameRT, 'r')
        fobjOut = open(pathOutput+tool+'.txt', 'w')
        #Peptide mit Retentionszeit ausgeben  
        for line in fobjIn:
            if check :
                print line.rstrip()     
            
            peptide = line.rstrip()
            # no C-/N-terminal group
            peptide = peptide.split("-")[1]
           
            RT = biolccc.calculateRT(peptide, biolccc.rpAcnFaRod, biolccc.standardChromoConditions)
            if check :
                print 'RT of', peptide, 'is\t\t', RT
            
            fobjOut.write(peptide + "\t" + str(RT) + "\n")
        
        fobjIn.close() 
        fobjOut.close() 
        
        
          
#     if tool == "SSRCalc":
#         fnameRT = os.path.join(pathInput+tool+'.txt')
#         fobjIn = open(fnameRT, 'r')
#         fobjOut = open(pathOutput+tool+'.txt', 'w')
#           
#         pleaseDo2 = os.system('cd src/SSRCalc/') 
#         umschreiben zu platzhaltervariablem
#         pleaseDo3 = os.system("/home/shiller/src/SSRCalc/"+"SSRCalc3.pl --alg 3.0 --source '/home/shiller/workspace/Tools/prediction_tools/input/SSRCalc.txt' --output tsv > '/home/shiller/workspace/Tools/prediction_tools/output/SSRCalcUnmod.txt'")
#        
#         pleaseDo2.wait() #warte bis process zuende
#         trimPath = '/home/shiller/workspace/Tools/prediction_tools/output/SSRCalcUnmod.txt'
#         trim(trimPath)
         
          
      
# trim SSRCalc output for PredictionToolReader.createMatrix()   
def trim(path):        
        # trim SSRCalc Output 
        fnameRT = path
        fobjIn = open(fnameRT, 'r')
        fobjOut = open('/home/shiller/workspace/Tools/prediction_tools/output/SSRCalc.txt', 'w')
        
        check = 0
        
        #Peptide mit Retentionszeit ausgeben  
        for line in fobjIn:
            if check :
                print line.rstrip()     
            
            data = re.split('\s+', line)
            seq = data[0]
            rt = data[2] 
        
            fobjOut.write(seq + "\t" + rt +"\n")
            print data    
        fobjIn.close() 
        fobjOut.close() 



# tools = ["Elude", "SSRCalc", "BioLCCC"]
# for tool in tools:
#     callTool(tool)

cmd = "elude -t /home/shiller/src/ELUDE/train.txt -e /home/shiller/src/ELUDE/test.txt -o /home/shiller/workspace/Tools/prediction_tools/output/Elude.txt -v 5"
# cmd1 = biolccc
# cmd2 = ssrcalc
# TODO je nachdem was fuer ein tool gewaehlt wurde
os.system(cmd)






