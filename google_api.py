"""
module for working with Google Sheet
check if module oauth2client installed in your environment
"""

import os.path


import pygsheets


import db
from log import log


class GoogleAPI:
    """
    This class for creating object for sheet from Google Sheet
    and can return data from cell and write data and color to cell
    """

    def __init__(self, credential, sheet, worksheet):
        """
        get object the sheet with wich we can work
        :param credential: string with path to json file with credential (see API Google console for developers)
        :param sheet: string with name of online sheet into Google
        :param worksheet: string with name of worksheet
        example: obj = GoogleAPI("path/to/file.json", "Sheet", "WorkSheet")
        """

        if not (os.path.exists(credential) and os.path.isfile(credential)):
            raise FileNotFoundError("File credential not found. Check path, pls")

        client = pygsheets.authorize(service_file=credential)
        sh = client.open(sheet)
        self.__wks = sh.worksheet_by_title(worksheet)

    def get_value(self, column, row):
        """
        method returns cell's value
        :param column: string with label of column
        :param row: string with number of row
        :return: string with cell's value
        example: obj.get_value("A", "2")
        """

        cell_value = self.__wks.cell(column + row).value

        return cell_value

    def get_all_ttn(self, c_ttn, c_symbol, s_row):
        worksheet = self.__wks.get_all_values()
        result = {}
        for index, item in enumerate(worksheet):
            if index < s_row - 1:
                continue
            if not item[c_ttn].isdigit():
                continue
            # write all new TTN to the base
            if not db.find_ttn(item[c_ttn]):
                db.write_newttn(item[c_ttn], item[c_symbol], index+1)
                log.info(f"write {item[c_ttn]} to database")
            if item[c_symbol].strip() in ["+", "\'+", "-"]:
                continue

            result[item[c_ttn].strip()] = [index+1, item[c_symbol]]

        return result

    def write_value(self, column, row, value):
        """
        method write value to cell
        :param column: string with label of column
        :param row: string with number of row
        :param value: value wich writing
        :return: None
        example: obj.write_value("A","2", "Hello")
        """
        # symbol +(plus) can't write to cell in Google Sheet so we change it
        if value == "+":
            value = "'+"

        cell = self.__wks.cell(column + row)
        cell.value = value

    def color_cell(self, column, row, color):
        """
        method set color of cell
        :param column: string with column's label
        :param row:string with number of row
        :param color: string with name of color(red, green, yellow)
        :return: None
        example: obj.color_cell("A", "2", "red")
        """
        set_color = (1, 1, 1, 1)
        if color == "red":
            set_color = (1, 0, 0, 1)
        if color == "green":
            set_color = (0, 1, 0, 1)
        if color == "yellow":
            set_color = (1, 1, 0, 1)

        cell = self.__wks.cell(column + row)
        cell.color = set_color

    def find_by_col(self, col, value):
        values = self.__wks.get_col(col=col+1)
        try:
            result = values.index(value) + 1
        except ValueError:
            result = None
        return result


if __name__ == '__main__':
    print("Module must be imported")
