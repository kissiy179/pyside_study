import sys
from PySide import QtGui, QtCore


class Test(object):

    def do(self):
        print 'do anything!!!'

print QtGui.QMenu
class MyMenu(QtGui.QMenu):

    def __init__(self, parent=None, core=Test()):
        super(MyMenu, self).__init__(parent)
        # self.core = core
        # self.AddAction('test')
        # self.AddAction('test2')




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    menu = MyMenu()
    menu.addAction('test', Test().do)
    menu.addAction('test2')
    menu.addAction('test3')
    menu.popup(QtGui.QCursor.pos())
    sys.exit(app.exec_())