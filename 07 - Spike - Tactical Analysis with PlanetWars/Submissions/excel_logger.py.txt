# & Project: Tactical Analysis with PlanetWars
# & Author: Thomas Horsley - 103071494
# & Date: 29/03/23

# * IMPORTANT
# * As there's so many comments contained in these files, I'd 110% recommend installing the
# * colorful comments VSCode extension to aid in readability.

#! ======================================================================================== !#
#!                                        Overview

# ^ This class will allow Planet Wars to print the data into an excel
# ^ spreadsheet and manipulate the data.

from openpyxl import Workbook
from openpyxl.styles import Font
from players import Player


class ExcelLogger(object):
    # TODO: Initialize the logger
    def __init__(self, book_name: str, sheet_name: str):
        self.workbook = Workbook()
        self.book_name = self.__validateBookName(book_name)
        self.worksheet = self.__initWorksheet(sheet_name)

        self.__cleanupExcelDefaults

    # Summary: Adds headers to worksheet for numpy analysis
    def __initWorksheet(self, sheet_name: str):
        self.workbook.create_sheet(sheet_name, 0)
        worksheet = self.workbook[sheet_name]

        headers = ["Match ID", "Winner", "Loser", "Map"]

        for col, header in enumerate(headers):
            cell = worksheet.cell(row=1, column=col + 1, value=header)
            cell.font = Font(bold=True, italic=True)

        self.workbook.save(self.book_name)
        return worksheet

    # Summary: Cleans up default excel file
    def __cleanupExcelDefaults(self):
        for sheet_name in self.workbook.sheetnames:
            if sheet_name == "Sheet":
                sheet = self.workbook.get_sheet_by_name(sheet_name)
                self.workbook.remove(sheet)

                self.workbook.save(self.book_name)
                return

    # Summary: Ammends .xlsx if needed
    def __validateBookName(self, given_book_name):
        book_name = None

        if given_book_name[-5] == ".xlsx":
            book_name = given_book_name
        else:
            book_name = given_book_name + ".xlsx"
        return book_name

    # Summary: Finds empty row and calls __fillRow()
    def appendWinData(self, match_id: int, winner, opponent, map_name: str):
        if self.__tieTest(winner):
            winner_name = "tie"
            opponent_name = "tie"
        else:
            winner_name = winner.name
            opponent_name = opponent[0].name

        max_row = 200
        data = [match_id, winner_name, opponent_name, map_name]

        if type(winner_name) == int:
            data = [match_id, "Tie", "Tie", map_name]

        for row_index in range(1, max_row):
            cell = self.worksheet.cell(row=row_index, column=1)
            if cell.value == None:
                self.__fillRow(data, row_index)
                return

    # Summary: Appends a list of data to a row
    def __fillRow(self, data: list, row_id: int):
        for col, datum in enumerate(data):
            self.worksheet.cell(row=row_id, column=col + 1, value=datum)

        self.workbook.save(self.book_name)

    # Summary: Tests for a tie returns true if tie occur
    def __tieTest(self, winner) -> bool:
        if type(winner) is int:
            return True
        elif type(winner) is Player:
            return False
        else:
            print("Winner was not of type int or string")
