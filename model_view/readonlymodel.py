import sys
import os
from PySide import QtCore, QtGui


class StringListModel(QtCore.QAbstractListModel):

	def __init__(self, strings, parent=None):
		super(StringListModel, self).__init__(parent)
		self.strings = strings


	def rowCount(self, parent=None):
		return len(self.strings)


	def data(self, index, role):
		if not index.isValid():
			return None
		elif index.row() >= self.rowCount:
			return None
		elif role == QtCore.Qt.DisplayRole:
			return self.strings[index.row()]
		else:
			return None



	def headerData(self, section, orientation, role):
		if role != QtCore.Qt.DisplayRole:
			return None
		if orientation == QtCore.Qt.Horizontal:
			return 'column {0}'.format(section)
		else:
			return 'row {0}'.format(section)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	listview = QtGui.QTreeView()
	model = StringListModel(['tamaki', 'chiyu', 'satoshi'])
	listview.setModel(model)
	listview.show()
	sys.exit(app.exec_())