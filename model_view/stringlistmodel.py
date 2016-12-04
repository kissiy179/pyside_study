import sys
import os
from PySide import QtCore, QtGui



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	numbers = ['One', 'Two', 'Three', 'Four', 'Five']
	model = QtGui.QStringListModel(numbers)
	listview = QtGui.QListView()
	listview.setModel(model)
	listview.show()
	sys.exit(app.exec_())