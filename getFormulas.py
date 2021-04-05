import cv2
import os, fnmatch
import re

from lxml import html, etree
import xml.etree.ElementTree as ET

from xml.dom import minidom

import random


def collectLatexFromFiles2(rootdir, dest):

    listOfFormulas = []
    fileNumber = 0
    count = 0
    count2 = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = str(subdir) + '/' + file
            with open(path, 'r') as reader:
                fileNumber = fileNumber + 1
                print(fileNumber, end=" ")
                if fileNumber%100 == 0:
                    print()

                line = reader.readline()
                while line:
                    regex = "encoding=\"application/x-tex\""
                    regexMatch = re.findall(regex, line)

                    if regexMatch != []:
                        line = reader.readline()
                        if not line:
                            break
                        
                        
                        line = line.strip() #remove white spaces before and after string
                        
                        if len(line) >= 2:
                            if line[-1] == '\\':
                                    line = "" # multiline not supported
                            elif line[-1] == '%':
                                line = "" # multiline not supported    

                        if len(line) > 2:
                            if line[-2] == '\\' and line[-1] == ',':
                                line = line[0:-2]
                            if line[-1] == ',':
                                line = line[0:-1]
                            if line[-1] == '%':
                                line = line[0:-1]

                        duplicate = False
                        for i in range(len(line)):
                            if line[i] == '\\':
                                if duplicate:
                                    line = line[:i] + line[i:] #cut of duplicate
                                    duplicate = False
                                else:
                                    duplicate = True
                            else:
                                duplicate = False


                        if line is not [] and line not in listOfFormulas:
                            listOfFormulas.append(line)
                    
                    regex = "<span class=\"LaTeX\">.*</span>"
                    regexMatch = re.findall(regex, line)
                    
                    for regIter in regexMatch:
                        line = regIter[20:-7]

                        #front $
                        for i in range(len(line)):
                            if line[i] != '$':
                                break
                        line = line[i:]

                        #back $
                        for i in range(len(line) - 1, -1, -1):
                            if line[i] != '$':
                                break
                        line = line[:i]

                        if len(line) >= 2:
                            if line[-2] == '\\':
                                    line = "" # multiline not supported

                        if len(line) > 2:
                            if line[-2] == '\\' and line[-1] == ',':
                                line = line[:-2]

                        if len(line) > 1:
                            if line[-1] == ',':
                                line = line[:-1]
                            if line[-1] == '%':
                                line = line[:-1]

                        line = line.strip()

                        duplicate = False
                        for i in range(len(line)):
                            if line[i] == '\\':
                                if duplicate:
                                    line = line[:i] + line[i:] #cut of duplicate
                                    duplicate = False
                                else:
                                    duplicate = True
                            else:
                                duplicate = False
                        
                        if line is not [] and line not in listOfFormulas:
                            listOfFormulas.append(line)
                            
                    line = reader.readline()
        count = count + 1
        if count >= 2:
            break
           

    with open(dest, 'w') as writer:
        for formula in listOfFormulas:
            writer.write(formula)
            writer.write("\n")
            








            

    with open(dest, 'w') as writer:
        for formula in listOfFormulas:
            writer.write(formula)
            writer.write("\n")
            
