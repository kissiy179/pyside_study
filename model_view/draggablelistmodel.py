import sys
from PySide import QtCore, QtGui



class DragDropListModel(QtCore.QAbstractListModel):

	columns = ['test']

	def __init__(self, strings, parent=None):
		super(DragDropListModel, self).__init__(parent)
		self.strings = strings



	def supportedDropActions(self):
		return QtCore.Qt.MoveAction



	def rowCount(self, parent=None):
		return len(self.strings)


	def data(self, index, role):
		if not index.isValid():
			return None
		if index.row() >= self.rowCount():
			return None
		if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
			return self.strings[index.row()]
		return None



	def setData(self, index, value, role=QtCore.Qt.EditRole):
		if index.isValid and role == QtCore.Qt.EditRole:
			self.strings[index.row()] = str(value)
			self.dataChanged.emit(index, index)
			return True
		return False



	def flags(self, index):
		defaultFlags = super(DragDropListModel, self).flags(index) | QtCore.Qt.ItemIsEditable
		if index.isValid:
			return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | defaultFlags
		else:
			return QtCore.Qt.ItemIsDragEnabled | defaultFlags


	def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
		self.beginInsertRows(parent, position, position + rows -1)
		for row in range(rows):
			self.strings.insert(position, '--- tmp ---')
		self.endInsertRows()
		return True



	def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
		self.beginRemoveRows(parent, position, position + rows -1)
		for row in range(rows):
			del self.strings[position]
		self.endRemoveRows()
		return True



	def mimeData(self, indexes):
		mimeData = super(DragDropListModel, self).mimeData(indexes)
		mimeData.setText(indexes[0].data(role=QtCore.Qt.DisplayRole))
		return mimeData



	def dropMimeData(self, data, action, row, column, parent):
		print 'data =', data.text()
		print 'action =', action
		print 'row =', row
		super(DragDropListModel, self).dropMimeData(data, action, row, column, parent)
		index = self.index(row, column, parent)
		self.setData(index, data.text())
		return True



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	view = QtGui.QListView()
	view.setModel(DragDropListModel(['test{0}'.format(i) for i in range(5)]))
	view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
	view.setDragEnabled(True)
	view.setAcceptDrops(True)
	view.setDropIndicatorShown(True)

	view.show()
	sys.exit(app.exec_())