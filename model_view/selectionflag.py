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
    bottomRight = model.index(5,2)
    selection = QtGui.QItemSelection(topLeft, bottomRight)
    selectionModel.select(selection, QtGui.QItemSelectionModel.Select)

    toggleSelection = QtGui.QItemSelection()
    topLeft = model.index(2,1)
    bottomRight = model.index(7,3)
    toggleSelection.select(topLeft, bottomRight)
    selectionModel.select(toggleSelection, QtGui.QItemSelectionModel.Toggle)
    
    table.show()
    sys.exit(app.exec_())