def collectLatexFromFiles0(rootdir, dest):

    listOfFormulas = []
    fileNumber = 0
    count = 0
    count2 = 0
    for subdir, dirs, files in os.walk(rootdir):
        print("---------", subdir, "---------")
        for file in files:
            path = str(subdir) + '/' + file
            with open(path, 'r') as reader:
                fileNumber = fileNumber + 1
                print(fileNumber, end=" ")
                if fileNumber%100 == 0:
                    print()

                line = reader.readline()
                while line:
                    regex = "encoding=\"application/x-tex\""
                    regexMatch = re.findall(regex, line)

                    if regexMatch != []:
                        line_formula = reader.readline()
                        if not line_formula:
                            break
                        line_end = reader.readline()
                        #if not line_end:
                        #    break

                        line_formula = line_formula.strip() #remove white spaces before and after string
                        line_end = line_end.strip() #remove white spaces before and after string
                        
                        regex_end = "</annotation>"
                        regexMatch = re.findall(regex_end, line_end)

                        if regexMatch != [] and len(line_formula) > 1:
                            if line_formula[-1] == '\\':
                                    line_formula = "" # multiline not supported

                            if line_formula is not "":
                                
                                asciiPass = True
                                formulaLen = len(line_formula)
                                i = 0
                                while i < formulaLen:
                                    char = line_formula[i]
                                    if ord(char) > 127:
                                        asciiPass = False
                                        break
                                    if char is '\\': # deleting white space with \ special sign
                                        if i < formulaLen - 1:
                                            if line_formula[i+1] == ' ':
                                                line_formula = line_formula[:i] + line_formula[i+1:]
                                                formulaLen = formulaLen - 1
                                            elif charUnrepresentative(line_formula[i+1]):
                                                line_formula = line_formula[:i] + line_formula[i+2:]
                                                formulaLen = formulaLen - 2
                                            
                                    i = i + 1            
                                
                                if asciiPass and line_formula not in listOfFormulas:
                                    line_formula = line_formula.strip()
                                    listOfFormulas.append(line_formula)
                                    
                    
                    #regex = "<span class=\"LaTeX\">.*</span>"
                    #regexMatch = re.findall(regex, line)

                    regex = "<span class=\"LaTeX\">.*</span>"
                    regexMatch = re.split(regex, line)
                    
                    if len(regexMatch) == 2:
                        lim_down = len(regexMatch[0])
                        lim_up = len(regexMatch[1])

                        line_formula = line[lim_down + 1 : lim_up]
                        line_formula = line_formula[20:-7] # got rid of <span..> </span>

                        for i in range(len(line)):
                            if line[i] != '$':
                                break
                        line = line[i:]

                        #back $
                        for i in range(len(line) - 1, -1, -1):
                            if line[i] != '$':
                                break
                        line = line[:i]

                        if line_formula is not "":
                                
                                asciiPass = True
                                formulaLen = len(line_formula)
                                i = 0
                                while i < formulaLen:
                                    char = line_formula[i]
                                    if ord(char) > 127:
                                        asciiPass = False
                                        break
                                    if char is '\\': # deleting white space with \ special sign
                                        if i < formulaLen - 1:
                                            if line_formula[i+1] == ' ':
                                                line_formula = line_formula[:i] + line_formula[i+1:]
                                                formulaLen = formulaLen - 1
                                            elif charUnrepresentative(line_formula[i+1]):
                                                line_formula = line_formula[:i] + line_formula[i+2:]
                                                formulaLen = formulaLen - 2
                                            
                                    i = i + 1            
                                
                                if asciiPass and line_formula not in listOfFormulas:
                                    line_formula = line_formula.strip()
                                    listOfFormulas.append(line_formula)
                    
                    
                            
                    line = reader.readline()
        #count = count + 1
        #if count >= 2:
        #    break
           

    with open(dest, 'w') as writer:
        for formula in listOfFormulas:
            writer.write(formula)
            writer.write("\n")

