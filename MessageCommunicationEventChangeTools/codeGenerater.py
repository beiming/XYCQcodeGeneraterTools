#coding=utf-8

import os,os.path as path,re,shutil
from xml.dom import minidom

#xml config
SrcDirAttributeName = 'SrcDir'
ObjEventXmlName = 'ObjEvent'
UnPackFunctionName = 'UnPackFunctionName'
UpackClassPrefix = 'UpackClassPrefix'
UpackClassFunc = 'UpackClassFunc'

#folder path
SrcDir = ''
YxEventFileName = 'Global/YXEvent.as'
YxUnpackFileName = 'Global/YXUnpacking.as'
OutPutDir = '\Global\SocketUnpack'
TemplateFileName = os.getcwd() + r'\template.as'
configXMLFileName = os.getcwd() + os.sep + 'config.xml'

#now event
ObjEvent = ''

#function match flag
UnPackPreifx = 'messageFunctionArray[YXEvent.EventStringSplite(YXEvent.'
EventMessageFlag = '#'
EventFuncFlag = '='
LeftBracket = '{'
RightBracket = '}'
LeftAnnotation = '/*'
RightAnnotation = '*/'
FunctionStatment = r'.*function +'

#template match
NewClassNameFlag = '$Classname$'
NewFuncNameFlag = '$unpack$'

def analyzeEventInfo():
    '''get massage id'''
    resultStr = None 
    YxEventFile = file(YxEventFileName, 'r')
    for lineStr in YxEventFile:
        if lineStr.find(ObjEvent) != -1:
            resultStr = lineStr.strip()
            break
    YxEventFile.close()
    if resultStr is not None:
        flagIndex = resultStr.rfind(EventMessageFlag) + 1
        return resultStr[flagIndex:-2]
    else:
        return None

def analyzeUnpackInfo():
    '''get function name'''
    resultStr = None
    YxUnpackFile = file(YxUnpackFileName, 'r')
    nowUnpackMessage = UnPackPreifx + ObjEvent
    for lineStr in YxUnpackFile:
        if lineStr.find(nowUnpackMessage) != -1:
            resultStr = lineStr.strip()
            break;
    YxUnpackFile.close()
    if resultStr is not None:
        flagIndex = resultStr.rfind(EventFuncFlag) + 1
        return resultStr[flagIndex:-1].lstrip()
    else:
        return None

def changeMessageFunction(className,funcName):
    '''change function name
    delete original function statement'''
    YxUnpackFile = file(YxUnpackFileName, 'r')
    allLines = YxUnpackFile.readlines()
    YxUnpackFile.close()
    nowUnpackMessage = UnPackPreifx + ObjEvent

    arrLen = len(allLines)
    #change function name
    nameIndex = -1
    for index in xrange(arrLen):
        if allLines[index].find(nowUnpackMessage) != -1:
            nameIndex = index
            tempStr = allLines[index].split(EventFuncFlag)
            tempStr[1] = tempStr[1].replace(funcName, className + UpackClassFunc)
            allLines[index] = EventFuncFlag.join(tempStr)
            break;
    if nameIndex == -1:
        return None

    #delete original function statement
    statement = findFuncStatment(allLines, funcName, index)
    if statement is None:
        print 'can\'t find the function declaration statement:\n%s' % (funcName)
        return None
    funcStatement = allLines[statement[0]:statement[1] + 1]
    for index in range(statement[0], statement[1] + 1):
        allLines[index] = ''

    YxUnpackFile = file(YxUnpackFileName, 'w')
    YxUnpackFile.writelines(allLines)
    YxUnpackFile.close()
    print 'The Original unpack function had replaced with: %s\nand function: %s had removed\n' % (className + UpackClassFunc, funcName)
    creatClassFile(className, funcStatement)

