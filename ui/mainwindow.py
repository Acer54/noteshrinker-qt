# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow_noteshrinker_qt(object):
    def setupUi(self, MainWindow_noteshrinker_qt):
        MainWindow_noteshrinker_qt.setObjectName(_fromUtf8("MainWindow_noteshrinker_qt"))
        MainWindow_noteshrinker_qt.resize(1070, 794)
        MainWindow_noteshrinker_qt.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow_noteshrinker_qt.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(MainWindow_noteshrinker_qt)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tV_Fileview = QtGui.QTreeView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tV_Fileview.sizePolicy().hasHeightForWidth())
        self.tV_Fileview.setSizePolicy(sizePolicy)
        self.tV_Fileview.setObjectName(_fromUtf8("tV_Fileview"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.tW_workbench = Workbench_Tablewidget(self.layoutWidget)
        self.tW_workbench.setMinimumSize(QtCore.QSize(460, 0))
        self.tW_workbench.setObjectName(_fromUtf8("tW_workbench"))
        self.tW_workbench.setColumnCount(0)
        self.tW_workbench.setRowCount(0)
        self.verticalLayout_9.addWidget(self.tW_workbench)
        self.gB_preview = QtGui.QGroupBox(self.layoutWidget)
        self.gB_preview.setObjectName(_fromUtf8("gB_preview"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.gB_preview)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.lbl_preview = QtGui.QLabel(self.gB_preview)
        self.lbl_preview.setObjectName(_fromUtf8("lbl_preview"))
        self.horizontalLayout_11.addWidget(self.lbl_preview)
        self.verticalLayout_9.addWidget(self.gB_preview)
        self.horizontalLayout_13.addLayout(self.verticalLayout_9)
        self.gB_settings = QtGui.QGroupBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gB_settings.sizePolicy().hasHeightForWidth())
        self.gB_settings.setSizePolicy(sizePolicy)
        self.gB_settings.setMinimumSize(QtCore.QSize(320, 0))
        self.gB_settings.setMaximumSize(QtCore.QSize(360, 16777215))
        self.gB_settings.setObjectName(_fromUtf8("gB_settings"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.gB_settings)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 30, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cB_create_images = QtGui.QCheckBox(self.gB_settings)
        self.cB_create_images.setObjectName(_fromUtf8("cB_create_images"))
        self.verticalLayout.addWidget(self.cB_create_images)
        self.cB_create_merged_pdf = QtGui.QCheckBox(self.gB_settings)
        self.cB_create_merged_pdf.setObjectName(_fromUtf8("cB_create_merged_pdf"))
        self.verticalLayout.addWidget(self.cB_create_merged_pdf)
        self.cB_create_single_pdf = QtGui.QCheckBox(self.gB_settings)
        self.cB_create_single_pdf.setObjectName(_fromUtf8("cB_create_single_pdf"))
        self.verticalLayout.addWidget(self.cB_create_single_pdf)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.pB_go = QtGui.QPushButton(self.gB_settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_go.sizePolicy().hasHeightForWidth())
        self.pB_go.setSizePolicy(sizePolicy)
        self.pB_go.setObjectName(_fromUtf8("pB_go"))
        self.horizontalLayout.addWidget(self.pB_go)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_10.addItem(spacerItem)
        self.line = QtGui.QFrame(self.gB_settings)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_10.addWidget(self.line)
        self.gB_settings_details = QtGui.QGroupBox(self.gB_settings)
        self.gB_settings_details.setTitle(_fromUtf8(""))
        self.gB_settings_details.setObjectName(_fromUtf8("gB_settings_details"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.gB_settings_details)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.gB_settings_details)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.lE_filename_base = QtGui.QLineEdit(self.gB_settings_details)
        self.lE_filename_base.setText(_fromUtf8(""))
        self.lE_filename_base.setObjectName(_fromUtf8("lE_filename_base"))
        self.verticalLayout_2.addWidget(self.lE_filename_base)
        self.verticalLayout_7.addLayout(self.verticalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.gB_settings_details)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.lcdNumber = QtGui.QLCDNumber(self.gB_settings_details)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.horizontalLayout_7.addWidget(self.lcdNumber)
        self.hS_resulting_colors = QtGui.QSlider(self.gB_settings_details)
        self.hS_resulting_colors.setOrientation(QtCore.Qt.Horizontal)
        self.hS_resulting_colors.setObjectName(_fromUtf8("hS_resulting_colors"))
        self.horizontalLayout_7.addWidget(self.hS_resulting_colors)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        spacerItem4 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem4)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.gB_settings_details)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.lcdNumber_2 = QtGui.QLCDNumber(self.gB_settings_details)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.horizontalLayout_8.addWidget(self.lcdNumber_2)
        self.hS_percentage_of_pixels = QtGui.QSlider(self.gB_settings_details)
        self.hS_percentage_of_pixels.setOrientation(QtCore.Qt.Horizontal)
        self.hS_percentage_of_pixels.setObjectName(_fromUtf8("hS_percentage_of_pixels"))
        self.horizontalLayout_8.addWidget(self.hS_percentage_of_pixels)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.verticalLayout_7.addLayout(self.verticalLayout_4)
        spacerItem6 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem6)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.gB_settings_details)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.lcdNumber_3 = QtGui.QLCDNumber(self.gB_settings_details)
        self.lcdNumber_3.setObjectName(_fromUtf8("lcdNumber_3"))
        self.horizontalLayout_9.addWidget(self.lcdNumber_3)
        self.hS_background_saturation = QtGui.QSlider(self.gB_settings_details)
        self.hS_background_saturation.setOrientation(QtCore.Qt.Horizontal)
        self.hS_background_saturation.setObjectName(_fromUtf8("hS_background_saturation"))
        self.horizontalLayout_9.addWidget(self.hS_background_saturation)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)
        spacerItem8 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem8)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_5 = QtGui.QLabel(self.gB_settings_details)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.lcdNumber_4 = QtGui.QLCDNumber(self.gB_settings_details)
        self.lcdNumber_4.setObjectName(_fromUtf8("lcdNumber_4"))
        self.horizontalLayout_10.addWidget(self.lcdNumber_4)
        self.hS_background_threshold = QtGui.QSlider(self.gB_settings_details)
        self.hS_background_threshold.setOrientation(QtCore.Qt.Horizontal)
        self.hS_background_threshold.setObjectName(_fromUtf8("hS_background_threshold"))
        self.horizontalLayout_10.addWidget(self.hS_background_threshold)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        spacerItem10 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem10)
        self.pB_reset_to_default = QtGui.QPushButton(self.gB_settings_details)
        self.pB_reset_to_default.setObjectName(_fromUtf8("pB_reset_to_default"))
        self.verticalLayout_7.addWidget(self.pB_reset_to_default)
        spacerItem11 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem11)
        self.pB_apply_to_all = QtGui.QPushButton(self.gB_settings_details)
        self.pB_apply_to_all.setObjectName(_fromUtf8("pB_apply_to_all"))
        self.verticalLayout_7.addWidget(self.pB_apply_to_all)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.verticalLayout_10.addWidget(self.gB_settings_details)
        self.horizontalLayout_12.addLayout(self.verticalLayout_10)
        self.horizontalLayout_13.addWidget(self.gB_settings)
        self.horizontalLayout_14.addWidget(self.splitter)
        MainWindow_noteshrinker_qt.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow_noteshrinker_qt)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1070, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow_noteshrinker_qt.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow_noteshrinker_qt)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow_noteshrinker_qt.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_noteshrinker_qt)
        QtCore.QObject.connect(self.hS_resulting_colors, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber.display)
        QtCore.QObject.connect(self.hS_percentage_of_pixels, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber_2.display)
        QtCore.QObject.connect(self.hS_background_saturation, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber_3.display)
        QtCore.QObject.connect(self.hS_background_threshold, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber_4.display)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_noteshrinker_qt)
        MainWindow_noteshrinker_qt.setTabOrder(self.cB_create_images, self.cB_create_merged_pdf)
        MainWindow_noteshrinker_qt.setTabOrder(self.cB_create_merged_pdf, self.cB_create_single_pdf)
        MainWindow_noteshrinker_qt.setTabOrder(self.cB_create_single_pdf, self.pB_go)
        MainWindow_noteshrinker_qt.setTabOrder(self.pB_go, self.tW_workbench)
        MainWindow_noteshrinker_qt.setTabOrder(self.tW_workbench, self.tV_Fileview)

    def retranslateUi(self, MainWindow_noteshrinker_qt):
        MainWindow_noteshrinker_qt.setWindowTitle(_translate("MainWindow_noteshrinker_qt", "NoteShrinker Qt", None))
        self.gB_preview.setTitle(_translate("MainWindow_noteshrinker_qt", "Preview:", None))
        self.lbl_preview.setText(_translate("MainWindow_noteshrinker_qt", "Preview...", None))
        self.gB_settings.setTitle(_translate("MainWindow_noteshrinker_qt", "Settings:", None))
        self.cB_create_images.setText(_translate("MainWindow_noteshrinker_qt", "create Images", None))
        self.cB_create_merged_pdf.setText(_translate("MainWindow_noteshrinker_qt", "create merged PDF", None))
        self.cB_create_single_pdf.setText(_translate("MainWindow_noteshrinker_qt", "create single PDFs", None))
        self.pB_go.setText(_translate("MainWindow_noteshrinker_qt", "Go!", None))
        self.label.setText(_translate("MainWindow_noteshrinker_qt", "Filename-Extention:", None))
        self.label_2.setText(_translate("MainWindow_noteshrinker_qt", "Resulting Colors:", None))
        self.label_3.setText(_translate("MainWindow_noteshrinker_qt", "% of pixels to sample:", None))
        self.label_4.setText(_translate("MainWindow_noteshrinker_qt", "Background saturation:", None))
        self.label_5.setText(_translate("MainWindow_noteshrinker_qt", "Background value threshold %:", None))
        self.pB_reset_to_default.setText(_translate("MainWindow_noteshrinker_qt", "Reset to default", None))
        self.pB_apply_to_all.setText(_translate("MainWindow_noteshrinker_qt", "Apply Settings to all Images", None))

from lib.Workbench import Workbench_Tablewidget