def collectLatexFromFiles(rootdir, dest):

    listOfFormulas = []
    fileNumber = 0
    count = 0
    count2 = 0
    for subdir, dirs, files in os.walk(rootdir):
        print("---------", subdir, "---------")
        for file in files:
            path = str(subdir) + '/' + file
            with open(path, 'r') as reader:
                fileNumber = fileNumber + 1
                print(fileNumber, file, end=" ")
                if fileNumber%100 == 0:
                    print()

                line = reader.readline()
                while line:
                    regex = "encoding=\"application/x-tex\""
                    regexMatch = re.findall(regex, line)

                    if regexMatch != []:
                        line_formula = reader.readline()
                        if not line_formula:
                            break
                        line_end = reader.readline()
                        #if not line_end:
                        #    break

                        line_formula = line_formula.strip() #remove white spaces before and after string
                        line_end = line_end.strip() #remove white spaces before and after string
                        
                        regex_end = "</annotation>"
                        regexMatch = re.findall(regex_end, line_end)

                        if regexMatch != [] and len(line_formula) > 1:
                            if line_formula[-1] == '\\':
                                    line_formula = "" # multiline not supported

                            if line_formula is not "":
                                regex_style = "style"
                                stylePos = line_formula.find(regex_style)
                                while stylePos != -1:
                                    #deleting style from line_formula
                                    line_formula = line_formula[:stylePos] \
                                        + line_formula[stylePos + len(regex_style):]

                                    i = stylePos - 1
                                    while line_formula[i] != '\\':
                                        i = i - 1
                                    line_formula = line_formula[:i] + line_formula[stylePos:]
                                    stylePos = line_formula.find(regex_style)

                                    line_formula = line_formula.strip()

                                regex_qquad = "\qquad"
                                stylePos = line_formula.find(regex_qquad)
                                while stylePos != -1:
                                        #deleting qquad from line_formula
                                        line_formula = line_formula[:stylePos] \
                                            + line_formula[stylePos + len(regex_qquad):]
                                        stylePos = line_formula.find(regex_qquad)
                                
                                line_formula = line_formula.strip()

                                regex_qquad = "% "
                                stylePos = line_formula.find(regex_qquad)
                                while stylePos != -1:
                                        #deleting qquad from line_formula
                                        line_formula = line_formula[:stylePos] \
                                            + line_formula[stylePos + len(regex_qquad):]
                                        stylePos = line_formula.find(regex_qquad)
                                
                                line_formula = line_formula.strip()

                                regex_qquad = "~{}"
                                stylePos = line_formula.find(regex_qquad)
                                while stylePos != -1:
                                        #deleting qquad from line_formula
                                        line_formula = line_formula[:stylePos] \
                                            + line_formula[stylePos + len(regex_qquad):]
                                        stylePos = line_formula.find(regex_qquad)
                                
                                line_formula = line_formula.strip()


                                asciiPass = True
                                formulaLen = len(line_formula)
                                i = 0
                                while i < formulaLen:
                                    char = line_formula[i]
                                    if ord(char) > 127:
                                        asciiPass = False
                                        break
                                    if char is '\\': # deleting white space with \ special sign
                                        if i < formulaLen - 1:
                                            if line_formula[i+1] == ' ':
                                                line_formula = line_formula[:i] + line_formula[i+1:]
                                                formulaLen = formulaLen - 1
                                            elif charUnrepresentative(line_formula[i+1]):
                                                line_formula = line_formula[:i] + line_formula[i+2:]
                                                formulaLen = formulaLen - 2
                                            
                                    i = i + 1            
                                
                                if asciiPass and line_formula not in listOfFormulas:
                                    line_formula = line_formula.strip()
                                    if len(line_formula) <= 64 and len(line_formula) > 1:
                                        listOfFormulas.append(line_formula)
                                    
                    
                    
                            
                    line = reader.readline()

            print(len(listOfFormulas))
            count = count + 1
            if count >= 50:
                with open(dest, 'a+') as writer:
                    for formula in listOfFormulas:
                        writer.write(formula)
                        writer.write("\n")
                    
                count = 0
                listOfFormulas = []

def charUnrepresentative(char):
    unrepChars = ['.', ',', ':', ';', '?', '!', '[', ']', '\\', '-', '_', '|', ')', '(']
    if char in unrepChars:
        return True
    else:
        return False

def deleteLinesLongerThan(lineMaxLength, path):
    c65 = 0
    c128 = 0
    with open(path, "r") as reader:
        with open(path+"1", "w") as writer: 
            for line in reader:
                if len(line.strip("\n")) <= lineMaxLength:
                    writer.write(line)
                elif len(line.strip("\n")) == 65:
                    c65 = c65 + 1
                elif len(line.strip("\n")) > 128:
                    c128 = c128 + 1

    print("dlugosci 65: ", c65)
    print("wieksze niz 128: ", c128)

    #with open(path, 'r+') as writer:
    #    line = writer.readline()
    #    while line:
    #        if len(line) <= lineMaxLength:
    #           writer.write(line)
    #    
    #        line = writer.readline()

