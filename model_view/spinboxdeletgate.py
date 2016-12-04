import sys
import os
from PySide import QtCore, QtGui


class SpinBoxDelegate(QtGui.QItemDelegate):

	def __init__(self, parent=None):
		super(SpinBoxDelegate, self).__init__(parent)


	def createEditor(self, parent, option, index):
		print 'createEditor'
		editor = QtGui.QSpinBox(parent)
		editor.setMinimum(0)
		editor.setMaximum(10000)
		return editor


	def setEditorData(self, editor, index):
		value = int(index.data(QtCore.Qt.EditRole))
		print index.row(), '---&', value
		# print int(value), '---' 
		# print 'test'
		# spinbox = QtGui.QSpinBox(editor)
		editor.setValue(value)


	def setModelData(self, editor, model, index):
		#spinbox = QtGui.QSpinBox(editor)
		value = editor.interpretText()
		model.setData(index, value, QtCore.Qt.EditRole)


	def updateEditorGeometory(self, editor, option, index):
		editor.setGeometry(option.rect)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	numbers = ['1', '2', '3', '4', '5']
	model = QtGui.QStringListModel(numbers)
	listview = QtGui.QListView()
	listview.setModel(model)
	listview.setItemDelegate(SpinBoxDelegate())
	listview.show()
	sys.exit(app.exec_())