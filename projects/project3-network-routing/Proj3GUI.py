#!/usr/bin/env python3

import math
import random
import signal
import sys
import time


from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
	from PyQt5.QtWidgets import *
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtGui import *
	from PyQt4.QtCore import *
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtWidgets import *
	from PyQt6.QtGui import *
	from PyQt6.QtCore import *
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


#TODO: Error checking on txt boxes
#TODO: Color strings


# Import in the code with the actual implementation
from CS312Graph import *
from NetworkRoutingSolver import *
#from NetworkRoutingSolver_faster import *
#from NetworkRoutingSolver_complete import *

BLACK = (0,0,0)

class PointLineView( QWidget ):

#signal for sending mouse clicks to the GUI
	pointclicked = pyqtSignal(str,QPointF)

	def __init__( self, status_bar, data_range ):
		super(QWidget,self).__init__()
		self.setMinimumSize(600,400)
		self.clicknode = 'start'
		self.pointList	= {}
		self.edgeList	= {}
		self.labelList	 = {}
		self.status_bar = status_bar
		self.data_range = data_range
		self.start_pt = None
		self.end_pt = None

	def displayStatusText(self, text):
		self.status_bar.showMessage(text)

	def clearPoints(self):
		self.pointList = {}

	def clearEdges(self):
		self.edgeList = {}
		self.labelList = {}

	def addPoints( self, point_list, color ):
		if color in self.pointList:
			self.pointList[color].extend( point_list )
		else:
			self.pointList[color] = point_list

	def setStartLoc( self, point ):
		self.start_pt = point
		self.repaint()

	def setEndLoc( self, point ):
		self.end_pt = point
		self.repaint()

	def addEdge( self, startPt, endPt, label, edgeColor, labelColor=None ):
		if not labelColor:
			labelColor = edgeColor
		assert( type(startPt) == QPointF )
		assert( type(endPt)	  == QPointF )
		assert( type(label)	  == str )
		edge = QLineF(startPt, endPt)
		if edgeColor in self.edgeList.keys():
			self.edgeList[edgeColor].append( edge )
		else:
			self.edgeList[edgeColor] = [edge]
		midp = QPointF( (edge.x1()+edge.x2())/2.0,
						(edge.y1()+edge.y2())/2.0 )
		if edgeColor in self.labelList.keys():
			self.labelList[edgeColor].append( (midp,label) )
		else:
			self.labelList[edgeColor] = [(midp,label)]

# Reimplemented to allow setting source/target nodes with mouse click
	def mousePressEvent(self,e):
		scale = self.getScale()
		self.pointclicked.emit(self.clicknode,QPointF((e.position().x()-self.width())/scale+2,(self.height()-e.position().y())/scale-1))
		if self.clicknode == 'start':
			self.clicknode = 'end'
		else:
			self.clicknode = 'start'

	def getScale(self):
		xr = self.data_range['x']
		yr = self.data_range['y']
		w = self.width()
		h = self.height()
		w2h_desired_ratio = (xr[1]-xr[0])/(yr[1]-yr[0])
		if w / h < w2h_desired_ratio:
			 scale = w / (xr[1]-xr[0])
		else:
			 scale = h / (yr[1]-yr[0])
		return scale

	def paintEvent(self, event):
		painter = QPainter(self)
		# painter.setRenderHint(QPainter.Antialiasing,True)
		scale = self.getScale()
		tform = QTransform()
		tform.translate(self.width()/2.0,self.height()/2.0)
		tform.scale(1.0,-1.0)
		painter.setTransform(tform)
		for color in self.edgeList:
			c = QColor(color[0],color[1],color[2])
			painter.setPen( c )
			for edge in self.edgeList[color]:
				ln = QLineF( scale*edge.x1(), scale*edge.y1(), scale*edge.x2(), scale*edge.y2() )
				painter.drawLine( ln )
		R = 1.0E3
		RECT = QRectF(-R,-R,2.0*R,2.0*R)
		align = QTextOption(Qt.AlignmentFlag.AlignCenter)
		for color in self.labelList:
			c = QColor(color[0],color[1],color[2])
			painter.setPen( c )
			for label in self.labelList[color]:
				temp_tform = QTransform()
				temp_tform.translate(self.width()/2.0,self.height()/2.0)
				temp_tform.scale(1.0,-1.0)
				pt = label[0]
				temp_tform.translate(scale*pt.x(),scale*pt.y())
				temp_tform.scale(1.0,-1.0)
				painter.setTransform(temp_tform)
				painter.drawText( RECT, label[1], align )
		painter.setTransform(tform)
		for color in self.pointList:
			c = QColor(color[0],color[1],color[2])
			painter.setPen( c )
			for point in self.pointList[color]:
				pt = QPointF(scale*point.x(), scale*point.y())
				painter.drawEllipse( pt, 1.0, 1.0)
		if self.start_pt:
			painter.setPen( QPen(QColor(0,255,0), 2.0) )
			pt = QPointF( scale*self.start_pt.x() -0.0, \
						  scale*self.start_pt.y() -0.0 )
			painter.drawEllipse( pt, 4.0, 4.0)
		if self.end_pt:
			painter.setPen( QPen(QColor(255,0,0), 2.0) )
			pt = QPointF( scale*self.end_pt.x() -0.0, \
						  scale*self.end_pt.y() -0.0 )
			painter.drawEllipse( pt, 4.0, 4.0)


