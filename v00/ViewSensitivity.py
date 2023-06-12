from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class SensitivityDialog(qtw.QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.layoutsUI()
        self.widgets()

    def layoutsUI(self):
        self.main_layout = qtw.QHBoxLayout()
        self.setLayout(self.main_layout) #Main layout

        self.analysis_layout = qtw.QGridLayout()
        self.optimization_layout = qtw.QGridLayout()

    
    def widgets(self):
        #Analysis parameters
        analysis_groupbox = qtw.QGroupBox("Analysis")
        self.analysis_layout.addWidget(analysis_groupbox)
        

        self.repeat_checkbox = qtw.QCheckBox(
            "Repeat",
            self,
            checkeable = True,
            checked = False
        )


        analysis_groupbox.


        optimization_groupbox = qtw.QGroupBox("Optimization")

