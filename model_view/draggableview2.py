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
		encodeData = QtCore.QByteArray()
		stream = QtCore.QDataStream(encodeData, QtCore.QIODevice.WriteOnly)
		for index in indexes:
			if index.isValid():
				text = self.data(index, QtCore.Qt.DisplayRole)
				stream.writeString(text)
		mimeData.setData('application/vnd.text.list', encodeData)
		print '--------------------------'
		print mimeData
		print repr(encodeData)
		print stream
		print mimeData.text()
		return mimeData



	def dropMimeData(self, data, action, row, column, parent):
		print row, column, parent, '----'
		if action == QtCore.Qt.IgnoreAction:
			return True
		if not data.hasFormat('application/vnd.text.list'):
			return False
		if column > 0:
			return False
		if row != -1:
			beginRow = row
		elif parent.isValid():
			beginRow = parent.row()
		else:
			beginRow = self.rowCount()
		encodeData = data.data('application/vnd.text.list')
		stream = QtCore.QDataStream(encodeData, QtCore.QIODevice.ReadOnly)
		newItems = []
		rows = 0
		while not stream.atEnd():
			text = stream.readString()
			newItems.append(text)
			rows += 1
		self.insertRows(beginRow, rows)
		for text in newItems:
			idx = self.index(beginRow, 0)
			self.setData(idx, text)
			beginRow += 1
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