class Proj3GUI( QMainWindow ):

	def __init__( self ):
		super(Proj3GUI,self).__init__()
		self.RED_STYLE	 = "background-color: rgb(255, 220, 220)"
		self.PLAIN_STYLE = "background-color: rgb(255, 255, 255)"
		self.graph = None
		self.initUI()
		self.solver = NetworkRoutingSolver()
		self.genParams = (None, None)

	def newPoints(self):
		# TODO - ERROR CHECKING!!!!
		seed = int(self.randSeed.text())
		random.seed( seed )
		ptlist = []
		RANGE = self.data_range
		xr = self.data_range['x']
		yr = self.data_range['y']
		npoints = int(self.size.text())
		while len(ptlist) < npoints:
			x = random.uniform(0.0,1.0)
			y = random.uniform(0.0,1.0)
			if True:
				xval = xr[0] + (xr[1]-xr[0])*x
				yval = yr[0] + (yr[1]-yr[0])*y
				ptlist.append( QPointF(xval,yval) )
		return ptlist

	def generateNetwork(self):
		nodes = self.newPoints()
		OUT_DEGREE = 3
		size = len(nodes)
		edgeList = {}
		for u in range(size):
			edgeList[u] = []
			pt_u = nodes[u]
			chosen = []
			for i in range(OUT_DEGREE):
				v = random.randint(0,size-1)
				while v in chosen or v == u:
					v = random.randint(0,size-1)
				chosen.append(v)
				pt_v = nodes[v]
				uv_len = math.sqrt( (pt_v.x()-pt_u.x())**2 + \
									(pt_v.y()-pt_u.y())**2 )
				edgeList[u].append( (v,100.0*uv_len) )
			edgeList[u] = sorted(edgeList[u], key=lambda n:n[0])
		self.graph = CS312Graph(nodes, edgeList)
		self.genParams = (self.randSeed.text(), self.size.text())
		self.view.clearEdges()
		self.view.clearPoints()
		self.sourceNode.setText('')
		self.targetNode.setText('')

	def generateClicked(self):
		if int(self.size.text()) < 4:
			self.statusBar.showMessage('Input Error: Network size must be greater than 3')
		else:
			self.statusBar.showMessage('')
			self.generateNetwork()
			self.view.addPoints( [x.loc for x in self.graph.getNodes()], (0,0,0) )
			self.view.repaint()
