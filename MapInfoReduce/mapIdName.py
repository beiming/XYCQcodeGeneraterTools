#coding=utf-8

import os,zlib
from xml.dom import minidom


def getXMLFile():
	extensionName = '.x'
	result = [(os.path.splitext(x)[0],praseXMLFile(unpackFile(x))) for x in os.listdir(os.getcwd()) if os.path.splitext(x)[1].lower() == extensionName]
	#for tupleText in result:
	#	print ('%s---%s' % tupleText)

def unpackFile(fileName):
	try:
		xfile = open(fileName,'rb')
		data = xfile.read()
		xfile.close()
		data = zlib.decompress(data)
	except Exception,e:
		print e
	return data

def praseXMLFile(data):
	xmlDom = minidom.parseString(data)
	mapXml = xmlDom.getElementsByTagName('Map')[0]
	#取得当前xml跟节点(The one and only root element of the document)，然后取其第一个子节点，是个TEXT_NODE，然后取其下一个节点(同一个父节点)
	#mapId = xmlDom.documentElement.firstChild.nextSibling.attributes['Code'] .value
	mapId = xmlDom.getElementsByTagName('Scene')[0].getAttribute('Code')
	mapName = mapXml.getAttribute('Name')
	print mapId, '-'*3 ,mapName.encode('gbk')
	return mapName.encode('gbk')



if __name__ == '__main__':
	getXMLFile()