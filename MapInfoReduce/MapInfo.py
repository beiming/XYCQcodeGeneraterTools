#coding=utf-8

class MapInfo(object):
	'''mapInfo.xml's info to save here.
	contents map's base infomation.
	
	id: map's template id.
	point1: upper left stand point.
	point2: lower right stand point.
	point1Arr: upper left transport points.
	point2Arr: upper left transport points.
	
	pointSplit: point1, point2 split with this.
	pointArrSplit: point1Arr, point2Arr split with this.
	transFlag: transport points flag.
	'''
	pointSplit =' '
	pointArrSplit ='_'
	transFlag ='4'
	pointArrSplitout = ','
	
	def __init__(self, id, point1, point2, point1Arr, point2Arr):
		super(MapInfo, self).__init__(self)
		self.id = id
		self.point1 = point1
		self.point2 = point2
		
		self.point1Arr = point1Arr
		self.point2Arr = point2Arr
		
	def show(self):
		print self.__dict__
		