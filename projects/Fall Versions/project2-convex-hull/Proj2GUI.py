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


# Import the code with the actual implementation
from convex_hull import *


# This class controls the visual stuff in the GUI.  An instance of it is passed to the solver
# when it is called so that wrapper functions in the file "convex_hull.py" can update the GUI
#
class PointLineView( QWidget ):
	def __init__( self, status_bar ):
		super(QWidget,self).__init__()
		self.setMinimumSize(600,400)

		self.pointList  = {}
		self.lineList   = {}
		self.status_bar = status_bar

	def displayStatusText(self, text):
		self.status_bar.showMessage(text)
		self.update()
		app.processEvents

	def clearPoints(self):
		self.pointList = {}

	def clearLines(self, lines=None):
		if(not lines):
			self.lineList = {}
		else:
			for color in self.lineList:
				for line in lines:
					try:
						self.lineList[color].remove(line)
					except:
						pass
		self.update()
		app.processEvents()

	def addPoints( self, point_list, color ):
		if color in self.pointList:
			self.pointList[color].extend( point_list )
		else:
			self.pointList[color] = point_list

	def addLines( self, line_list, color ):
		if color in self.lineList:
			self.lineList[color].extend( line_list )
		else:
			self.lineList[color] = line_list
		self.update()
		app.processEvents()

	def paintEvent(self, event):
		painter = QPainter(self)

		w = self.width() / 2.0
		h = self.height() / 2.0
		w2h_desired_ratio = 1.5
		if w / h < w2h_desired_ratio:
			h = w / w2h_desired_ratio
		else:
			w = h * w2h_desired_ratio

		tform = QTransform()
		tform.translate(self.width()/2.0,self.height()/2.0)
		tform.scale(1.0,-1.0)
		painter.setTransform(tform)

		for color in self.lineList:
			c = QColor(color[0],color[1],color[2])
			painter.setPen( c )
			for line in self.lineList[color]:
				ln = QLineF( w*line.x1(), h*line.y1(), w*line.x2(), h*line.y2() )
				painter.drawLine( ln )

		for color in self.pointList:
			c = QColor(color[0],color[1],color[2])
			painter.setPen( c )
			for point in self.pointList[color]:
				pt = QPointF(w*point.x(), h*point.y())
				painter.drawEllipse( pt, 1.0, 1.0)


# Main GUI class
#
class Proj2GUI( QMainWindow ):
	def __init__( self ):
		super(Proj2GUI,self).__init__()

		# This is where the points for a problem instance are kept
		self.points = None

		# Getting an instance of your solver
		self.solver = ConvexHullSolver()

		# start the GUI
		self.initUI()

	# Generator for new sets of points that represent hull finding problem instances
	def newPoints(self):

		if self.randBySeed.isChecked():
			seed = int(self.randSeed.text())
			random.seed( seed )
		else: # do by time
			random.seed( time.time() )

		ptlist = []
		unique_xvals = {}
		max_r  = 0.98
		WIDTH  = 1.0
		HEIGHT = 1.0
		npoints = int(self.npoints.text())
		if self.distribOval.isChecked():
			while len(ptlist) < npoints:
				x = random.uniform(-1.0,1.0)
				y = random.uniform(-1.0,1.0)
				if x**2+y**2 <= max_r**2:
					xval = WIDTH*x
					yval = HEIGHT*y
					if not xval in unique_xvals:
						ptlist.append( QPointF(xval,yval) )
						unique_xvals[xval] = 1
		elif self.distribSphere.isChecked():
			while len(ptlist) < npoints:
				x = random.uniform(-1.0,1.0)
				y = random.uniform(-1.0,1.0)
				z = random.uniform(-1.0,1.0)
				if x**2 + y**2 + z**2 <= max_r**2:
					xval = WIDTH*x
					yval = HEIGHT*y
					if not xval in unique_xvals:
						ptlist.append( QPointF(xval,yval) )
						unique_xvals[xval] = 1
		elif self.distribGaussian.isChecked():
			while len(ptlist) < npoints:
				x = random.gauss(0.0,0.25)
				y = random.gauss(0.0,0.25)
				if x**2+y**2 <= max_r**2:
					xval = WIDTH*x
					yval = HEIGHT*y
					if not xval in unique_xvals:
						ptlist.append( QPointF(xval,yval) )
						unique_xvals[xval] = 1
		return ptlist

