#!/usr/bin/env python3

import signal
import sys
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

import time
import math

# Import in the code with the actual implementation
from GeneSequencing import *


class Proj4GUI( QMainWindow ):

	def __init__( self ):
		super(Proj4GUI,self).__init__()

		self.RED_STYLE	 = "background-color: rgb(255, 220, 220)"
		self.PLAIN_STYLE = "background-color: rgb(255, 255, 255)"

		self.seqs = self.loadSequencesFromFile()
		self.processed_results = []

		self.initUI()
		self.solver = GeneSequencing()

	def processClicked(self):
		sequences = [ self.seqs[i][2] for i in sorted(self.seqs.keys()) ]

		self.statusBar.showMessage('Processing...')
		app.processEvents()
		start = time.time()

		for i in range(len(sequences)):
			jresults = []
			for j in range(len(sequences)):
				if(j < i):
					s = {}
				else:
					s = self.solver.align(sequences[i], sequences[j], banded=self.banded.isChecked(),
													align_length=int(self.alignLength.text()))
					self.table.item(i,j).setText('{}'.format(int(s['align_cost']) if s['align_cost'] \
																					 != math.inf else s['align_cost']))
					app.processEvents()
				jresults.append(s)
			self.processed_results.append(jresults)

		end = time.time()
		ns = end-start
		nm = math.floor(ns/60.)
		ns = ns - 60.*nm
		if nm > 0:
			self.statusBar.showMessage('Done.  Time taken: {} mins and {:3.3f} seconds.'.format(nm,ns))
		else:
			self.statusBar.showMessage('Done.  Time taken: {:3.3f} seconds.'.format(ns))
		self.processButton.setEnabled(False)
		self.clearButton.setEnabled(True)
		self.repaint()

	def clearClicked(self):
		self.processed_results = []
		self.resetTable()
		self.processButton.setEnabled(True)
		self.clearButton.setEnabled(False)

		self.seq1n_lbl.setText( 'Label {}: '.format('I') )
		self.seq1c_lbl.setText( 'Sequence {}: '.format('I') )
		self.seq2c_lbl.setText( 'Sequence {}: '.format('J') )
		self.seq2n_lbl.setText( 'Label {}: '.format('J') )

		self.seq1_name.setText( '{}'.format(' ') )
		self.seq2_name.setText( '{}'.format(' ') )
		self.seq1_chars.setText( '{}'.format(' ') )
		self.seq2_chars.setText( '{}'.format(' ') )
		self.statusBar.showMessage('')
		self.repaint()

	def resetTable(self):
		for i in range(self.table.rowCount()):
			for j in range(self.table.columnCount()):
				if j >= i:
					self.table.item(i,j).setText(' ')

	def cellClicked(self, i, j):
		print('Cell {},{} clicked!'.format(i,j))
		print('lbls: {} and {}'.format(self.seqs[i][1],self.seqs[j][1]))

		if self.processed_results and j >= i:
			print('in if')
			self.seq1n_lbl.setText( 'Label {}: '.format(i+1) )
			self.seq1c_lbl.setText( 'Sequence {}: '.format(i+1) )
			self.seq2c_lbl.setText( 'Sequence {}: '.format(j+1) )
			self.seq2n_lbl.setText( 'Label {}: '.format(j+1) )

			self.seq1_name.setText( '{}'.format(self.seqs[i][1]) )
			self.seq2_name.setText( '{}'.format(self.seqs[j][1]) )
			results = self.processed_results[i][j]
			self.seq1_chars.setText( '{}'.format(results['seqi_first100']) )
			self.seq2_chars.setText( '{}'.format(results['seqj_first100']) )

	def loadSequencesFromFile( self ):
		FILENAME = 'genomes.txt'
		raw = open(FILENAME,'r').readlines()
		sequences = {}

		i = 0
		cur_id	= ''
		cur_str = ''
		for liner in raw:
			line = liner.strip()
			if '#' in line:
				if len(cur_id) > 0:
					sequences[i] = (i,cur_id,cur_str)
					cur_id	= ''
					cur_str = ''
					i += 1
				parts = line.split('#')
				cur_id = parts[0]
				cur_str += parts[1]
			else:
				cur_str += line
		if len(cur_str) > 0 or len(cur_id) > 0:
			sequences[i] = (i,cur_id,cur_str)
		return sequences

	def getTableDims( self ):
		w = self.table.columnWidth(self.table.rowCount()-1) - 4
		for i in range(self.table.columnCount()):
			w += self.table.columnWidth(i)
		h = self.table.horizontalHeader().height() + 1
		for i in range(self.table.rowCount()):
			h += self.table.rowHeight(i)
		return (w,h)

	def initUI( self ):
		self.setWindowTitle('Gene Sequence Alignment')
		self.setWindowIcon( QIcon('icon312.png') )

		self.statusBar = QStatusBar()
		self.setStatusBar( self.statusBar )

		vbox = QVBoxLayout()
		boxwidget = QWidget()
		boxwidget.setLayout(vbox)
		self.setCentralWidget( boxwidget )

		self.table = QTableWidget(self)
		NSEQ = 10
		self.table.setRowCount(NSEQ)
		self.table.setColumnCount(NSEQ)

		headers = [ 'sequence{}'.format(a+1) for a in range(NSEQ) ]
		self.table.setHorizontalHeaderLabels(headers)
		self.table.setVerticalHeaderLabels(headers)

		for i in range(NSEQ):
			for j in range(NSEQ):
				qitem = QTableWidgetItem(" ")
				qitem.setFlags( Qt.ItemFlag.ItemIsSelectable |  Qt.ItemFlag.ItemIsEnabled )
				if j < i:
					qitem.setBackground(QColor(200,200,200))
					qitem.setFlags( Qt.ItemFlag.ItemIsSelectable )
				self.table.setItem(i,j,qitem)
		for i in range(NSEQ):
			self.table.resizeColumnToContents(i)
		for j in range(NSEQ):
			self.table.resizeRowToContents(i)

		w,h = self.getTableDims()
		self.table.setFixedWidth(w)
		self.table.setFixedHeight(h)

		self.processButton	= QPushButton('Process')
		self.clearButton	= QPushButton('Clear')

		self.banded		= QCheckBox('Banded')
		self.banded.setChecked(False)
		self.alignLength	  = QLineEdit('1000')
		font = QFont()
		font.setFamily("Courier New")
		self.seq1_name	   = QLineEdit('')
		self.seq1_name.setFixedWidth(650)
		self.seq1_name.setEnabled(False)
		self.seq1_chars		= QLineEdit('')
		self.seq1_chars.setFixedWidth(850)
		self.seq1_chars.setFont(font)
		self.seq1_chars.setEnabled(False)
		self.seq2_chars		= QLineEdit('')
		self.seq2_chars.setFixedWidth(850)
		self.seq2_chars.setFont(font)
		self.seq2_chars.setEnabled(False)
		self.seq2_name	   = QLineEdit('')
		self.seq2_name.setFixedWidth(650)
		self.seq2_name.setEnabled(False)

		h = QHBoxLayout()
		h.addStretch(1)
		h.addWidget( self.table )
		h.addStretch(1)
		vbox.addLayout(h)

		h = QHBoxLayout()
		vleft  = QVBoxLayout()
		vright = QVBoxLayout()
		self.seq1n_lbl = QLabel('Label I: ')
		vleft.addWidget( self.seq1n_lbl )
		vright.addWidget( self.seq1_name )

		self.seq1c_lbl = QLabel('Sequence I: ')
		vleft.addWidget( self.seq1c_lbl )
		vright.addWidget( self.seq1_chars )

		self.seq2c_lbl = QLabel('Sequence J: ')
		vleft.addWidget( self.seq2c_lbl )
		vright.addWidget( self.seq2_chars )

		self.seq2n_lbl = QLabel('Label J: ')
		vleft.addWidget( self.seq2n_lbl )
		vright.addWidget( self.seq2_name )

		h.addLayout(vleft)
		h.addLayout(vright)
		vbox.addLayout(h)

		h = QHBoxLayout()
		h.addStretch(1)
		h.addWidget( self.processButton )
		h.addWidget( self.clearButton )
		h.addStretch(1)
		vbox.addLayout(h)

		h = QHBoxLayout()
		h.addStretch(1)
		h.addWidget( self.banded )
		h.addWidget( QLabel('Align Length: ') )
		h.addWidget( self.alignLength )
		h.addStretch(1)
		vbox.addLayout(h)

		self.processButton.clicked.connect(self.processClicked)
		self.clearButton.clicked.connect(self.clearClicked)
		self.clearButton.setEnabled(False)
		self.table.cellClicked.connect(self.cellClicked)

		self.show()


if __name__ == '__main__':
	# This line allows CNTL-C in the terminal to kill the program
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QApplication(sys.argv)
	w = Proj4GUI()
	sys.exit(app.exec())
