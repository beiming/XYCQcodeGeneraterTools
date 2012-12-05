#coding=utf-8import os,os.path as path,re,shutilfrom xml.dom import minidom#xml configSrcDirAttributeName = 'SrcDir'ObjEventXmlName = 'ObjEvent'UnPackFunctionName = 'UnPackFunctionName'UpackClassPrefix = 'UpackClassPrefix'UpackClassFunc = 'UpackClassFunc'SendPackFunctionName = 'SendPackFunctionName'SendPackClassPrefix = 'SendPackClassPrefix'SendPackClassFunc = 'SendPackClassFunc'ReplaceFunctionName = {}ReplaceClassPrefix = {}ReplaceClassFunc = {}#now eventObjEvent = ''NowFlag = ''SendFlag = 'send'UnpackFlag = 'unpack'#folder pathSrcDir = ''YxEventFileName = 'Global\YXEvent.as'CommunicationFileName = {UnpackFlag: 'Global\YXUnpacking.as', SendFlag: 'Global\YXPackSend.as'}OutPutDir = {UnpackFlag: 'Global\SocketUnpack', SendFlag: 'Global\SocketSendpack'}TemplateFileName = {UnpackFlag: os.getcwd() + r'\unPackTemplate.as', SendFlag: os.getcwd() + r'\sendPackTemplate.as'}configXMLFileName = os.getcwd() + os.sep + 'config.xml'#function match flagCommunicationPreifx = {UnpackFlag: 'messageFunctionArray[YXEvent.EventStringSplite(YXEvent.', SendFlag: 'YXAPI.dispatcher.addEventListener(YXEvent.'}FunctionStatment = r'.*function +'CommunicationEventFlag = {UnpackFlag: '=', SendFlag: ','}CommunicationEventFlagEnd = {UnpackFlag: ';', SendFlag: ')'}EventMessageFlag = '#'LeftBracket = '{'RightBracket = '}'LeftAnnotation = '/*'RightAnnotation = '*/'#template matchNewClassNameFlag = '$Classname$'NewFuncNameFlag = {UnpackFlag: '$unpack$', SendFlag: '$send$'}def analyzeEventInfo():    '''get massage id'''    resultStr = None     YxEventFile = file(YxEventFileName, 'r')    for lineStr in YxEventFile:        if lineStr.find(ObjEvent) != -1:            resultStr = lineStr.strip()            break    YxEventFile.close()    if resultStr is not None:        flagIndex = resultStr.rfind(EventMessageFlag) + 1        return resultStr[flagIndex:-2]    else:        return Nonedef analyzeFunctionInfo(pNowFlag):    '''get function name'''    global NowFlag    resultStr = None    NowFlag = pNowFlag    YxUnpackFile = file(CommunicationFileName[NowFlag], 'r')    nowUnpackMessage = CommunicationPreifx[NowFlag] + ObjEvent    for lineStr in YxUnpackFile:        if lineStr.find(nowUnpackMessage) != -1:            resultStr = lineStr.strip()            break;    YxUnpackFile.close()    if resultStr is not None:        flagStart = resultStr.rfind(CommunicationEventFlag[NowFlag]) + 1        flagEnd = resultStr.rfind(CommunicationEventFlagEnd[NowFlag])        return resultStr[flagStart:flagEnd].strip()    else:        return Nonedef changeMessageFunction(messageId,funcName):    '''change function name    delete original function statement'''    className = ReplaceClassPrefix[NowFlag]+messageId    YxUnpackFile = file(CommunicationFileName[NowFlag], 'r')    allLines = YxUnpackFile.readlines()    YxUnpackFile.close()    nowUnpackMessage = CommunicationPreifx[NowFlag] + ObjEvent    arrLen = len(allLines)    #change function name    nameIndex = -1    for index in xrange(arrLen):        if allLines[index].find(nowUnpackMessage) != -1:            nameIndex = index            tempStr = allLines[index].split(CommunicationEventFlag[NowFlag])            if NowFlag == UnpackFlag:                tempStr[0] = tempStr[0].replace('YXEvent.EventStringSplite(YXEvent.' + ObjEvent + ')', messageId)            else:                #tempStr[0] = tempStr[0].replace('YXEvent.' + ObjEvent, messageId)                pass            tempStr[1] = tempStr[1].replace(funcName, className + ReplaceClassFunc[NowFlag])            allLines[index] = CommunicationEventFlag[NowFlag].join(tempStr)            break;    if nameIndex == -1:        return None    #delete original function statement    statement = findFuncStatment(allLines, funcName, index)    if statement is None:        print 'can\'t find the function declaration statement:\n%s' % (funcName)        return None    funcStatement = allLines[statement[0]:statement[1] + 1]    for index in range(statement[0], statement[1] + 1):        allLines[index] = ''    YxUnpackFile = file(CommunicationFileName[NowFlag], 'w')    YxUnpackFile.writelines(allLines)    YxUnpackFile.close()    print 'The Original unpack function had replaced with: %s\nand function: %s had removed\n' % (className + UpackClassFunc, funcName)    creatClassFile(className, funcStatement)def findFuncStatment(lis, funcName, startIndex):    '''find the function statment and annotation return [start, index] line num'''    funcDeclarationIndex = -1    funcDeclarationStartIndex = -1;    arrLen = len(lis)    pattern = FunctionStatment + funcName    for index in xrange(startIndex,arrLen):        if re.search(pattern, lis[index]) != None:            lis[index] = lis[index].replace(funcName, ReplaceFunctionName[NowFlag])            if lis[index].find('private') != -1:                lis[index] = lis[index].replace('private', 'public',1)            elif lis[index].find('protected') != -1:                lis[index] = lis[index].replace('protected', 'public',1)            funcDeclarationIndex = index            break;    if funcDeclarationIndex == -1:        return None    #find the first left bracket line index {    bracketMatch = -1    leftBracketIndex = -1    for index in xrange(funcDeclarationIndex,arrLen):        if lis[index].find(LeftBracket) != -1:            bracketMatch = 1            leftBracketIndex = index + 1            break;    if leftBracketIndex == -1:        return None    #match brackets, find the function statement{}    for index in xrange(leftBracketIndex, arrLen):        if lis[index].find(LeftBracket) != -1:            bracketMatch += 1        if lis[index].find(RightBracket) != -1:            bracketMatch -= 1        if bracketMatch == 0:            funcDeclarationEndIndex = index             break;    if funcDeclarationEndIndex == -1:        return None    #find the last function end }    for index in xrange(funcDeclarationIndex -1,-1,-1):        if lis[index].find(RightBracket) != -1:            funcDeclarationStartIndex = index + 1;            break;    if funcDeclarationIndex - funcDeclarationStartIndex > 30:        return None    #find this function annotation area    for index in xrange(funcDeclarationStartIndex,funcDeclarationIndex):        if lis[index].find(LeftAnnotation) != -1:            funcDeclarationStartIndex = index;            break;    if funcDeclarationIndex - funcDeclarationStartIndex > 30:        return None        if funcDeclarationEndIndex - funcDeclarationStartIndex < 1:        return None        return (funcDeclarationStartIndex, funcDeclarationEndIndex)def creatClassFile(className, lis):    '''creat new file'''    newClassFile =  OutPutDir[NowFlag] + className + '.as'    if os.path.exists(newClassFile):        print 'File already exists:\n%s' % (newClassFile)        return    shutil.copy(TemplateFileName[NowFlag], newClassFile)    newClass = file(newClassFile, 'r')    allLines = newClass.readlines()    newClass.close()    arrLen = len(allLines)    for index in xrange(arrLen):        if allLines[index].find(NewClassNameFlag) != -1:            allLines[index] = allLines[index].replace(NewClassNameFlag, className)        elif allLines[index].find(NewFuncNameFlag[NowFlag]) != -1:            allLines[index] = allLines[index].replace(NewFuncNameFlag[NowFlag], ''.join(lis))        newClass = file(newClassFile, 'w')    newClass.writelines(allLines)    newClass.close()    print 'Creat Class:\n%s' % (newClassFile)def init():	'''init xml config'''	global SrcDir, UnPackFunctionName, UpackClassPrefix, UpackClassFunc, ObjEvent, SendPackFunctionName, SendPackClassPrefix, SendPackClassFunc	configXMLDom = minidom.parse(configXMLFileName)	root = configXMLDom.documentElement	if root.hasAttribute(SrcDirAttributeName):		SrcDir = root.attributes[SrcDirAttributeName].value		SrcDir = unicode2utf8(SrcDir)		if SrcDir == '':			print '%s is empty' % (SrcDirAttributeName)			return False		else:			SrcDir += os.altsep			if os.path.exists(SrcDir):				UnPackFunctionName = root.attributes[UnPackFunctionName].value				UpackClassPrefix = root.attributes[UpackClassPrefix].value				UpackClassFunc = root.attributes[UpackClassFunc].value				SendPackFunctionName = root.attributes[SendPackFunctionName].value				SendPackClassPrefix = root.attributes[SendPackClassPrefix].value				SendPackClassFunc = root.attributes[SendPackClassFunc].value								UnPackFunctionName = unicode2utf8(UnPackFunctionName)				UpackClassPrefix = unicode2utf8(UpackClassPrefix)				UpackClassFunc = unicode2utf8(UpackClassFunc)				SendPackFunctionName = unicode2utf8(SendPackFunctionName)				SendPackClassPrefix = unicode2utf8(SendPackClassPrefix)				SendPackClassFunc = unicode2utf8(SendPackClassFunc)								for node in root.getElementsByTagName(ObjEventXmlName):					if len(node.childNodes) > 0:						ObjEvent = node.childNodes[0].data.strip()						ObjEvent = unicode2utf8(ObjEvent)						break;				if ObjEvent == '':					print '%s is empty' % (ObjEventXmlName)					return False				else:					initVariable()					return True			else:				print 'No such Folder:\n%s' % (SrcDir)				return False	else:		print 'No attribute: %s' % (SrcDirAttributeName)		return False		def initVariable():    '''init path variable'''    global SrcDir, YxEventFileName, CommunicationFileName, OutPutDir, ReplaceFunctionName, ReplaceClassPrefix, ReplaceClassFunc    YxEventFileName = SrcDir + YxEventFileName    CommunicationFileName[UnpackFlag] = SrcDir + CommunicationFileName[UnpackFlag]    CommunicationFileName[SendFlag] = SrcDir + CommunicationFileName[SendFlag]    OutPutDir[UnpackFlag] = SrcDir + OutPutDir[UnpackFlag] + os.altsep    OutPutDir[SendFlag] = SrcDir + OutPutDir[SendFlag] + os.altsep    ReplaceFunctionName[UnpackFlag] = UnPackFunctionName    ReplaceFunctionName[SendFlag] = SendPackFunctionName    ReplaceClassPrefix[UnpackFlag] = UpackClassPrefix    ReplaceClassPrefix[SendFlag] = SendPackClassPrefix    ReplaceClassFunc[UnpackFlag] = UpackClassFunc    ReplaceClassFunc[SendFlag] = SendPackClassFunc    #print ('%s\n%s\n%s\n%s\n%s\n%s\n%s\n') %( SrcDir, YxEventFileName, CommunicationFileName,OutPutDir, ReplaceFunctionName, ReplaceClassPrefix, ReplaceClassFunc)	def unicode2utf8(str):	'''python default Unicode to UTF-8'''	return str.encode('utf-8')	def main():    '''core function enter'''    messageId = analyzeEventInfo()    funcName = analyzeFunctionInfo(UnpackFlag)    if funcName is None:        funcName = analyzeFunctionInfo(SendFlag)    if messageId != None and funcName != None:        print 'Find message Id: %s\nFind function name: %s\n' % (messageId, funcName)        changeMessageFunction(messageId, funcName)    else:        print 'Error message Id: %s\nError function name: %s\n' % (messageId, funcName)		if __name__ == '__main__':	if init() is True:		pass		main()	