#		if self.graph:
#				self.generateNetwork()
#				self.view.addPoints( [x.loc for x in self.graph.getNodes()], (0,0,0) )
#				self.view.repaint()
#		else:
#			self.generateNetwork()
#			self.view.addPoints( [x.loc for x in self.graph.getNodes()], (0,0,0) )
#			self.view.repaint()
			self.graphReady = True
			self.checkGenInputs()
			self.checkPathInputs()

	def display_paths( self, heap_path, heap_time, array_path, array_time ):
		self.view.clearEdges()
		if heap_path:
			cost = heap_path['cost']
			for start,end,lbl in heap_path['path']:
				self.view.addEdge(startPt=start, endPt=end, label=lbl, edgeColor=(128,128,255))
			self.heapTime.setText('{:.6f}s'.format(heap_time))
			if not array_path:
				self.arrayTime.setText('')
				self.speedup.setText('')
		if array_path:
			cost = array_path['cost']
			for start,end,lbl in array_path['path']:
				self.view.addEdge(startPt=start, endPt=end, label=lbl, edgeColor=(128,128,255))
			self.arrayTime.setText('{:.6f}s'.format(array_time))
			if not heap_path:
				self.heapTime.setText('')
				self.speedup.setText('')
		if heap_path and array_path:
			if heap_time > 0:
				ratio = 1.0*array_time/heap_time
			else:
				ratio = math.inf
			self.speedup.setText('Heap is {:.3f}x Faster'.format(ratio))
		self.view.repaint()

	def computeClicked(self):
		self.solver.initializeNetwork(self.graph)
		doArray = False
		doHeap	= False
		if self.useUnsorted.isChecked():
			doArray = True
			heap_path = None
			heap_time = None
		elif self.useHeap.isChecked():
			doHeap = True
			array_path = None
			array_time = None
		else:
			doArray = True
			doHeap = True
		if doArray:
			array_time = self.solver.computeShortestPaths( int(self.sourceNode.text())-1, use_heap=False )
			array_path = self.solver.getShortestPath( int(self.targetNode.text())-1 )
			dist = array_path['cost']
		if doHeap:
			heap_time = self.solver.computeShortestPaths( int(self.sourceNode.text())-1, use_heap=True )
			heap_path = self.solver.getShortestPath( int(self.targetNode.text())-1 )
			dist = heap_path['cost']
		self.display_paths( heap_path, heap_time, array_path, array_time )
		self.checkPathInputs()
		if dist == float('inf'):
			self.totalCost.setText( 'UNREACHABLE' )
		else:
			self.totalCost.setText( '{:.3f}'.format(dist) )
		self.view.clicknode = 'start'
		self.repaint()

	def checkGenInputs(self):
		seed  = self.randSeed.text()
		size = self.size.text()
		if self.graph:
			if self.genParams[0] == seed and self.genParams[1] == size:
				self.generateButton.setEnabled(False)
			elif (seed == '') or (size == ''):
				self.generateButton.setEnabled(False)
			else:
				self.generateButton.setEnabled(True)

	def checkInputValue(self, widget, validrange):
		assert( type(widget) == QLineEdit )
		retval = None
		valid  = False
		try:
			sval = widget.text()
			if sval == '':
				valid = True
			else:
				ival = int(sval)
				if validrange:
					if ival >= validrange[0] and ival <= validrange[1]:
						retval = ival
						valid = True
		except:
			pass
		if not valid:
			widget.setStyleSheet( self.RED_STYLE )
		else:
			widget.setStyleSheet( '' )
		return '' if retval==None else retval

	def checkPathInputs(self):
		if not self.graphReady:
			self.computeCost.setEnabled(False)
			print( self.sourceNode.styleSheet() )
			self.sourceNode.setStyleSheet( '' )
			self.sourceNode.setEnabled(False)
			self.targetNode.setStyleSheet( '' )
			self.targetNode.setEnabled(False)
		else: # HAS GRAPH!!!
			self.sourceNode.setEnabled(True)
			self.targetNode.setEnabled(True)
			self.computeCost.setEnabled(False)
			valid_inds = [1,int(self.genParams[1])]
			points = self.graph.getNodes()
			src	 = self.checkInputValue( self.sourceNode, valid_inds )
			if not src == '':
				self.view.setStartLoc( points[src-1].loc )
			else:
				self.view.setStartLoc( None )
			dest = self.checkInputValue( self.targetNode, valid_inds )
			if not dest == '':
				if src == dest:
					self.targetNode.setStyleSheet( self.RED_STYLE )
					self.view.setEndLoc( None )
				else:
					self.view.setEndLoc( points[dest-1].loc )
			else:
				self.view.setEndLoc( None )
			if ((not src == self.lastPath[0]) or (not dest == self.lastPath[1])) and \
				(not src == '') and (not dest == '') and (not src == dest):
				self.computeCost.setEnabled(True)
				self.view.repaint()

