import sys
import os
from PySide import QtCore, QtGui



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    model = QtGui.QStandardItemModel(8, 4)
    table = QtGui.QTableView()
    table.setModel(model)
    selectionModel = table.selectionModel()

    topLeft = model.index(0,0)
    bottomRight = model.index(model.rowCount()-1, model.columnCount()-1)
    columnSelection = QtGui.QItemSelection(topLeft, bottomRight)
    selectionModel.select(columnSelection, QtGui.QItemSelectionModel.Select)

    
    table.show()
    sys.exit(app.exec_())