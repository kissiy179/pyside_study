import sys
import os
import functools
import uuid
from PySide import QtCore, QtGui


class StringListModel(QtCore.QAbstractListModel):

	def __init__(self, strings, parent=None):
		super(StringListModel, self).__init__(parent)
		self.strings = strings


	def rowCount(self, parent=None):
		return len(self.strings)


	def flags(self, index):
		if not index.isValid():
			return QtCore.Qt.ItemIsEnabled
		return QtCore.QAbstractItemModel.flags(self, index) | QtCore.Qt.ItemIsEditable


	def data(self, index, role):
		if not index.isValid():
			return None
		elif index.row() >= self.rowCount:
			return None
		elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
			return self.strings[index.row()]
		else:
			return None



	def setData(self, index, value, role):
		if index.isValid and role == QtCore.Qt.EditRole:
			self.strings[index.row()] = str(value)
			self.dataChanged.emit(index, index)
			return True
		return False



	def headerData(self, section, orientation, role):
		if role != QtCore.Qt.DisplayRole:
			return None
		if orientation == QtCore.Qt.Horizontal:
			return 'column {0}'.format(section)
		else:
			return 'row {0}'.format(section)



	def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
		self.beginInsertRows(parent, position, position + rows -1)
		for row in range(rows):
			self.strings.insert(position, str(uuid.uuid4()))
		self.endInsertRows()
		return True



	def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
		self.beginRemoveRows(parent, position, position + rows -1)
		for row in range(rows):
			del self.strings[position]
		self.endRemoveRows()
		return True



if __name__ == '__main__':

	def insertToSelection():
		indexes = selection.selectedIndexes()
		row = indexes[0].row() if indexes else 0
		model.insertRows(row, 1)

	def removeFromSelection():
		indexes = selection.selectedIndexes()
		row = indexes[0].row() if indexes else 0
		model.removeRows(row, 1)

	app = QtGui.QApplication(sys.argv)
	wgt = QtGui.QWidget()
	layout = QtGui.QVBoxLayout()
	listview = QtGui.QTreeView()
	model = StringListModel(['tamaki', 'chiyu', 'satoshi'])
	listview.setModel(model)
	selection = listview.selectionModel()
	layout.addWidget(listview)

	btn = QtGui.QPushButton('insert Row')
	btn.clicked.connect(insertToSelection)
	layout.addWidget(btn)
	btn = QtGui.QPushButton('remove Row')
	btn.clicked.connect(removeFromSelection)
	layout.addWidget(btn)

	wgt.setLayout(layout)
	wgt.show()
	sys.exit(app.exec_())