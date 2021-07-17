# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'front/test-ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(777, 475)
        MainWindow.setMinimumSize(QtCore.QSize(696, 475))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTasks = QtWidgets.QLabel(self.centralwidget)
        self.labelTasks.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTasks.setObjectName("labelTasks")
        self.verticalLayout.addWidget(self.labelTasks)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.taskSelect = QtWidgets.QComboBox(self.centralwidget)
        self.taskSelect.setObjectName("taskSelect")
        self.taskSelect.addItem("")
        self.taskSelect.addItem("")
        self.horizontalLayout_2.addWidget(self.taskSelect)
        self.taskInfo = QtWidgets.QPushButton(self.centralwidget)
        self.taskInfo.setMaximumSize(QtCore.QSize(25, 16777215))
        self.taskInfo.setObjectName("taskInfo")
        self.horizontalLayout_2.addWidget(self.taskInfo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.verticalLayout.addWidget(self.line_1)
        self.labelSolutions = QtWidgets.QLabel(self.centralwidget)
        self.labelSolutions.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSolutions.setObjectName("labelSolutions")
        self.verticalLayout.addWidget(self.labelSolutions)
        self.listSolutions = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listSolutions.sizePolicy().hasHeightForWidth())
        self.listSolutions.setSizePolicy(sizePolicy)
        self.listSolutions.setMinimumSize(QtCore.QSize(181, 0))
        self.listSolutions.setObjectName("listSolutions")
        item = QtWidgets.QListWidgetItem()
        self.listSolutions.addItem(item)
        self.verticalLayout.addWidget(self.listSolutions)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.langSelect = QtWidgets.QComboBox(self.centralwidget)
        self.langSelect.setIconSize(QtCore.QSize(16, 16))
        self.langSelect.setFrame(True)
        self.langSelect.setObjectName("langSelect")
        self.langSelect.addItem("")
        self.langSelect.addItem("")
        self.langSelect.addItem("")
        self.verticalLayout.addWidget(self.langSelect)
        self.runTests = QtWidgets.QPushButton(self.centralwidget)
        self.runTests.setObjectName("runTests")
        self.verticalLayout.addWidget(self.runTests)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.solutionTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.solutionTitle.sizePolicy().hasHeightForWidth())
        self.solutionTitle.setSizePolicy(sizePolicy)
        self.solutionTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.solutionTitle.setObjectName("solutionTitle")
        self.verticalLayout_2.addWidget(self.solutionTitle)
        self.codeBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.codeBrowser.sizePolicy().hasHeightForWidth())
        self.codeBrowser.setSizePolicy(sizePolicy)
        self.codeBrowser.setMinimumSize(QtCore.QSize(500, 290))
        self.codeBrowser.setObjectName("codeBrowser")
        self.verticalLayout_2.addWidget(self.codeBrowser)
        self.solutionOutput = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.solutionOutput.sizePolicy().hasHeightForWidth())
        self.solutionOutput.setSizePolicy(sizePolicy)
        self.solutionOutput.setObjectName("solutionOutput")
        self.verticalLayout_2.addWidget(self.solutionOutput)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 777, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.actionAdd_Task = QtWidgets.QAction(MainWindow)
        self.actionAdd_Task.setObjectName("actionAdd_Task")
        self.actionAdd_Solution = QtWidgets.QAction(MainWindow)
        self.actionAdd_Solution.setObjectName("actionAdd_Solution")
        self.actionAdd_Tests = QtWidgets.QAction(MainWindow)
        self.actionAdd_Tests.setObjectName("actionAdd_Tests")
        self.actionLanguage_detection_On = QtWidgets.QAction(MainWindow)
        self.actionLanguage_detection_On.setObjectName("actionLanguage_detection_On")
        self.actionSetting = QtWidgets.QAction(MainWindow)
        self.actionSetting.setObjectName("actionSetting")
        self.actionDetect_language = QtWidgets.QAction(MainWindow)
        self.actionDetect_language.setObjectName("actionDetect_language")
        self.menuFile.addAction(self.actionAdd_Task)
        self.menuFile.addAction(self.actionAdd_Solution)
        self.menuSettings.addAction(self.actionDetect_language)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Checker"))
        self.labelTasks.setText(_translate("MainWindow", "Tasks"))
        self.taskSelect.setItemText(0, _translate("MainWindow", "test_task"))
        self.taskSelect.setItemText(1, _translate("MainWindow", "task1"))
        self.taskInfo.setText(_translate("MainWindow", "?"))
        self.labelSolutions.setText(_translate("MainWindow", "Solutions"))
        __sortingEnabled = self.listSolutions.isSortingEnabled()
        self.listSolutions.setSortingEnabled(False)
        item = self.listSolutions.item(0)
        item.setText(_translate("MainWindow", "solutionFileName.go"))
        item.setToolTip(_translate("MainWindow", "AuthorName"))
        self.listSolutions.setSortingEnabled(__sortingEnabled)
        self.langSelect.setItemText(0, _translate("MainWindow", "python"))
        self.langSelect.setItemText(1, _translate("MainWindow", "cpp"))
        self.langSelect.setItemText(2, _translate("MainWindow", "golang"))
        self.runTests.setText(_translate("MainWindow", "Run Tests"))
        self.solutionTitle.setText(_translate("MainWindow", "AuthorName - solutionFileName.go"))
        self.codeBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.solutionOutput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.menuFile.setTitle(_translate("MainWindow", "Menu"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionAdd_Task.setText(_translate("MainWindow", "Add Task"))
        self.actionAdd_Solution.setText(_translate("MainWindow", "Add Solution"))
        self.actionAdd_Tests.setText(_translate("MainWindow", "Add Tests"))
        self.actionLanguage_detection_On.setText(_translate("MainWindow", "Language detection: On"))
        self.actionSetting.setText(_translate("MainWindow", "Setting"))
        self.actionDetect_language.setText(_translate("MainWindow", "Detect language: On"))