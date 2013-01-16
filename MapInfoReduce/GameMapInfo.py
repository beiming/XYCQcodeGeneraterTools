#coding=utf-8
from MapInfo import MapInfo

class GameMapInfo(object):
	'''gameMapInfo.xml's info to save here.
	contents map's specific infomation.
	
	id: map id in game.
	imageTemplate: map's image template and xml template index.
	delpoint: map's delete transport point.
	name: map's in game's name.
	
	pointSplit: delpoint, outpoint split with this.
	transSplit: transport points split with this.
	transFlag: transport points flag.
	'''
	pointSplit=' '
	transSplit='|'
	transFlag='4'
	
	def __init__(self, id, imageTemplate, delpoint, name,mapInfo, transToId):
		super(GameMapInfo, self).__init__(self)
		self.id = id
		self.imageTemplate = imageTemplate
		self.delpoint = delpoint
		self.transToId = transToId
		self.name = name
		self.setMapInfo(mapInfo)
				
	def setMapInfo(self, mapInfo):
		self.mapInfo = mapInfo
		self.outpoint = mapInfo.point2  if self.delpoint == mapInfo.point1 else mapInfo.point1
		
	def setTransTo(self,mapInfo):
		self.transToMap = mapInfo
		if self.transToMap:
			#_4_1021002|55|44,
			transPoint = self.transSplit.join(self.transToMap.delpoint.split(self.pointSplit))
			self.transToInfo = self.getTransToText()
		else:
			self.transToInfo = ''
			
	def getTransToText(self):
		transPoint = self.transSplit.join(self.transToMap.delpoint.split(self.pointSplit))
		#return self.mapInfo.pointArrSplit +  self.transFlag + self.mapInfo.pointArrSplit + self.transToMap.id + self.transSplit + transPoint + self.mapInfo.pointArrSplitout
		return self.transToMap.id + self.transSplit + transPoint + self.mapInfo.pointArrSplitout
	
	def getDeleteText(self):
		return ''
		
	def getDeletePoints(self):
		if self.delpoint == self.mapInfo.point1:
			lis = self.mapInfo.point1Arr.split(self.mapInfo.pointArrSplitout)
		else:
			lis = self.mapInfo.point2Arr.split(self.mapInfo.pointArrSplitout)
		return [x.strip() + self.mapInfo.pointArrSplitout for x in lis if x]
		return lis
	
	def getReplacePoints(self):
		if self.outpoint == self.mapInfo.point1:
			lis = self.mapInfo.point1Arr.split(self.mapInfo.pointArrSplitout)
		else:
			lis = self.mapInfo.point2Arr.split(self.mapInfo.pointArrSplitout)
		return [x.strip() + self.mapInfo.pointArrSplitout for x in lis if x]
		return lis
		
	def show(self):
		print self.name.encode('gbk')
		print self.transToMap.name.encode('gbk') if self.transToInfo else 'None'
		print self.transToInfo
		self.mapInfo.show()
		print self.__dict__
		print ''
		