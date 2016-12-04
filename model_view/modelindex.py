# encoding: utf-8
import sys
import os
from PySide import QtCore, QtGui



## pysideでは使用するタイミングですべてアイテムが読み終わってないとrowCountが取得できない。
#  なのでとりあえず放置。
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	crr_dir = os.path.dirname(__file__)
	model = QtGui.QFileSystemdModel()
	model.setRootPath(crr_dir)
	sys.exit(app.exec_())