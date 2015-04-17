__author__ = 'gru'


import xlrd # used for reading excel files
import numpy as np # numerical library
from datetime import datetime, timedelta, date


import training_constants as Constants
import abc

class TrainingDataParser:
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def read_training_data(self,path):
        raise NotImplementedError



class XlsParser(TrainingDataParser):

    start_row = 4

    def __init__(self, path):
        self.path=path
        self.book = xlrd.open_workbook(path)
        return

    def read_cell_value(self, sheet_id, row_id, col_id):
        return self.book.sheet_by_index(sheet_id).cell_value(row_id, col_id)


    def read_training_data(self):

        sheet = self.get_sheet_from_xls(self.path,0)

        dates = self.read_date_cells_as_str(self.book, sheet, 0, self.start_row)
        self.data={Constants.date_key: dates}

        value_list=[]
        key=''
        key_list=[]
        for col_index in range(2,sheet.ncols):
            for row_index in range(0,sheet.nrows):
                if (not(sheet.cell_type(row_index, col_index) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK))):

                    if (sheet.cell_type(row_index, col_index) == xlrd.XL_CELL_TEXT):
                        string = sheet.cell(rowx=row_index,colx=col_index).value


                        if('[' in string):
                            string_list = string.split('[')
                            string = string_list[0].rstrip()

                        if(key==''):
                            #string = u.encode('ascii')
                            key = string
                            key_list.append(string)

                        else:
                            value_list.append(string)

                    elif (sheet.cell_type(row_index,col_index) == xlrd.XL_CELL_NUMBER):
                        value_list.append(sheet.cell(rowx=row_index,colx=col_index).value)

            if(key!= ''):
                self.data.update({key: value_list})

            key = '' # set key to '' to account for empty columns
            value_list=[]
        self.print_dict(self.data, self.data.keys())




    @staticmethod
    def get_sheet_from_xls(path, sheetId):
        book = xlrd.open_workbook(path)
        return book.sheet_by_index(sheetId)

    @staticmethod
    def col_values_not_null(sheet, colx, start_rowx=0, end_rowx=None):
        values = sheet.col_values(colx, start_rowx, end_rowx)
        values_filtered = [x if x != ''  else 0 for x in values]
        #[ x if x%2 else x*100 for x in range(1, 10) ]

        print values_filtered
        return values_filtered

    @staticmethod
    def read_date_cells_as_str(book, sheet, colId, row_start=0):
        dates=[]
        date_obj = date.today()
        for row_index in range(row_start, sheet.nrows):
                cell = sheet.cell(row_index, colId)
                if cell.ctype == xlrd.XL_CELL_DATE:
                    # Returns a tuple.
                    dt_tuple = xlrd.xldate_as_tuple(sheet.cell_value(row_index, colId), book.datemode)
                    # Create datetime object from this tuple.
                    date_from_cell = date_obj.replace(
                    dt_tuple[0], dt_tuple[1], dt_tuple[2])
                    dates.append(date_from_cell.isoformat())


        return dates

    def get_sheet_names(self):
        if self.book != None:
            return self.book.sheet_names()
        else:
            return Exception #Todo proper exception

    @staticmethod
    def print_dict(d, key_list):
        for key in key_list:
            print key
            print d[key]