def collect_dirtyLatexFromFiles(rootdir, dest):

    listOfFormulas = []
    fileNumber = 0
    count = 0
    count2 = 0
    for subdir, dirs, files in os.walk(rootdir):
        print("---------", subdir, "---------")
        for file in files:
            path = str(subdir) + '/' + file
            with open(path, 'r') as reader:
                fileNumber = fileNumber + 1
                print(fileNumber, end=" ")
                if fileNumber%100 == 0:
                    print()

                line = reader.readline()
                while line:
                    #regex = "<span class=\"LaTeX\">.*</span>"
                    #regexMatch = re.split(regex, line)
                    
                    split_line = line.split("<span class=\"LaTeX\">", 1)
                    if len(split_line) != 1:
                        line_formula = split_line[1]
                        line_formula = line_formula.split("</span>", 1)[0]

                        line_formula = line_formula.strip()

                        if len(line_formula) > 1: 
                            if line_formula[0] == '$':
                                if len(line_formula) > 2:
                                    if line_formula[1] == '$':
                                        line_formula = line_formula[2:]
                                    else:
                                        line_formula = line_formula[1:]
                                else:
                                    line_formula = line_formula[1:]
                            
                            if line_formula[-1] == '$':
                                if len(line_formula) > 2:
                                    if line_formula[-2] == '$':
                                        line_formula = line_formula[:-2]
                                    else:
                                        line_formula = line_formula[:-1]
                                else:
                                    line_formula = line_formula[:-1]

                        line_formula = line_formula.strip()

                        if len(line_formula) > 1: 
                            if line_formula[-1] == '\\':
                                        line_formula = "" # multiline not supported

                            if line_formula is not "":
                                regex_style = "array"
                                stylePos = line_formula.find(regex_style)
                                if stylePos != -1:
                                    line_formula = ""

                                regex_style = "style"
                                stylePos = line_formula.find(regex_style)
                                while stylePos != -1:
                                    #deleting style from line_formula
                                    line_formula = line_formula[:stylePos] \
                                        + line_formula[stylePos + len(regex_style):]

                                    i = stylePos - 1
                                    while line_formula[i] != '\\':
                                        i = i - 1
                                    line_formula = line_formula[:i] + line_formula[stylePos:]
                                    stylePos = line_formula.find(regex_style)

                                    line_formula.strip()

                                regex_qquad = "\qquad"
                                stylePos = line_formula.find(regex_qquad)
                                while stylePos != -1:
                                        #deleting qquad from line_formula
                                        line_formula = line_formula[:stylePos] \
                                            + line_formula[stylePos + len(regex_qquad):]
                                        stylePos = line_formula.find(regex_qquad)
                                line_formula.strip()


                            line_formula = line_formula.strip()

                            asciiPass = True
                            formulaLen = len(line_formula)
                            i = 0
                            while i < formulaLen:
                                char = line_formula[i]
                                if ord(char) > 127:
                                    asciiPass = False
                                    break
                                if char is '\\': # deleting white space with \ special sign
                                    if i < formulaLen - 1:
                                        if line_formula[i+1] == ' ':
                                            line_formula = line_formula[:i] + line_formula[i+1:]
                                            formulaLen = formulaLen - 1
                                        elif charUnrepresentative(line_formula[i+1]):
                                            line_formula = line_formula[:i] + line_formula[i+2:]
                                            formulaLen = formulaLen - 2
                                        
                                i = i + 1         

                           
                            if len(line_formula) > 1 and line_formula not in listOfFormulas:
                                line_formula = line_formula.strip()
                                listOfFormulas.append(line_formula)
                    
                          
                    line = reader.readline()


        #count = count + 1
        #if count >= 4:
        #    break
           

    with open(dest, 'w') as writer:
        for formula in listOfFormulas:
            writer.write(formula)
            writer.write("\n")

