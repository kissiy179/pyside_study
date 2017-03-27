
## -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

class SpinBoxDelegate(QtGui.QItemDelegate):

    def createEditor(self, parent, option, index):
        #編集する時に呼ばれるWidgetを設定
        editor = QtGui.QDoubleSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)

        return editor

    def setEditorData(self, spinBox, index):
        #編集されたときに呼ばれ、セットされた値をWidgetにセットする?
        value = index.model().data(index, QtCore.Qt.EditRole)
        spinBox.setValue(value)
        
    def setModelData(self, spinBox, model, index):
        #ModelにSpinboxの編集した値をセットする?
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self,painter,option,index):
        #通常時の表示
        num = index.data()
        #Barの表示
        #Column 2 の時だけBarを表示する

        if index.column() == 0:
            box = QtGui.QStyleOptionComboBox()
            box.rect = option.rect
            box.currentText = str(num)
            QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_ComboBoxLabel, box, painter)

        if index.column() == 1:
            bar = QtGui.QStyleOptionProgressBar()
            bar.rect = option.rect
            bar.rect.setHeight(option.rect.height() - 1)
            bar.rect.setTop(option.rect.top() + 1)
            bar.minimum = 0
            bar.maximum = 100
            bar.progress = int(num)
            bar.textVisible = True
            bar.text = str(num) + '%'
            bar.textAlignment = QtCore.Qt.AlignCenter
            QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_ProgressBar, bar, painter)
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    model = QtGui.QStandardItemModel(4, 2)
    tableView = QtGui.QTableView()
    tableView.setModel(model)

    delegate = SpinBoxDelegate()
    tableView.setItemDelegate(delegate)

    for row in range(4):
        for column in range(2):
            index = model.index(row, column, QtCore.QModelIndex())
            model.setData(index, (row + 1) * (column + 1))

    tableView.setWindowTitle("Spin Box Delegate")
    tableView.show()
    sys.exit(app.exec_())