# Listens for signal of mouse click and finds the nearest point and sets it alternately as
# source or target node
	def setByClick(self,clickednode,point):
		if not self.graphReady:
			pass
		else:
			id = -1
			dist = math.inf
			for node in self.graph.nodes:
				if math.sqrt(pow((abs(node.loc.x()-point.x())),2) + pow((abs(node.loc.y()-point.y())),2)) < dist:
					dist = math.sqrt(pow((abs(node.loc.x()-point.x())),2) + pow((abs(node.loc.y()-point.y())),2))
					id = node.node_id+1
			if id != -1:
				self.view.clearEdges()
				if clickednode == 'start':
					self.sourceNode.setText(str(id))
				elif clickednode == 'end':
					self.targetNode.setText(str(id))
				self.checkPathInputs()

	def initUI( self ):
		self.setWindowTitle('Network Routing')
		self.setWindowIcon( QIcon('icon312.png') )
		self.statusBar = QStatusBar()
		self.setStatusBar( self.statusBar )
		vbox = QVBoxLayout()
		boxwidget = QWidget()
		boxwidget.setLayout(vbox)
		self.setCentralWidget( boxwidget )
		SCALE = 1.0
		self.data_range		= { 'x':[-2*SCALE,2*SCALE], \
								'y':[-SCALE,SCALE] }
		self.view			= PointLineView( self.statusBar, \
											 self.data_range )
		self.generateButton = QPushButton('Generate')
		self.computeCost	= QPushButton('Compute Cost')
		self.useUnsorted	= QRadioButton('Unsorted Array')
		self.useHeap		= QRadioButton('Min Heap')
		self.useBoth		= QRadioButton('Use Both')
		self.arrayTime		= QLineEdit('')
		self.arrayTime.setFixedWidth(120)
		self.arrayTime.setEnabled(False)
		self.heapTime		= QLineEdit('')
		self.heapTime.setFixedWidth(120)
		self.heapTime.setEnabled(False)
		self.speedup		= QLineEdit('')
		self.speedup.setFixedWidth(200)
		self.speedup.setEnabled(False)
		self.randSeed		= QLineEdit('0')
		self.size			= QLineEdit('7')
		self.sourceNode		= QLineEdit('')
		self.targetNode		= QLineEdit('')
		self.totalCost		= QLineEdit('0.0')
		h = QHBoxLayout()
		h.addWidget( self.view )
		vbox.addLayout(h)
		h = QHBoxLayout()
		h.addWidget( QLabel('Random Seed: ') )
		h.addWidget( self.randSeed )
		h.addWidget( QLabel('Size: ') )
		h.addWidget( self.size )
		h.addWidget( self.generateButton )
		h.addStretch(1)
		vbox.addLayout(h)
		h = QHBoxLayout()
		h.addWidget( QLabel( 'Source Node: ' ) )
		h.addWidget( self.sourceNode )
		h.addWidget( QLabel( 'Target Node: ' ) )
		h.addWidget( self.targetNode )
		h.addWidget( self.computeCost )
		h.addWidget( QLabel( 'Total Path Cost: ' ) )
		h.addWidget( self.totalCost )
		self.totalCost.setEnabled(False)
		h.addStretch(1)
		vbox.addLayout(h)
		h = QHBoxLayout()
		h.addWidget( self.useUnsorted )
		h.addWidget( self.arrayTime )
		h.addWidget( self.useHeap )
		h.addWidget( self.heapTime )
		h.addWidget( self.useBoth )
		h.addWidget( self.speedup )
		self.useHeap.setChecked(True)
		h.addStretch(1)
		vbox.addLayout(h)
		self.lastPath = (None,None)
		self.computeCost.setEnabled(False)
		self.sourceNode.textChanged.connect(self.checkPathInputs)
		self.targetNode.textChanged.connect(self.checkPathInputs)
		self.view.pointclicked.connect(self.setByClick)
		self.randSeed.textChanged.connect(self.checkGenInputs)
		self.size.textChanged.connect(self.checkGenInputs)
		self.generateButton.clicked.connect(self.generateClicked)
		self.computeCost.clicked.connect(self.computeClicked)
		self.graphReady = False
		self.checkPathInputs()
		self.show()


if __name__ == '__main__':
	# This line allows CNTL-C in the terminal to kill the program
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QApplication(sys.argv)
	w = Proj3GUI()
	sys.exit(app.exec())
