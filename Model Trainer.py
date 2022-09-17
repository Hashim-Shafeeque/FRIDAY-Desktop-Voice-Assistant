# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FridayGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import random


# noinspection PyShadowingNames,PyAttributeOutsideInit,PyUnresolvedReferences
class Ui_FridayGUI(object):
    def setupUi(self, FridayGUI):
        FridayGUI.setObjectName("FridayGUI")
        FridayGUI.resize(4096, 2160)
        self.centralwidget = QtWidgets.QWidget(FridayGUI)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1600, 1000, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("alternate-background-color: rgb(255, 255, 0);background:transparent;\n"
"border-radius:none;\n"
"color: rgb(124, 124, 124);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1730, 1000, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("alternate-background-color: rgb(255, 255, 127);\n"
"background:transparent;\n"
"border-radius:none;\n"
"color: rgb(170, 0, 0);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.label.setText("")
        self.movie_set = ["C:/FRIDAY/files/icons/STARTING_3.gif",
                          "C:/FRIDAY/files/icons/STARTING_1.gif",
                          "C:/FRIDAY/files/icons/STARTING_4.gif",
                          "C:/FRIDAY/files/icons/STARTING_2.gif"]
        self.movie_selected = random.choice(self.movie_set)
        self.movie_ = QtGui.QMovie(self.movie_selected)
        self.label.setMovie(self.movie_)
        self.movie_.start()
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(1650, 840, 481, 101))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser.setFont(font)
        self.textBrowser.setStyleSheet("background:transparent;\n"
                                       "border-radius:none;\n"
                                       "color:red;\n"
                                       "font-size:50px;")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(1650, 910, 481, 101))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:grey;\n"
                                         "font-size:50px;")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(20, 50, 251, 101))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(48)
        font.setBold(False)
        self.textBrowser_3.setFont(font)
        self.textBrowser_3.setAutoFillBackground(False)
        self.textBrowser_3.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:#8a0000;\n"
                                         "font-size:64px;")
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(20, 110, 311, 41))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(24)
        font.setBold(False)
        self.textBrowser_4.setFont(font)
        self.textBrowser_4.setAutoFillBackground(False)
        self.textBrowser_4.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:grey;\n"
                                         "font-size:32px;")
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 180, 331, 891))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap())
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_5.setGeometry(QtCore.QRect(30, 240, 261, 351))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_5.setFont(font)
        self.textBrowser_5.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:red;\n"
                                         "font-size:30px;")
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_6.setGeometry(QtCore.QRect(30, 620, 261, 41))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(24)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.textBrowser_6.setFont(font)
        self.textBrowser_6.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:silver;\n"
                                         "font-size:30px;")
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_7.setGeometry(QtCore.QRect(30, 680, 261, 351))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_7.setFont(font)
        self.textBrowser_7.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:grey;\n"
                                         "font-size:30px;")
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1360, 50, 551, 301))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap())
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(550, 930, 761, 131))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap())
        self.label_4.setScaledContents(False)
        self.label_4.setObjectName("label_4")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1981, 51))
        self.frame.setMouseTracking(False)
        self.frame.setStyleSheet("background-color: rgb(9, 5, 13);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_close = QtWidgets.QPushButton(self.frame)
        self.pushButton_close.setGeometry(QtCore.QRect(1880, 0, 21, 23))
        self.pushButton_close.setStyleSheet(" background:transparent;\n"
"border-radius:none;")
        self.pushButton_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("files/icons/x.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_close.setIcon(icon)
        self.pushButton_close.setObjectName("pushButton_close")
        # self.pushButton_maximize = QtWidgets.QPushButton(self.frame)
        # self.pushButton_maximize.setGeometry(QtCore.QRect(1830, 0, 21, 23))
        # self.pushButton_maximize.setStyleSheet(" background:transparent;\n"
# "border-radius:none;")
        # self.pushButton_maximize.setText("")
        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap("files/icons/maximize-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pushButton_maximize.setIcon(icon1)
        # self.pushButton_maximize.setObjectName("pushButton_maximize")
        self.pushButton_minimize_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_minimize_2.setGeometry(QtCore.QRect(1830, 0, 21, 23))
        self.pushButton_minimize_2.setStyleSheet(" background:transparent;\n"
"border-radius:none;")
        self.pushButton_minimize_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("files/icons/arrow-down-left.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_minimize_2.setIcon(icon2)
        self.pushButton_minimize_2.setObjectName("pushButton_minimize_2")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(0, -10, 1991, 33))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("files/icons/title_bar.png"))
        self.label_5.setScaledContents(False)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 5, 61, 34))
        self.label_6.setStyleSheet("background:transparent;\n"
"border-radius:none;")
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("files/icons/friday.ico"))
        self.label_6.setScaledContents(False)
        self.label_6.setObjectName("label_6")
        self.label_5.raise_()
        self.pushButton_close.raise_()
        # self.pushButton_maximize.raise_()
        self.pushButton_minimize_2.raise_()
        self.label_6.raise_()
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1740, 150, 131, 121))
        self.label_7.setStyleSheet("background:transparent;\n"
                                   "border-radius:none;")
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap())
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.textBrowser_8 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_8.setGeometry(QtCore.QRect(1400, 90, 481, 51))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_8.setFont(font)
        self.textBrowser_8.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:silver;\n"
                                         "font-size:30px;")
        self.textBrowser_8.setObjectName("textBrowser_8")
        self.textBrowser_9 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_9.setGeometry(QtCore.QRect(1520, 150, 141, 111))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(75)
        self.textBrowser_9.setFont(font)
        self.textBrowser_9.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:maroon;\n"
                                         "font-size:70px;")
        self.textBrowser_9.setObjectName("textBrowser_9")
        self.textBrowser_10 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_10.setGeometry(QtCore.QRect(1400, 270, 301, 51))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_10.setFont(font)
        self.textBrowser_10.setStyleSheet("background:transparent;\n"
                                         "border-radius:none;\n"
                                         "color:grey;\n"
                                         "font-size:30px;")
        self.textBrowser_10.setObjectName("textBrowser_10")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(1380, 660, 501, 81))
        font = QtGui.QFont()
        font.setFamily("DS-Digital")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1350, 640, 581, 121))
        self.label_8.setStyleSheet("background:transparent;\n"
                                   "border-radius:none;")
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("files/icons/DIALOGUE_BOX.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(370, 40, 311, 111))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(680, 40, 311, 111))
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(990, 40, 311, 111))
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.lineEdit.raise_()
        self.label.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.textBrowser.raise_()
        self.textBrowser_2.raise_()
        self.textBrowser_3.raise_()
        self.textBrowser_4.raise_()
        self.label_2.raise_()
        self.textBrowser_5.raise_()
        self.textBrowser_6.raise_()
        self.textBrowser_7.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.frame.raise_()
        self.label_7.raise_()
        self.textBrowser_8.raise_()
        self.textBrowser_9.raise_()
        self.textBrowser_10.raise_()
        FridayGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(FridayGUI)
        QtCore.QMetaObject.connectSlotsByName(FridayGUI)

    def retranslateUi(self, FridayGUI):
        _translate = QtCore.QCoreApplication.translate
        FridayGUI.setWindowTitle(_translate("FridayGUI", "FRIDAY Desktop Voice Assistant"))
        FridayGUI.setWindowIcon("files/icons/Friday_icon_file")
        self.pushButton.setText(_translate("FridayGUI", "RUN"))
        self.pushButton_2.setText(_translate("FridayGUI", "TERMINATE"))
        self.textBrowser_3.setHtml(_translate("FridayGUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DS-Digital\'; font-size:24pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textBrowser_4.setHtml(_translate("FridayGUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DS-Digital\'; font-size:24pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textBrowser_5.setHtml(_translate("FridayGUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DS-Digital\'; font-size:24pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textBrowser_6.setHtml(_translate("FridayGUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DS-Digital\'; font-size:24pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textBrowser_7.setHtml(_translate("FridayGUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DS-Digital\'; font-size:24pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FridayGUI = QtWidgets.QMainWindow()
    ui = Ui_FridayGUI()
    ui.setupUi(FridayGUI)
    FridayGUI.show()
    sys.exit(app.exec_())
