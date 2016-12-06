# encoding: utf-8
import sys
import os
from PySide import QtCore, QtGui



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    crr_dir = os.path.dirname(__file__)
    model = QtGui.QFileSystemModel()
    model.setRootPath(crr_dir)

    # ↓↓↓ これやってあげないとなぜかファイルシステムのパースしない ===================================================
    treeview = QtGui.QTreeView()
    app.processEvents(QtCore.QEventLoop.AllEvents)
    # ↑↑↑ ========================================================================================

    parent_index = model.index(crr_dir)
    row_count = model.rowCount(parent_index)
    wgt = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    for row in range(row_count):
        index = model.index(row, 0, parent_index)
        txt = index.data(QtCore.Qt.DisplayRole)
        btn = QtGui.QPushButton(txt)
        layout.addWidget(btn)
    wgt.setLayout(layout)
    wgt.show()
    sys.exit(app.exec_())