# Methods that handle GUI events
	def clearClicked(self):
		self.view.clearLines()
		self.view.displayStatusText('')
		self.solveButton.setEnabled(True)
		self.view.update()
		app.processEvents()

	def generateClicked(self):
		if self.points:
			self.view.clearPoints()
			self.view.clearLines()
		self.points = self.newPoints()
		self.view.addPoints( self.points, (0,0,0) )
		self.solveButton.setEnabled(True)
		self.view.update()
		app.processEvents()

# This the method that hooks into your solver.  It passes the
# problem instance/solution request (a set of points) to the solver, along with
# the recursion flag to indicate whether to animate the solution
# and a view object so the GUI can be updated
	def solveClicked(self):
		self.generateButton.setEnabled(False)
		self.clearButton.setEnabled(False)
		self.solveButton.setEnabled(False)
		self.view.update()
		app.processEvents()
		self.solver.compute_hull(self.points,self.showRecursion.isChecked(),self.view)
		self.generateButton.setEnabled(True)
		self.clearButton.setEnabled(True)
		self.view.update()
		app.processEvents()

	def _randbytime(self):
		self.randSeed.setEnabled(False)

	def _randbyseed(self):
		self.randSeed.setEnabled(True)

	# Setting up the GUI
	def initUI( self ):
		self.setWindowTitle('Convex Hull')
		self.setWindowIcon( QIcon('icon312.png') )

		self.statusBar = QStatusBar()
		self.setStatusBar( self.statusBar )

		vbox = QVBoxLayout()
		boxwidget = QWidget()
		boxwidget.setLayout(vbox)
		self.setCentralWidget( boxwidget )

		self.view           = PointLineView( self.statusBar )
		self.npoints        = QLineEdit('10')
		self.generateButton = QPushButton('Generate')
		self.solveButton    = QPushButton('Solve')
		self.clearButton    = QPushButton('Clear To Points')
		self.distribOval    = QRadioButton('Uniform')
		self.distribSphere  = QRadioButton('Spherical')
		self.distribGaussian= QRadioButton('Gaussian')

		self.randByTime     = QRadioButton('Random')
		self.randBySeed     = QRadioButton('Seed')
		self.randSeed       = QLineEdit('0')

		self.showRecursion	= QCheckBox('Show Recursion')

		h = QHBoxLayout()
		h.addWidget( self.view )
		vbox.addLayout(h)

		h = QHBoxLayout()
		h.addWidget( QLabel( 'Number of points to generate: ' ) )
		h.addWidget( self.npoints )
		h.addWidget( self.generateButton )
		h.addWidget( self.solveButton )
		h.addWidget( self.clearButton )
		h.addStretch(1)
		vbox.addLayout(h)

		h = QHBoxLayout()
		grp = QButtonGroup(self)
		grp.addButton(self.distribOval)
		grp.addButton(self.distribSphere)
		grp.addButton(self.distribGaussian)
		h.addWidget( QLabel( 'Distribution of generated points: ' ) )
		h.addWidget( self.distribOval )
		h.addWidget( self.distribSphere )
		h.addWidget( self.distribGaussian )
		h.addStretch(1)
		vbox.addLayout(h)

		h = QHBoxLayout()
		h.addWidget( QLabel( 'Point Locations: ' ) )
		grp = QButtonGroup(self)
		grp.addButton(self.randByTime)
		grp.addButton(self.randBySeed)
		h.addWidget( self.randByTime )
		h.addWidget( self.randBySeed )
		h.addWidget( self.randSeed )
		h.addStretch(1)
		h.addWidget(self.showRecursion)
		vbox.addLayout(h)

		self.generateButton.clicked.connect(self.generateClicked)
		self.solveButton.clicked.connect(self.solveClicked)
		self.clearButton.clicked.connect(self.clearClicked)

		self.randByTime.clicked.connect(self._randbytime)
		self.randBySeed.clicked.connect(self._randbyseed)


		self.randByTime.setChecked(True)
		self.distribOval.setChecked(True)
		self.generateClicked()

		self.showRecursion.setChecked(False)

		self.show()




if __name__ == '__main__':
	# This line allows CNTL-C in the terminal to kill the program
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QApplication(sys.argv)
	w = Proj2GUI()
	sys.exit(app.exec())
