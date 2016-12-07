import sys
import os
from PySide import QtCore, QtGui



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    model = QtGui.QStandardItemModel(8, 4)
    table = QtGui.QTableView()
    table.setModel(model)
    selectionModel = table.selectionModel()

    topLeft = model.index(0,1)
    bottomRight = model.index(0,2)
    columnSelection = QtGui.QItemSelection(topLeft, bottomRight)
    selectionModel.select(columnSelection, QtGui.QItemSelectionModel.Select | QtGui.QItemSelectionModel.Columns)

    topLeft = model.index(0,0)
    bottomRight = model.index(1,0)
    rowSelection = QtGui.QItemSelection(topLeft, bottomRight)
    selectionModel.select(rowSelection, QtGui.QItemSelectionModel.Select | QtGui.QItemSelectionModel.Rows)
    
    table.show()
    sys.exit(app.exec_())