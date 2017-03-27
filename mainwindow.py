#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *

class TopDockWidget(QWidget):
    def __init__(self, parent=None):
        super(TopDockWidget, self).__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Here is Top Dock Widget"))
        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)
        self.setStyleSheet("background-color: lightblue")

class BottomDockWidget(QWidget):
    def __init__(self, parent=None):
        super(BottomDockWidget, self).__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Here is Bottom Dock Widget"))
        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)
        self.setStyleSheet("background-color: lightpink")

class LeftDockWidget(QWidget):
    def __init__(self, parent=None):
        super(LeftDockWidget, self).__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Here is Left Dock Widget"))
        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)
        self.setStyleSheet("background-color: lightyellow")

class RightDockWidget(QWidget):
    def __init__(self, parent=None):
        super(RightDockWidget, self).__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Here is Right Dock Widget"))
        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)
        self.setStyleSheet("background-color: lightgreen")

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Here is Central Widget", self))
        self.setLayout(vbox)
        self.setStyleSheet("background-color: lightcoral")

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window Framework")
        
        # Menu Bar
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addMenu("New...")
        self.file_menu.addMenu("Open...")
        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.edit_menu.addMenu("Undo...")
        
        # Tool Bar
        self.file_tool = self.addToolBar("File")
        self.file_tool.addAction("New...")
        self.file_tool.addAction("Open...")
        self.edit_tool = self.addToolBar("Edit")
        self.edit_tool.addAction("Undo...")
        
        # Dock Widget
        ## Top
        self.top_dock = QDockWidget("Top Dock Widget", self)
        self.top_dock.setWidget(TopDockWidget(self))
        self.addDockWidget(Qt.TopDockWidgetArea, self.top_dock)
        ## Bottom
        self.bottom_dock = QDockWidget("Bottom Dock Widget", self)
        self.bottom_dock.setWidget(BottomDockWidget(self))
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock)
        ## Left
        self.left_dock = QDockWidget("Left Dock Widget", self)
        self.left_dock.setWidget(LeftDockWidget(self))
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)
        ## Right
        self.right_dock = QDockWidget("Right Dock Widget", self)
        self.right_dock.setWidget(RightDockWidget(self))
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)
        
        # Central Widget
        self.setCentralWidget(CentralWidget(self))
        
        # Status Bar
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage("Here is Status Bar", 5000)
        self.setStatusBar(self.status_bar)

def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()