def cleanData(path, dest):
    listOfFormulas = []
    with open(path, 'r') as reader:
        line_formula = reader.readline()

        while line_formula:
            regex_style = "style"
            stylePos = line_formula.find(regex_style)
            while stylePos != -1:
                #deleting style from line_formula
                line_formula = line_formula[:stylePos] \
                    + line_formula[stylePos + len(regex_style):]

                i = stylePos - 1
                while line_formula[i] != '\\':
                    i = i - 1
                line_formula = line_formula[:i] + line_formula[stylePos:]
                stylePos = line_formula.find(regex_style)

                line_formula = line_formula.strip()

            regex_qquad = "\qquad"
            stylePos = line_formula.find(regex_qquad)
            while stylePos != -1:
                    #deleting qquad from line_formula
                    line_formula = line_formula[:stylePos] \
                        + line_formula[stylePos + len(regex_qquad):]
                    stylePos = line_formula.find(regex_qquad)
            
            line_formula = line_formula.strip()

            regex_qquad = "% "
            stylePos = line_formula.find(regex_qquad)
            while stylePos != -1:
                    #deleting qquad from line_formula
                    line_formula = line_formula[:stylePos] \
                        + line_formula[stylePos + len(regex_qquad):]
                    stylePos = line_formula.find(regex_qquad)
            
            line_formula = line_formula.strip()

            regex_qquad = "~{}"
            stylePos = line_formula.find(regex_qquad)
            while stylePos != -1:
                    #deleting qquad from line_formula
                    line_formula = line_formula[:stylePos] \
                        + line_formula[stylePos + len(regex_qquad):]
                    stylePos = line_formula.find(regex_qquad)
            
            line_formula = line_formula.strip()

            asciiPass = True
            formulaLen = len(line_formula)
            i = 0
            while i < formulaLen:
                char = line_formula[i]
                if ord(char) > 127: #clean special symbols
                    asciiPass = False
                    break
                if char is '\\': # deleting white space with \ special sign
                    if i < formulaLen - 1:
                        if line_formula[i+1] == ' ':
                            line_formula = line_formula[:i] + line_formula[i+1:]
                            formulaLen = formulaLen - 1
                        elif charUnrepresentative(line_formula[i+1]):
                            line_formula = line_formula[:i] + line_formula[i+2:]
                            formulaLen = formulaLen - 2
                        
                i = i + 1

            #delete more than one inner space
            line_formula = re.sub(' +', ' ', line_formula)
            
            if asciiPass:
                line_formula = line_formula.strip()
                if len(line_formula) <= 64 and len(line_formula) > 1:
                    listOfFormulas.append(line_formula)

            line_formula = reader.readline()
           

    with open(dest, 'a+') as writer:
        for formula in listOfFormulas:
            writer.write(formula)
            writer.write("\n")

def extractTrainTestSets(fromFile, toTestF, toTrainF, procTest):
    if procTest > 1:
        print("size of test set is too big")
        exit(0)

    numOfLines = sum(1 for line in open(fromFile))
    sizeOfTestSet = int(numOfLines * procTest)
    randLineNumbers = random.sample(range(1, numOfLines), sizeOfTestSet)
    randLineNumbers.sort()
    indexLine = 0
    lineNumberToExtract = randLineNumbers[indexLine]

    linesToTest  = []
    linesToTrain = []
    with open(fromFile, 'r') as reader:
        for lineNumber, line in enumerate(reader):
            if lineNumber == lineNumberToExtract:
                linesToTest.append(line)

                if indexLine < sizeOfTestSet - 1:
                    indexLine = indexLine + 1
                    lineNumberToExtract = randLineNumbers[indexLine]
            else:
                linesToTrain.append(line)
    
    with open(toTrainF, 'w') as writer:
        for line in linesToTrain:
            writer.write(line)

    with open(toTestF, 'w') as writer:
        for line in linesToTest:
            writer.write(line)

