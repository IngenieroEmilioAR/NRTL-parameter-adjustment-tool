from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


import pandas as pd

import os







class DataFileRoute(qtw.QWidget):
    """
    The function openfile returns a string with the route of the excel book
    with the experimental data.
    The function emit_signal recieves that string and emits it as a signal
    to the xxxClass, which 
    """    
    def __init__(self):
        super().__init__()
    def open_File(self):
        filename,_  = qtw.QFileDialog.getOpenFileName(self,
        "Select file...",
        os.path.dirname(os.path.abspath(__file__)),
        'CSV files (*.csv);; Excel Files (*.xlsx)'
        )
        return filename








class DataFrameCreation():
    """
    Pandas' Dataframe creation from a fileroute.
    """
    def __init__(self, file_route):
        self.dataframe = self.read_With_Pandas_csv(file_route)
    def read_With_Pandas_csv(self,file_route):
        dataframe = pd.read_csv(file_route)
        return dataframe
    def read_With_Pandas_xlsx(self, file_route):
        dataframe = pd.read_xlsx(file_route)
        return dataframe
    def get_Dataframe(self):
        return self.dataframe

        






class TableCreation():
    """
    qtw.QTableWidget creation either from a csv file, xlsx file
    or from a np.ndarray
    """        


    def datatable_from_csv_file(self):
        self.file_route = DataFileRoute().open_File()
        self.dfc = DataFrameCreation(self.file_route)
        self.data_frame = self.dfc.get_Dataframe()
        self.data_table = self.table_Model(self.data_frame)
    

        return self.data_table, self.data_frame, self.file_route

    def datatable_from_array(self, data):
        headers = data.keys()
        cols = len(headers)
        content = list(data.values())
        rows = max(len(v) for v in data.values())

        data_table = qtw.QTableWidget(rows, cols)
        data_table.setHorizontalHeaderLabels(headers)

        for i in range(len(content)):
            for j in range(len(content[i])):
                data_table.setItem(j,i, qtw.QTableWidgetItem(str(content[i][j])))

        data_table.resizeColumnsToContents()


        return data_table
        


        
    
    def table_Model(self, dataframe):
        rows, cols = dataframe.shape
        data_table = qtw.QTableWidget(rows,cols)
        data_table.setHorizontalHeaderLabels(dataframe.columns.values)

        #print(dataframe[0])
        
        for i in range(dataframe.shape[0]):
            for j in range(dataframe.shape[1]):
                data_table.setItem(i, j, qtw.QTableWidgetItem(str(dataframe.at[i,dataframe.columns.values[j] ])))

        return data_table



    def get_Data_Table(self, from_data = None):
        if from_data == None:
            self.data_table_frame_and_name = self.datatable_from_csv_file()
            return self.data_table_frame_and_name
        else:
            data_table = self.datatable_from_array(from_data)
            return data_table
        
        









