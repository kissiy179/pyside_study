# encoding: utf-8
import sys
import os
from PySide import QtCore, QtGui


class SimpleTreeModel(QtCore.QAbstractListModel):
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

	このバージョンではアイテムデータハンドリングに必要な
	data, rowCount, columnCount, (headerData)
	を実装し、これだけで動作するQAbstractListModelを継承している
	次バージョンでQAbstractItemModelに置き換える
	'''

	columns = ['Widget Hierarchy']  # カラムリスト

	def __init__(self, parent=None):
		'''初期化処理'''
		super(SimpleTreeModel, self).__init__(parent)



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



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	treeview = QtGui.QTreeView()
	model = SimpleTreeModel()
	treeview.setModel(model)
	treeview.show()
	sys.exit(app.exec_())