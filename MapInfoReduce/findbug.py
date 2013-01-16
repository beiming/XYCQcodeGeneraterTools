from Tkinter import *
from xml.dom import minidom
import math

def getx(x, y, a):
	return int(x * math.cos(a) + y * math.sin(a))
	
def gety(x, y, a):
	return int(-x * math.sin(a) + y * math.cos(a))
	

def getAllTxt(index):
	xmlDom = minidom.parse(str(index)+'.xml')
	mapXml = xmlDom.getElementsByTagName('Map')[0]
	return mapXml.getAttribute('Terrain')
	
	
allTxt = getAllTxt(6)
allNode = allTxt.split(',')
nodes = []

for x in range(128):
    xlis = []
    nodes.append(xlis)
    for y in range(128):
        xlis.append('1')#can walk
        
for node in allNode:
	if node:
		info = node.split('_')
		if info != u'':
			if info[2] != '0':
				nodes[int(info[0])][int(info[1])] = '1'#can walk
			else:
				nodes[int(info[0])][int(info[1])] = '0'#no way
		
size = 5
angle = -45
offsetX = 0
offsetY = 0

radians = angle * math.pi / 180
root = Tk()
cv = Canvas(root, bg = 'white', width = 1280, height = 1280)
for x in range(128):
	for y in range(128):
		if nodes[x][y] == '0':#no way
			x1 = x * size
			y1 = y * size
			
			x2 = x1
			y2 = y1 - size
			
			x3 = x1 - size
			y3 = y1 - size
			
			x4 = x1 - size
			y4 = y1
			
			#x1 = getx(x1,y1,radians) + offsetX
			#y1 = gety(x1,y1,radians) + offsetY
			
			#x2 = getx(x2,y2,radians) + offsetX
			#y2 = gety(x2,y2,radians) + offsetY
			
			#x3 = getx(x3,y3,radians) + offsetX
			#y3 = gety(x3,y3,radians) + offsetY
			
			#x4 = getx(x4,y4,radians) + offsetX
			#y4 = gety(x4,y4,radians) + offsetY
			
			#cv.create_rectangle(x1, y1, x2, y2,  outline = 'red',fill = 'red')
			cv.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, outline = 'red',fill = 'red')
		#else:#can walk
		#	cv.create_rectangle(x1, y1, x2, y2,outline = 'black',fill = 'black')
cv.pack()
root.mainloop()



	

