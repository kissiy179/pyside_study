import sys
import os
from PySide import QtCore, QtGui



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	splitter = QtGui.QSplitter()
	crr_dir = os.path.dirname(__file__)
	model = QtGui.QFileSystemModel()
	model.setRootPath(crr_dir)
	tree = QtGui.QTreeView(splitter)
	tree.setModel(model)
	tree.setRootIndex(model.index(crr_dir))
	lst = QtGui.QListView(splitter)
	lst.setModel(model)
	lst.setRootIndex(model.index(crr_dir))
	splitter.show()
	sys.exit(app.exec_())