def findFuncStatment(lis, funcName, startIndex):
    '''find the function statment and annotation return [start, index] line num'''
    funcDeclarationIndex = -1
    funcDeclarationStartIndex = -1;
    arrLen = len(lis)
    pattern = FunctionStatment + funcName
    for index in xrange(startIndex,arrLen):
        if re.search(pattern, lis[index]) != None:
            lis[index] = lis[index].replace(funcName, UnPackFunctionName)
            if lis[index].find('private') != -1:
                lis[index] = lis[index].replace('private', 'public',1)
            elif lis[index].find('protected') != -1:
                lis[index] = lis[index].replace('protected', 'public',1)
            funcDeclarationIndex = index
            break;
    if funcDeclarationIndex == -1:
        return None

    #find the first left bracket line index {
    bracketMatch = -1
    leftBracketIndex = -1
    for index in xrange(funcDeclarationIndex,arrLen):
        if lis[index].find(LeftBracket) != -1:
            bracketMatch = 1
            leftBracketIndex = index + 1
            break;
    if leftBracketIndex == -1:
        return None

    #match brackets, find the function statement{}
    for index in xrange(leftBracketIndex, arrLen):
        if lis[index].find(LeftBracket) != -1:
            bracketMatch += 1
        if lis[index].find(RightBracket) != -1:
            bracketMatch -= 1
        if bracketMatch == 0:
            funcDeclarationEndIndex = index 
            break;
    if funcDeclarationEndIndex == -1:
        return None

    #find the last function end }
    for index in xrange(funcDeclarationIndex -1,-1,-1):
        if lis[index].find(RightBracket) != -1:
            funcDeclarationStartIndex = index + 1;
            break;
    if funcDeclarationIndex - funcDeclarationStartIndex > 30:
        return None

    #find this function annotation area
    for index in xrange(funcDeclarationStartIndex,funcDeclarationIndex):
        if lis[index].find(LeftAnnotation) != -1:
            funcDeclarationStartIndex = index;
            break;
    if funcDeclarationIndex - funcDeclarationStartIndex > 30:
        return None
    
    if funcDeclarationEndIndex - funcDeclarationStartIndex < 1:
        return None
    
    return (funcDeclarationStartIndex, funcDeclarationEndIndex)

def creatClassFile(className, lis):
    '''creat new file'''
    newClassFile =  OutPutDir + className + '.as'
    if os.path.exists(newClassFile):
        print 'File already exists:\n%s' % (newClassFile)
        return
    shutil.copy(TemplateFileName, newClassFile)

    newClass = file(newClassFile, 'r')
    allLines = newClass.readlines()
    newClass.close()

    arrLen = len(allLines)
    for index in xrange(arrLen):
        if allLines[index].find(NewClassNameFlag) != -1:
            allLines[index] = allLines[index].replace(NewClassNameFlag, className)
        elif allLines[index].find(NewFuncNameFlag) != -1:
            allLines[index] = allLines[index].replace(NewFuncNameFlag, ''.join(lis))
    
    newClass = file(newClassFile, 'w')
    newClass.writelines(allLines)
    newClass.close()

    print 'Creat Class:\n%s' % (newClassFile)

def init():
	'''init xml config'''
	global SrcDir, UnPackFunctionName, UpackClassPrefix, UpackClassFunc, ObjEvent
	configXMLDom = minidom.parse(configXMLFileName)
	root = configXMLDom.documentElement
	if root.hasAttribute(SrcDirAttributeName):
		SrcDir = root.attributes[SrcDirAttributeName].value
		SrcDir = unicode2utf8(SrcDir)
		if SrcDir == '':
			print '%s is empty' % (SrcDirAttributeName)
			return False
		else:
			SrcDir += os.altsep
			if os.path.exists(SrcDir):
				UnPackFunctionName = root.attributes[UnPackFunctionName].value
				UpackClassPrefix = root.attributes[UpackClassPrefix].value
				UpackClassFunc = root.attributes[UpackClassFunc].value
				
				UnPackFunctionName = unicode2utf8(UnPackFunctionName)
				UpackClassPrefix = unicode2utf8(UpackClassPrefix)
				UpackClassFunc = unicode2utf8(UpackClassFunc)
				
				for node in root.getElementsByTagName(ObjEventXmlName):
					if len(node.childNodes) > 0:
						ObjEvent = node.childNodes[0].data.strip()
						ObjEvent = unicode2utf8(ObjEvent)
						break;
				if ObjEvent == '':
					print '%s is empty' % (ObjEventXmlName)
					return False
				else:
					initVariable()
					return True
			else:
				print 'No such Folder:\n%s' % (SrcDir)
				return False
	else:
		print 'No attribute: %s' % (SrcDirAttributeName)
		return False
		
def initVariable():
	'''init path variable'''
	global SrcDir, YxEventFileName, YxUnpackFileName, OutPutDir
	YxEventFileName = SrcDir + YxEventFileName
	YxUnpackFileName = SrcDir + YxUnpackFileName
	OutPutDir = SrcDir + OutPutDir  + os.altsep
	
def unicode2utf8(str):
	'''python default Unicode to UTF-8'''
	return str.encode('utf-8')
	
def main():
	'''core function enter'''
	messageId = analyzeEventInfo()
	funcName = analyzeUnpackInfo()
	if messageId != None and funcName != None:
		print 'Find message Id: %s\nFind function name: %s\n' % (messageId, funcName)
		changeMessageFunction(UpackClassPrefix+messageId, funcName)
	else:
		print 'Error message Id: %s\nError function name: %s\n' % (messageId, funcName)
		
if __name__ == '__main__':
	if init() is True:
		pass
		main()
	
