#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################
import copy
from PySide import QtCore, QtGui

import simpletreemodel_rc


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []


    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column=0):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class TreeModel(QtCore.QAbstractItemModel):

    crritem = None
    startparentitem = None
    dragitemposition = -1

    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(("Title", "Summary"))
        self.setupModelData(data.split('\n'), self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())


    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)


        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, lines, parent):
        for i in range(10):
            name = 'node{0}'.format(i)
            parent.appendChild(TreeItem([name], parent))
        return

        parents = [parent]
        indentations = [0]

        number = 0

        while number < len(lines):
            position = 0
            while position < len(lines[number]):
                if lines[number][position] != ' ':
                    break
                position += 1

            lineData = lines[number][position:].strip()

            if lineData:
                # Read the column data from the rest of the line.
                columnData = [s for s in lineData.split('\t') if s]

                if position > indentations[-1]:
                    # The last child of the current parent is now the new
                    # parent unless the current parent has no children.

                    if parents[-1].childCount() > 0:
                        parents.append(parents[-1].child(parents[-1].childCount() - 1))
                        indentations.append(position)

                else:
                    while position < indentations[-1] and len(parents) > 0:
                        parents.pop()
                        indentations.pop()

                # Append a new item to the current parent's list of children.
                parents[-1].appendChild(TreeItem(columnData, parents[-1]))

            number += 1


    def flags(self, index):
        defaultFlags = super(TreeModel, self).flags(index) | QtCore.Qt.ItemIsEditable
        if index.isValid:
            return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | defaultFlags
        else:
            return QtCore.Qt.ItemIsDragEnabled | defaultFlags


    def supportedDropActions(self):
        return QtCore.Qt.MoveAction


    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), data=['a', 'b']):
        print 'insertRows:', position, rows, parent
        self.beginInsertRows(parent, position, position + rows -1)
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        for row in range(rows):
            # parentItem.childItems.insert(position, TreeItem(data, parentItem))
            self.crritem.parentItem = parentItem
            parentItem.childItems.insert(position, self.crritem)
            # self.strings.insert(position, '--- tmp ---')appendChild()
        self.endInsertRows()
        return True




    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        print 'removeRows:', position, rows, parent
        self.beginRemoveRows(parent, position, position + rows -1)
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        delitem = self.startparentitem.childItems[self.dragitemposition]
        if delitem.parentItem == self.crritem.parentItem and delitem.row() > self.crritem.row():
            self.dragitemposition += 1
        del self.startparentitem.childItems[self.dragitemposition]
        self.endRemoveRows()
        return True



    def mimeData(self, indexes):
        print 'mimeData'
        mimeData = super(TreeModel, self).mimeData(indexes)
        encodeData = QtCore.QByteArray()
        stream = QtCore.QDataStream(encodeData, QtCore.QIODevice.WriteOnly)
        for index in indexes:
            if index.isValid() and index.column() == 0:
                # text = self.data(index, QtCore.Qt.DisplayRole)()
                self.crritem = copy.deepcopy(index.internalPointer())
                self.startparentitem = index.internalPointer().parentItem
                self.dragitemposition = index.row()
                # stream.writeString(text)
        mimeData.setData('application/vnd.text.list', encodeData)
        return mimeData


    def dropMimeData(self, data, action, row, column, parent):
        print 'dropMimeData'
        if action == QtCore.Qt.IgnoreAction:
            return True
        if not data.hasFormat('application/vnd.text.list'):
            return False
        if row != -1:
            beginRow = row
            # print 'row = -1'
        elif parent.isValid():
            beginRow = parent.row()
            # print 'isValid'
        else:
            beginRow = self.rowCount(parent)
            # print 'else'
        # print 'insert row = ', beginRow
        encodeData = data.data('application/vnd.text.list')
        stream = QtCore.QDataStream(encodeData, QtCore.QIODevice.ReadOnly)
        newItems = []
        rows = 1
        self.insertRows(beginRow, rows, parent, newItems)
        return True



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    f = QtCore.QFile(':/default.txt')
    f.open(QtCore.QIODevice.ReadOnly)
    model = TreeModel(str(f.readAll()))
    f.close()

    view = QtGui.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.setDragEnabled(True)
    view.setAcceptDrops(True)
    # view.setDropIndicatorShown(True)
    view.resize(1000, 500)
    view.show()
    sys.exit(app.exec_())
