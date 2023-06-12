import sys


from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc

from v00.View import ViewClass


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
    
        self.setWindowTitle('NRTL parameters adjustment')
        self.setWindowIcon(qtg.QIcon(".\images\logo.png"))

        self.view = ViewClass()
        self.setCentralWidget(self.view)
        self.showMaximized()
        
     






if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())

