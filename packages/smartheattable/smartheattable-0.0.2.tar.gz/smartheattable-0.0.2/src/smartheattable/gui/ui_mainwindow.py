# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(538, 723)
        font = QFont()
        font.setBold(True)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gbRun = QGroupBox(self.centralwidget)
        self.gbRun.setObjectName(u"gbRun")
        self.horizontalLayout = QHBoxLayout(self.gbRun)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnCalculate = QPushButton(self.gbRun)
        self.btnCalculate.setObjectName(u"btnCalculate")

        self.horizontalLayout.addWidget(self.btnCalculate)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnShutdown = QPushButton(self.gbRun)
        self.btnShutdown.setObjectName(u"btnShutdown")

        self.horizontalLayout.addWidget(self.btnShutdown)


        self.verticalLayout.addWidget(self.gbRun)

        self.gbTable = QGroupBox(self.centralwidget)
        self.gbTable.setObjectName(u"gbTable")
        self.horizontalLayout_2 = QHBoxLayout(self.gbTable)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnTableList = QPushButton(self.gbTable)
        self.btnTableList.setObjectName(u"btnTableList")

        self.horizontalLayout_2.addWidget(self.btnTableList)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.comboTable = QComboBox(self.gbTable)
        self.comboTable.addItem("")
        self.comboTable.addItem("")
        self.comboTable.setObjectName(u"comboTable")

        self.horizontalLayout_2.addWidget(self.comboTable)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.btnTableReboot = QPushButton(self.gbTable)
        self.btnTableReboot.setObjectName(u"btnTableReboot")

        self.horizontalLayout_2.addWidget(self.btnTableReboot)


        self.verticalLayout.addWidget(self.gbTable)

        self.gbScenario = QGroupBox(self.centralwidget)
        self.gbScenario.setObjectName(u"gbScenario")
        self.horizontalLayout_3 = QHBoxLayout(self.gbScenario)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btnScenList = QPushButton(self.gbScenario)
        self.btnScenList.setObjectName(u"btnScenList")

        self.horizontalLayout_3.addWidget(self.btnScenList)

        self.btnScenReload = QPushButton(self.gbScenario)
        self.btnScenReload.setObjectName(u"btnScenReload")

        self.horizontalLayout_3.addWidget(self.btnScenReload)

        self.btnScenPrint = QPushButton(self.gbScenario)
        self.btnScenPrint.setObjectName(u"btnScenPrint")

        self.horizontalLayout_3.addWidget(self.btnScenPrint)

        self.btnSetStatic = QPushButton(self.gbScenario)
        self.btnSetStatic.setObjectName(u"btnSetStatic")

        self.horizontalLayout_3.addWidget(self.btnSetStatic)

        self.btnSetDynamic = QPushButton(self.gbScenario)
        self.btnSetDynamic.setObjectName(u"btnSetDynamic")

        self.horizontalLayout_3.addWidget(self.btnSetDynamic)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addWidget(self.gbScenario)

        self.gbMode = QGroupBox(self.centralwidget)
        self.gbMode.setObjectName(u"gbMode")
        self.horizontalLayout_4 = QHBoxLayout(self.gbMode)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.rbLOPF = QRadioButton(self.gbMode)
        self.rbLOPF.setObjectName(u"rbLOPF")

        self.horizontalLayout_4.addWidget(self.rbLOPF)

        self.rbLPF = QRadioButton(self.gbMode)
        self.rbLPF.setObjectName(u"rbLPF")

        self.horizontalLayout_4.addWidget(self.rbLPF)

        self.rbPF = QRadioButton(self.gbMode)
        self.rbPF.setObjectName(u"rbPF")

        self.horizontalLayout_4.addWidget(self.rbPF)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addWidget(self.gbMode)

        self.gbDevices = QGroupBox(self.centralwidget)
        self.gbDevices.setObjectName(u"gbDevices")
        self.horizontalLayout_5 = QHBoxLayout(self.gbDevices)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btnListDevices = QPushButton(self.gbDevices)
        self.btnListDevices.setObjectName(u"btnListDevices")

        self.horizontalLayout_5.addWidget(self.btnListDevices)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addWidget(self.gbDevices)

        self.gbInfo = QGroupBox(self.centralwidget)
        self.gbInfo.setObjectName(u"gbInfo")
        self.horizontalLayout_6 = QHBoxLayout(self.gbInfo)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.plainTextEdit = QPlainTextEdit(self.gbInfo)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(500, 300))

        self.horizontalLayout_6.addWidget(self.plainTextEdit)


        self.verticalLayout.addWidget(self.gbInfo)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 538, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.gbRun.setTitle(QCoreApplication.translate("MainWindow", u"Run", None))
        self.btnCalculate.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
        self.btnShutdown.setText(QCoreApplication.translate("MainWindow", u"Shutdown", None))
        self.gbTable.setTitle(QCoreApplication.translate("MainWindow", u"Table", None))
        self.btnTableList.setText(QCoreApplication.translate("MainWindow", u"List", None))
        self.comboTable.setItemText(0, QCoreApplication.translate("MainWindow", u"All", None))
        self.comboTable.setItemText(1, QCoreApplication.translate("MainWindow", u"0", None))

        self.btnTableReboot.setText(QCoreApplication.translate("MainWindow", u"Reboot", None))
        self.gbScenario.setTitle(QCoreApplication.translate("MainWindow", u"Scenario", None))
        self.btnScenList.setText(QCoreApplication.translate("MainWindow", u"List", None))
        self.btnScenReload.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.btnScenPrint.setText(QCoreApplication.translate("MainWindow", u"Print current", None))
        self.btnSetStatic.setText(QCoreApplication.translate("MainWindow", u"Set static", None))
        self.btnSetDynamic.setText(QCoreApplication.translate("MainWindow", u"Set dynamic", None))
        self.gbMode.setTitle(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.rbLOPF.setText(QCoreApplication.translate("MainWindow", u"LOPF", None))
        self.rbLPF.setText(QCoreApplication.translate("MainWindow", u"LPF", None))
        self.rbPF.setText(QCoreApplication.translate("MainWindow", u"PF", None))
        self.gbDevices.setTitle(QCoreApplication.translate("MainWindow", u"Devices", None))
        self.btnListDevices.setText(QCoreApplication.translate("MainWindow", u"List RFID devices", None))
        self.gbInfo.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"calculate                      -> PyPSA simulation refresh\n"
"shutdown                    -> Shutdown of this program and disconnect all table sections\n"
"table \n"
"    list                             -> Print all table sections\n"
"   reboot all                  -> Reboot all table sections\n"
"   reboot [SECTION]   -> reboots given table section\n"
"scenario \n"
"    reload                        -> Find and load all scenarios in Static/\n"
"    list                              -> Print all available scenarios\n"
"    current                     -> Print all current scenario\n"
"    set -s [NAME]          -> Switches to given static scenario\n"
"    set -d [NAME]         -> Switches to given dynamic scenario (not yet implemented!)\n"
"mode \n"
"    set lopf                     -> Set calculation type to Linear Optimal Power Flow (LOPF)\n"
"    set lpf                       -> Set calculation type to Linear Power Flow (LPF)\n"
"    set pf                        -> Set calculation type to Power Flow (PF)\n"
""
                        "devices \n"
"    list                              -> Print the number of modules placed on each table\n"
"", None))
    # retranslateUi

