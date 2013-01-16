#coding=utf-8
import re,shutil,os, codecs, os.path as path
from GameMapInfo import GameMapInfo
from MapInfo import MapInfo
from xml.dom import minidom

resourceXML = 'qiqingXML'
objectXML = 'qiqingXMLOK'
resourceXMLPath = path.abspath(path.pardir) + os.sep + resourceXML
objectXMLPath = path.abspath(path.pardir) + os.sep + objectXML
def findResourceXML(gameMapDict):

	dirList =  os.listdir(resourceXMLPath)
	resourceXMLDict =dict([(fileName.split('_')[0], resourceXMLPath + os.sep + fileName)  for fileName in dirList if path.splitext(fileName)[1].lower() == '.xml'])
	
	for gameMapInfoKey in gameMapDict:
		gameMapInfo = gameMapDict[gameMapInfoKey]
		computeResourceXML(resourceXMLDict[gameMapInfoKey], gameMapInfo)


def praseGameMapInfo(mapInfo):
	gameMapInfoXML = 'gameMapInfo.xml'
	gameMapInfoDom = minidom.parse(gameMapInfoXML)
	#获取跟节点
	root = gameMapInfoDom.documentElement
	
	#获取跟节点的属性值
	GameMapInfo.pointSplit = root.attributes['pointSplit'].value
	GameMapInfo.transSplit = root.attributes['transSplit'].value
	GameMapInfo.transFlag = root.attributes['transFlag'].value
	
	gameMapDict = {}
	for node in root.childNodes:
		#判断是不是ELEMENT_NODE
		 if node.nodeType == node.ELEMENT_NODE:
			 id = node.getAttribute('id')
			 imageTemplate = node.getAttribute('imageTemplate')
			 delpoint = node.getAttribute('delpoint')
			 name = node.getAttribute('name')
			 transToId = node.getAttribute('transTo')
			 gameMapInfo = GameMapInfo(id, imageTemplate, delpoint, name, mapInfo[imageTemplate],transToId)	
			 gameMapDict[gameMapInfo.id] = gameMapInfo
			 
	for gameMapInfoKey in gameMapDict:
		gameMapInfo = gameMapDict[gameMapInfoKey]
		if gameMapInfo.transToId in gameMapDict:
			gameMapInfo.setTransTo(gameMapDict[gameMapInfo.transToId])
		else:
			gameMapInfo.setTransTo(None)		
	
	gameMapInfoDom.unlink()
	return gameMapDict
	
def praseMapInfo():
	mapInfoXML = 'mapInfo.xml'
	mapInfoDom = minidom.parse(mapInfoXML)
	root = mapInfoDom.documentElement
	
	MapInfo.pointSplit = root.attributes['pointSplit'].value
	MapInfo.pointArrSplit = root.attributes['pointArrSplit'].value
	MapInfo.pointArrSplitout = root.attributes['pointArrSplitout'].value
	MapInfo.transFlag = root.attributes['transFlag'].value
	
	
	mapDict = {}		
	for node in root.childNodes:
		if node.nodeType == node.ELEMENT_NODE:
			id = node.getAttribute('id')
			point1 = node.getAttribute('point1')
			point2 = node.getAttribute('point2')
			point1Arr = node.getElementsByTagName('point1Arr')[0].firstChild.data.strip()
			point2Arr = node.getElementsByTagName('point2Arr')[0].firstChild.data.strip()
			mapInfo = MapInfo(id, point1, point2, point1Arr, point2Arr)
			mapDict[mapInfo.id] = mapInfo
			#for pointArr in node.childNodes:
			#if pointArr.nodeType == node.ELEMENT_NODE:
			#print pointArr.firstChild.data.strip()
	mapInfoDom.unlink()
	return mapDict
	
	
		
def computeResourceXML(fileName, gameMapInfo):
	xmlDom = minidom.parse(fileName)
	mapXml = xmlDom.getElementsByTagName('Map')[0]
	TerrainTxt = mapXml.getAttribute('Terrain')
	
	print fileName
	for pointTxt in gameMapInfo.getDeletePoints():
		TerrainTxt = replaceTransPoint(pointTxt , gameMapInfo.getDeleteText(), TerrainTxt)
	
	for pointTxt in gameMapInfo.getReplacePoints():
		if gameMapInfo.transToInfo:
			repTex = pointTxt[:-1] + gameMapInfo.transToInfo
		else:
			repTex = ''
		TerrainTxt = replaceTransPoint(pointTxt, repTex, TerrainTxt)
		
	mapXml.setAttribute('Terrain', TerrainTxt)
	mapXml.setAttribute('name', gameMapInfo.name)
	writeXML(xmlDom, fileName)
		
	
def writeXML(xmlDom,fileName):
	try:
		edieFileNmae = objectXMLPath + os.sep + path.basename(fileName)
		shutil.copy(fileName, edieFileNmae)
		f = file(edieFileNmae,'w')
		writer = codecs.lookup('utf-8')[3](f)
		xmlDom.writexml(writer, "\t", "\t", os.linesep, "utf-8")
		f.close()
		print edieFileNmae + ' '*4+ 'saved!'
	except Exception,e:
		print e


		
def replaceTransPoint(regTxt, repTex, data):
	regex = re.compile(regTxt)
	subRes = regex.subn(repTex, data)
	print '[%s],[%s],[%s]' % (regTxt, repTex, subRes[1])
	return subRes[0]



findResourceXML(praseGameMapInfo(praseMapInfo()))