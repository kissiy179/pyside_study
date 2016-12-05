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
	indexes = selectionModel.selectedIndexes()
	for index in indexes:
		text = '({0},{1})'.format(index.row(), index.column())
		model.setData(index, text)
	table.show()
	sys.exit(app.exec_())