# encoding: utf-8
import sys
import os
from PySide import QtCore, QtGui


class SimpleTreeModel(QtCore.QAbstractItemModel):
	'''
	シンプルなツリー構造を扱うモデル
	仕様：
	・QWidgetを直接index.internalPointerに持つ
	・列数は1
	・行数は子ウィジェットの数
	・トップレベルのアイテム(ウィジェット)は1つ、メンバー変数topWidgetで保持
	・各アイテムの文字列表現はウィジェットのクラス名

	実装履歴：
	QAbstractItemModelには以下の3つの主な仮想関数がある
	・アイテムデータハンドリング(必須)
	・ナビゲーションとインデックス生成(必須)
	・ドラッグアンドドロップサポート

	このバージョンではアイテムデータハンドリングに必要な関数に加え、
	ナビゲーションとインデックス生成に必要な関数
	index, parent
	を実装する
	それに伴いスーパークラスをQAbstractItemModeに変更する
	'''

	columns = ['Widget Hierarchy']  # カラムリスト

	def __init__(self, parent=None):
		'''初期化処理'''
		super(SimpleTreeModel, self).__init__(parent)
		self.topWidget = QtGui.QWidget()



	def data(self, index, role=QtCore.Qt.DisplayRole):
		'''
		アイテムのデータを返す関数
		最低でもroleがDisplayRoleのときに値を返さないと実用性がない
		'''
		if role != QtCore.Qt.DisplayRole or not index.isValid():
			return None
		return type(QtGui.QWidget(index.internalPointer())).__name__



	def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
		'''
		ヘッダーとして表示させるデータを返す関数
		必須ではないがあった方がよい
		orientaionは水平(Horizontal)、垂直(Verchical)が入力され、sectionには何番目かが入力される
		'''
		if orientation != QtCore.Qt.Horizontal or role != QtCore.Qt.DisplayRole:
			return None
		return self.columns[section]



	def rowCount(self, parent):
		'''
		parentを親に持つアイテムの行数を返す関数
		子ウィジェットの数を行数とする
		ただし、ルート直下の行数は1とする
		'''
		if parent.isValid():
			wgt = QtGui.QWidget(parent.internalPointer())
			return len(wgt.findChildren(QtGui.QWidget))
		return 1



	def columnCount(self, parent):
		'''
		parentを親に持つアイテムの列数を返す関数
		'''
		return len(self.columns)



	def index(self, row, column, parent):
		if not parent.isValid():
			if(row == 0 and column == 0):
				return self.createIndex(0,0, self.topWidget)
			return QtCore.QModelIndex()
		if column != 0 or parent.column() != 0:
			return QtCore.QModelIndex()
		wgt = QtGui.QWidget(parent.internalPointer())
		children = wgt.findChildren(QtGui.QWidget)
		return createIndex(row, 0, children[row]) if row < len(children) else QtCore.QModelIndex()



	def parent(self, index):
		if index.isValid():
			wgt = QtGui.QWidget(index.internalPointer())
			if not wgt == self.topWidget:
				parent = wgt.parentWidget()
				row = parent.findChildren(QtGui.QWidget).index(wgt)
				if row > -1:
					return self.createIndex(row, 0, parent)
		return QtCore.QModelIndex()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	treeview = QtGui.QTreeView()
	model = SimpleTreeModel()
	treeview.setModel(model)
	treeview.show()
	sys.exit(app.exec_())