#!/usr/bin/env python

#This code makes it easy to take the running average of an arbitrary number
#of points. The number of points must be specified at the calling of the 
#class. This utilizes the "collections" library due to the excellent 
#efficiency of this class. It has a O(1).

import collections

class LPfilter:
	num = 10
	data = 0
	out = 0
	def __init__(self, numPoints, firstData):
		self.num = numPoints
		self.data = [firstData] * numPoints
		self.data = collections.deque(self.data, numPoints)
	def filter(self, newData):
		self.data.append(newData)
		self.out = sum(self.data)/self.num
		return self.out
