# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore

import sys

HEADER_DATA = ["ID","NAME","COMMENT"]

class TreeData(object):
    """
    中に表示されるデータの構造体
    """

    def __init__(self, data):
        self.data = data
    def columnNum(self):
        return len(self.data)


class TreeItem(object):
    """
    Treeに表示されるデータをコントロールするためのクラス
    """

    def __init__(self, task=None, parentItem=None):

        self.task = task
        self.parentItem = parentItem
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):

        return self.task.columnNum()

    def data(self, column):

        if self.task == None:
            return ""
        else:
            return self.task.data[column]

    def parent(self):

        return self.parentItem

    def row(self):

        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def clear(self):

        self.childItems = []


class treeModel(QtCore.QAbstractItemModel):
    """
    Model本体
    """
    tasks = []

    def __init__(self, items=None, parent=None):

        super(treeModel, self).__init__(parent)

        self.rootItem = TreeItem()
        if items is not None:
            self.addItems(items)

    def addItem(self,item):

        t_obj = TreeData(item)
        self.tasks.append(t_obj)
        self.setupModelData()

    def addItems(self,items):

        for i in items:
            t_obj = TreeData(i)
            self.tasks.append(t_obj)
        self.setupModelData()

    def setItem(self, items):

        self.tasks = []

        self.addItems(items)
        self.setupModelData()

    def data(self, index, role):

        if not index.isValid():
            return QtCore.QModelIndex()

        item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())

    def headerData(self, column, orientation, role):

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return HEADER_DATA[column]

    def columnCount(self, parent=None):

        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(HEADER_DATA)

    def rowCount(self, parent=QtCore.QModelIndex()):

        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def setupModelData(self):

        self.rootItem.clear()

        for task in self.tasks:
            obj = TreeItem(task, self.rootItem)
            self.rootItem.appendChild(obj)

    def parent(self, index):

        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QtCore.QModelIndex()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def index(self, row, column, parent):

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()


def main():
    app = QtGui.QApplication(sys.argv)

    dialog = QtGui.QDialog()
    
    items = [(10, 'remi', 'hello world'),
             (12, 'remi', 'hoge hoge')]

    model = treeModel(items)
    
    dialog.setMinimumSize(400, 150)
    layout = QtGui.QVBoxLayout(dialog)
    tv = QtGui.QTreeView(dialog)
    tv.setModel(model)
    layout.addWidget(tv)


    dialog.show()
    sys.exit(app.exec_())

main()