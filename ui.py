# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'anime2x.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLabel,
    QLineEdit, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QTextBrowser, QToolButton, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(671, 562)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Files = QGroupBox(self.centralwidget)
        self.Files.setObjectName(u"Files")
        self.Files.setGeometry(QRect(20, 130, 631, 81))
        self.OutputPath = QLabel(self.Files)
        self.OutputPath.setObjectName(u"OutputPath")
        self.OutputPath.setGeometry(QRect(20, 50, 71, 16))
        self.InputEdit = QLineEdit(self.Files)
        self.InputEdit.setObjectName(u"InputEdit")
        self.InputEdit.setGeometry(QRect(110, 20, 451, 20))
        self.OutputEdit = QLineEdit(self.Files)
        self.OutputEdit.setObjectName(u"OutputEdit")
        self.OutputEdit.setGeometry(QRect(110, 50, 451, 20))
        self.InputPath = QLabel(self.Files)
        self.InputPath.setObjectName(u"InputPath")
        self.InputPath.setGeometry(QRect(20, 20, 71, 16))
        self.InputButton = QToolButton(self.Files)
        self.InputButton.setObjectName(u"InputButton")
        self.InputButton.setGeometry(QRect(570, 20, 41, 21))
        self.OutputButton = QToolButton(self.Files)
        self.OutputButton.setObjectName(u"OutputButton")
        self.OutputButton.setGeometry(QRect(570, 50, 41, 21))
        self.Configs = QGroupBox(self.centralwidget)
        self.Configs.setObjectName(u"Configs")
        self.Configs.setGeometry(QRect(20, 220, 321, 221))
        self.Interpolation = QGroupBox(self.Configs)
        self.Interpolation.setObjectName(u"Interpolation")
        self.Interpolation.setGeometry(QRect(10, 20, 301, 91))
        self.inter_ratio4 = QRadioButton(self.Interpolation)
        self.inter_ratio4.setObjectName(u"inter_ratio4")
        self.inter_ratio4.setGeometry(QRect(20, 60, 261, 16))
        self.inter_ratio1 = QRadioButton(self.Interpolation)
        self.inter_ratio1.setObjectName(u"inter_ratio1")
        self.inter_ratio1.setGeometry(QRect(20, 20, 261, 16))
        self.inter_ratio1.setChecked(False)
        self.inter_ratio2 = QRadioButton(self.Interpolation)
        self.inter_ratio2.setObjectName(u"inter_ratio2")
        self.inter_ratio2.setGeometry(QRect(20, 40, 271, 16))
        self.inter_ratio2.setChecked(True)
        self.Upscaling = QGroupBox(self.Configs)
        self.Upscaling.setObjectName(u"Upscaling")
        self.Upscaling.setGeometry(QRect(10, 120, 301, 91))
        self.up_ratio2 = QRadioButton(self.Upscaling)
        self.up_ratio2.setObjectName(u"up_ratio2")
        self.up_ratio2.setGeometry(QRect(20, 40, 261, 16))
        self.up_ratio2.setChecked(True)
        self.up_ratio4 = QRadioButton(self.Upscaling)
        self.up_ratio4.setObjectName(u"up_ratio4")
        self.up_ratio4.setGeometry(QRect(20, 60, 271, 16))
        self.up_ratio1 = QRadioButton(self.Upscaling)
        self.up_ratio1.setObjectName(u"up_ratio1")
        self.up_ratio1.setGeometry(QRect(20, 20, 261, 16))
        self.up_ratio1.setChecked(False)
        self.Introduction = QGroupBox(self.centralwidget)
        self.Introduction.setObjectName(u"Introduction")
        self.Introduction.setGeometry(QRect(20, 10, 631, 111))
        self.description = QLabel(self.Introduction)
        self.description.setObjectName(u"description")
        self.description.setGeometry(QRect(20, 10, 601, 91))
        self.description.setTextFormat(Qt.AutoText)
        self.description.setScaledContents(False)
        self.description.setWordWrap(True)
        self.description.setOpenExternalLinks(True)
        self.Actions = QGroupBox(self.centralwidget)
        self.Actions.setObjectName(u"Actions")
        self.Actions.setGeometry(QRect(20, 450, 321, 91))
        self.Generate = QPushButton(self.Actions)
        self.Generate.setObjectName(u"Generate")
        self.Generate.setGeometry(QRect(20, 50, 75, 23))
        self.Cancel = QPushButton(self.Actions)
        self.Cancel.setObjectName(u"Cancel")
        self.Cancel.setGeometry(QRect(110, 50, 75, 23))
        self.OpenImage = QCheckBox(self.Actions)
        self.OpenImage.setObjectName(u"OpenImage")
        self.OpenImage.setGeometry(QRect(20, 20, 251, 16))
        self.OpenImage.setChecked(True)
        self.About = QPushButton(self.Actions)
        self.About.setObjectName(u"About")
        self.About.setGeometry(QRect(200, 50, 75, 23))
        self.Logs = QGroupBox(self.centralwidget)
        self.Logs.setObjectName(u"Logs")
        self.Logs.setGeometry(QRect(350, 220, 301, 321))
        self.textBrowser = QTextBrowser(self.Logs)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 20, 281, 291))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Anime2x - AI-powered Anime Video Enhancer", None))
        self.Files.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
        self.OutputPath.setText(QCoreApplication.translate("MainWindow", u"Output Path", None))
        self.OutputEdit.setText("")
        self.InputPath.setText(QCoreApplication.translate("MainWindow", u"Input Path(s)", None))
        self.InputButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.OutputButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.Configs.setTitle(QCoreApplication.translate("MainWindow", u"Configs", None))
        self.Interpolation.setTitle(QCoreApplication.translate("MainWindow", u"Interpolation", None))
        self.inter_ratio4.setText(QCoreApplication.translate("MainWindow", u"4x Frames (Very Long Time, Very Large File)", None))
        self.inter_ratio1.setText(QCoreApplication.translate("MainWindow", u"1x Frames (No Interpolation)", None))
        self.inter_ratio2.setText(QCoreApplication.translate("MainWindow", u"2x Frames", None))
        self.Upscaling.setTitle(QCoreApplication.translate("MainWindow", u"Upscaling", None))
        self.up_ratio2.setText(QCoreApplication.translate("MainWindow", u"2x Size", None))
        self.up_ratio4.setText(QCoreApplication.translate("MainWindow", u"4x Size  (Very Long Time, Very Large File)", None))
        self.up_ratio1.setText(QCoreApplication.translate("MainWindow", u"1x Size (No Upscaling)", None))
        self.Introduction.setTitle(QCoreApplication.translate("MainWindow", u"Introduction", None))
        self.description.setText(QCoreApplication.translate("MainWindow", u"This tool allows you to interpolate and upscale your anime video with high quality.\n"
"(1) Set your input path and output path in Files Panel. \n"
"(2) Select your preferred parameters in Configs Panel. (Larger ratio NEEDS longer time and larger disk space.)\n"
"(3) Click generate in Action Panel and wait for several minutes to process. ", None))
        self.Actions.setTitle(QCoreApplication.translate("MainWindow", u"Actions", None))
        self.Generate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.Cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.OpenImage.setText(QCoreApplication.translate("MainWindow", u"Open Output Directory After Generation", None))
        self.About.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.Logs.setTitle(QCoreApplication.translate("MainWindow", u"Logs", None))
    # retranslateUi

