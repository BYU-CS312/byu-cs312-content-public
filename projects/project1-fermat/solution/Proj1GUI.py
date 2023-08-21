#!/usr/bin/python3

import signal
import sys

# This imports the needed PYQT modules for the GUI
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit


# Import in the code that implements the actual primality testing
import fermat



class Proj1GUI( QWidget ):

    def __init__( self ):
        super().__init__()
        self.initUI()

    def initUI( self ):
        self.setWindowTitle('Primality Tester')
        self.setWindowIcon( QIcon('icon312.png') )

        # Now setup for project 1
        vbox = QVBoxLayout()
        self.setLayout( vbox )

        self.input_n = QLineEdit('312')
        self.input_k = QLineEdit('10')
        self.test    = QPushButton('Test Primality')
        self.outputF  = QLabel('<i>N is the number to test, K is how many random trials</i>')
        self.outputF.setMinimumSize(500,0)
        self.outputMR = QLabel('')
        self.outputMR.setMinimumSize(500,0)

        # N
        h = QHBoxLayout()
        h.addWidget( QLabel( 'N: ' ) )
        h.addWidget( self.input_n )
        vbox.addLayout(h)
        
        # K
        h = QHBoxLayout()
        h.addWidget( QLabel( 'K: ' ) )
        h.addWidget( self.input_k )
        vbox.addLayout(h)

        # Test
        h = QHBoxLayout()
        h.addStretch(1)
        h.addWidget( self.test )
        vbox.addLayout(h)

        # Output
        h = QHBoxLayout()
        h.addWidget( self.outputF )
        vbox.addLayout(h)
        h = QHBoxLayout()
        h.addWidget( self.outputMR )
        vbox.addLayout(h)

        # When the Test button is clicked, call testClicked()
        self.test.clicked.connect(self.testClicked)
        # Do the same if enter is pressed in either input field
        self.input_n.returnPressed.connect(self.testClicked)
        self.input_k.returnPressed.connect(self.testClicked)

        self.show()

#
# This is the method connected to the Test Button.  It calls the actual primality test code 
# (which you will implement) from the "fermat.py" file.
#
    def testClicked( self ):
        try:
            # Make sure inputs are valid integers
            n = int( self.input_n.text() )
            k = int( self.input_k.text() )

            # This is the call to the pass-through function that gets your results, from 
            # both the Fermat and Miller-Rabin tests you will implement
            ret_fermat,ret_mr = fermat.prime_test(n,k)
            
            # Output results from Fermat and compute the appropriate error bound, if necessary
            if ret_fermat == 'prime':
                prob = fermat.fprobability(k)
                self.outputF.setText( '<i>Fermat Result:</i> {:d} <b>is prime</b> with probability {:5.15f}'.format(n,prob) )
            else: # Should be 'composite'
                self.outputF.setText('<i>Fermat Result:</i> {:d} is <b>not prime</b>'.format(n))

            # Output results from Miller-Rabin and compute the appropriate error bound, if necessary
            if ret_mr == 'prime':
                prob = fermat.mprobability(k)
                self.outputMR.setText( '<i>MR Result:</i> {:d} <b>is prime</b> with probability {:5.15f}'.format(n,prob) )
            else: # Should be 'composite'
                self.outputMR.setText('<i>MR Result:</i> {:d} is <b>not prime</b>'.format(n))
                
        # If inputs not valid, display an error
        except Exception as e:
            self.outputF.setText('<i>ERROR:</i> ' + str(e) )




if __name__ == '__main__':
    # This line allows CNTL-C in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = QApplication(sys.argv)
    w = Proj1GUI()
    sys.exit(app.exec())
