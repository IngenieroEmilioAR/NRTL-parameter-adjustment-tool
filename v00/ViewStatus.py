from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

import datetime
import getpass





class Status(qtw.QWidget):

    def __init__(self, status = None):
        super().__init__()
        self.status = status
        self.user = getpass.getuser()
        
    def print_user(self):
        user = f"""
        User: {self.user}"""
        return user

    def last_action(self):
        actual_datetime = datetime.datetime.now()
        last_action = f"""Last action: {actual_datetime}
        """
        return last_action


    def initial_text(self):
        initial = f"""
        {self.print_user()}
        {self.last_action()}
=============================================================

Please, select a datafile with experimental data ...

"""
        return initial


    def after_data_selection(self, datafile):
        status_post_file_selection = f"""
=============================================================

{datafile} has been succesfully introduced.

To proceed, please complete the optimization zone.
To perform a sensitivity analysis or evaluate binary parameters using your experimental data, click on the designated buttons.

"""
        return status_post_file_selection


    def optimization_initialized(self):
        text = f"""
=============================================================
{self.last_action()}

Adjusting to the model ...        
        """
        return text

    def optimization_cannot_be_initialized(self):
        text = f"""

Calculations cannot be done, please verify your data structure.
        """
        return text

    def no_data(self):
        text = f"""

No data available. Please, select a datafile.
        """
        return text


    def optimization_completed(self):
        text  = f""" 

Optimization completed.
Generating thermodynamic data, please wait ...        
        """
        return text

    def evaluation_completed(self):
        text = """
        Results available.
        """
        return text

    def create_status_document(self):

        main_mdi_window = qtw.QMdiSubWindow()
        main_mdi_window.setWindowTitle("Status")
        #main_mdi_window.setWindowState(qtc.Qt.WindowMaximized)

        self.status_text_edit = qtw.QTextEdit(
            readOnly = True
        )

        main_mdi_window.setWidget(self.status_text_edit)
        
        self.set_status()

        return main_mdi_window


    def set_status(self):

        if self.status == None:
            self.status_text_edit.insertPlainText(self.default_text())
        else:
            self.status_text_edit.insertPlainText(self.status)

    def get_document(self):
        return self.status_doc

