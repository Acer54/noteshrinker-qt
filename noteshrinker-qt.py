#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################################################################
# Description:
# noteshrinker-qt is a multilingual GUI for the commandline program "noteshrink" (https://github.com/mzucker/noteshrink)
# which was initially created from Matt Zucker(https://github.com/mzucker).
# It supports adding, organizing and trimming possible arguments. It supplies previews and lets the user define
# the output-formats.
# It is cross-platform compatible and able to run with Python >= 2.7 and Qt >= 4.
#
#
# License:
#    MIT License
#    Copyright (c) 2016 Laumer Matthias
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#######################################################################################################################


import sys, os, logging, logging.handlers, io, argparse, time, signal
import res.res
from ui.mainwindow import Ui_MainWindow_noteshrinker_qt
from lib.FileSystemView import LM_QFileSystemModel, FileIconProvider
from PyQt4.QtCore import *  #TODO: Add Pyqt5 Support
from PyQt4.QtGui import *


__author__ = 'matthias laumer, matthias.laumer@web.de'
__title__='noteshrinker_qt'
__version__ = "0.0.1"

logger = logging.getLogger(__title__)
log_capture_string = io.StringIO()  # variable holds the complete log in realtime
LOG_FILENAME = __title__ + '.log'
cwd = os.path.dirname(os.path.realpath(__file__))      # gives the path, where the script is located

_ = lambda x : x


def setupLogger(console=True, File=False, Variable=False, Filebackupcount=0):
    '''
    Setup a logger for the application
    :return: Nothing
    '''
    global logger
    global log_capture_string
    # create logger
    logging.raiseExceptions = False
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Check if log exists and should therefore be rolled
    needRoll = os.path.isfile(LOG_FILENAME)

    if File:
        # create file handler which logs even debug messages and hold a backup of old logs
        fh = logging.handlers.RotatingFileHandler( LOG_FILENAME, backupCount=int(Filebackupcount)) # create a backup of the log
        fh.setLevel(logging.DEBUG) if args.get("debug") else fh.setLevel(logging.INFO)  #TODO:Change this to ERROR after dev
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if Variable:
        # create variable handler for on the fly read (e.g. for a log-interface)
        vh = logging.StreamHandler(log_capture_string)
        vh.setLevel(logging.DEBUG) if args.get("debug") else vh.setLevel(logging.INFO)
        vh.setFormatter(formatter)
        logger.addHandler(vh)
    if console:
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG) if args.get("debug") else ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # This is a stale log, so roll it
    if File and needRoll:
        # Add timestamp
        logger.debug(_('\n---------\nLog closed on {0}.\n---------\n').format(time.asctime()))
        # Roll over on application start
        logger.handlers[0].doRollover()
    # Add timestamp
    logger.debug(_('\n---------\nLog started on {0}.\n---------\n').format(time.asctime()))


def sigint_handler(*args):
    '''
    This handler is called whenever Python receives a "sigint" signal (CTRL+C)
    :param args: NOT IN USE
    :return: Nothong, Exits the programm with exit-code 0 (success)
    '''

    logger.debug(_("SigTerm received... savely shut down now."))
    time.sleep(1)
    logger.debug(_("Final Actions successfully performed."))
    sys.exit(0)


def excepthook(excType, excValue, traceback):
    '''
    This handler is called whenever an unexpected failure occurs
    (Uncaught Exception). The Exception is written to the log file for later use
    '''
    global logger
    logger.error("Uncaught exception",
                 exc_info=(excType, excValue, traceback))


class MainWindow(QMainWindow, Ui_MainWindow_noteshrinker_qt):
    '''
    All the visible aspects which have to be handled are in this class.
    '''
    sig_setProgressValue = pyqtSignal(int)

    def __init__(self, parent=None):
        '''
        :param parent: Usually None. (Because Mainwindow is normaly no Child of anything.)
        Initial tasks
        - setup Ui
        - create necessary Actions, Menus, Toolbars, setup Connections.
        '''

        super(MainWindow, self).__init__(parent)

        self.setupUi(self)  #TODO: Load UI File directelly after dev
        self.setWindowIcon(self.generateIcon())
        self.setupUi_Widgets()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createConnections()
        self.checkActions()
        self.__moveCenter()

        QTimer.singleShot(1, lambda: self.sig_setProgressValue.emit(0))

    ##################################################################################################STARTUP Actions:

    def generateIcon(self):
        '''
        see http://www.thankcoder.com/questions/jyzag/window-icon-does-not-show
        :return: QIcon with different sizes (used as an application icon)
        '''
        app_icon = QIcon()
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '16x16.png'), QSize(16, 16))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '22x22.png'), QSize(22, 22))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '24x24.png'), QSize(24, 24))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '32x32.png'), QSize(32, 32))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '48x48.png'), QSize(48, 48))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '64x64.png'), QSize(64, 64))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '96x96.png'), QSize(96, 96))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '128x128.png'), QSize(128, 128))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '192x192.png'), QSize(192, 192))
        app_icon.addFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res', '256x256.png'), QSize(256, 256))

        return app_icon

    def setupUi_Widgets(self):
        """
        Setup the Mainwindow. Make initial settings.
        """
        #TODO: Load the last import location from system-settings
        self.progressBar = QProgressBar(visible=False)
        self.statusbar.addPermanentWidget(self.progressBar)
        #self.progressBar.setVisible(False)
        self.picturelocation = QDesktopServices.storageLocation(QDesktopServices.PicturesLocation)

        # Setup the TreeView (Fileviewer):
        self.tV_Fileview.setDragEnabled(True)
        #self.tV_Fileview.setDropIndicatorShown(True)
        self.tV_Fileview.setSelectionMode(QAbstractItemView.ExtendedSelection)  # ctrl or shift for multiselection
        self.model = LM_QFileSystemModel()   # lib/FileSystemView.py
        self.provider = FileIconProvider()   # special icon for images (see Filters)
        self.model.setIconProvider(self.provider)
        self.model.setRootPath(self.picturelocation)
        self.model.setFilter(QDir.NoDotAndDotDot|QDir.AllEntries|QDir.AllDirs)
        self.model.setNameFilters(['*.png', '*.jpg', '*.jpeg', '*.gif'])
        self.tV_Fileview.setModel(self.model)
        self.tV_Fileview.setCurrentIndex(self.model.index(self.picturelocation))
        for i in [1, 2, 3]:
            self.tV_Fileview.hideColumn(i)

        # Setup the Tablewidget:
        self.tW_workbench.setDropIndicatorShown(True)
        self.tW_workbench.setColumnCount(4)

        self.tW_workbench.setHorizontalHeaderLabels([self.tr('Preview'),
                                                     self.tr('Filename'),
                                                     self.tr('Size'), ''])

        self.tW_workbench.horizontalHeader().setResizeMode(0, 100)             # preview
        self.tW_workbench.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)             # filename
        self.tW_workbench.horizontalHeader().setResizeMode(2, QHeaderView.ResizeToContents)    # size
        self.tW_workbench.horizontalHeader().setResizeMode(3, QHeaderView.Fixed)    # Button
        self.tW_workbench.horizontalHeader().setDefaultSectionSize(100)
        self.tW_workbench.horizontalHeader().setStretchLastSection(False)


        self.tW_workbench.resizeRowsToContents()    # enlarge the hight of the row, according to the preview

    def createActions(self):
        """
        Create Actions which are used in Toolbar, Menue and context-menues
        """

        self.ACTexit = QAction(QIcon(':/exit.png'), self.tr(u"&Exit"),self,
                                 shortcut=QKeySequence.Quit,
                                 statusTip=self.tr(u"Exit the Application"),
                                 triggered=self.close)
        self.ACTexit.setIconVisibleInMenu(True)

        self.ACTremovePos = QAction(QIcon(':/remove_row.png'), self.tr(u"&Remove position(s)"),self,
                                 shortcut=QKeySequence.Delete,
                                 statusTip=self.tr(u"Removes the selected position(s)"),
                                 triggered=self.tW_workbench.removeMarked)
        self.ACTremovePos.setIconVisibleInMenu(True)

        self.ACTaddPos = QAction(QIcon(':/add_row.png'), self.tr(u"&Add position(s)"),self,
                                 statusTip=self.tr(u"Adds the selected position(s)"),
                                 triggered=self.on_addPos)
        self.ACTaddPos.setIconVisibleInMenu(True)

        self.ACTmoveUp = QAction(QIcon(':/moveUp.png'), self.tr(u"&Move Up"),self,
                                 statusTip=self.tr(u"Move the selected position UP"),
                                 triggered=self.tW_workbench.moveUp)
        self.ACTmoveUp.setIconVisibleInMenu(True)

        self.ACTmoveDown = QAction(QIcon(':/moveDown.png'), self.tr(u"&RMove Down"),self,
                                 statusTip=self.tr(u"Move the selected position DOWN"),
                                 triggered=self.tW_workbench.moveDown)
        self.ACTmoveDown.setIconVisibleInMenu(True)

    def createMenus(self):
        """
        Create the Mainwindow meneu   " Datei  |   Bearbeiten   |   Extras   |   Hilfe "
        :return:
        """
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.ACTexit)

        self.editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        self.editMenu.addAction(self.ACTaddPos)
        self.editMenu.addAction(self.ACTremovePos)
        self.editMenu.addAction(self.ACTmoveUp)
        self.editMenu.addAction(self.ACTmoveDown)

        self.extrasMenu = self.menuBar().addMenu(self.tr("&Extras"))

        self.menuBar().addSeparator()    # seems like there is no effect on Linux. (maybe on Windows..)

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))

    def createToolBars(self):
        """
        A single Toolbar is used.
        """
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.ACTaddPos)
        self.fileToolBar.addAction(self.ACTremovePos)
        self.fileToolBar.addAction(self.ACTmoveUp)
        self.fileToolBar.addAction(self.ACTmoveDown)
        self.spacer = QWidget()                          # add streching / invisible widget to separate following
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.fileToolBar.addWidget(self.spacer)
        self.fileToolBar.addAction(self.ACTexit)

    def createContextMenue(self, point):   # called with (table/tree)view.customContextMenuRequested
        """
        This function is a customContextMenue of the presentation Area, it will be called with a right-click on the
        presentationArea.
        :param point: Qpoint, where the action was triggered.
        :return: brings up a context-menue which is almost the same, than in toolbar and menuebar.
        """
        pass

    def checkActions(self):    # caller: "selectionChanged" of tree/table or "SIGNAL("checkActions()"
        """
        Is called with signal "selectionChanged" of tableView (selection Model)
        """
        #check remove Action (True if any index is selected)
        try:
            self.ACTremovePos.setEnabled(True \
                if len(self.tW_workbench.selectionModel().selectedRows()) > 0 \
                                         else False)
        except IndexError:
            self.ACTremovePos.setEnabled(False)

        #check add Action (True if any index is selected)
        try:
            self.ACTaddPos.setEnabled(True \
                if len(self.tv_selectedFiles()) > 0 \
                                         else False)
        except IndexError:
            self.ACTaddPos.setEnabled(False)

        #check "Move Up / Move Down" only active it exactelly 1 is selected
        try:
            self.ACTmoveDown.setEnabled(True \
                if len(self.tW_workbench.selectionModel().selectedRows()) >= 1 \
                                         else False)
            self.ACTmoveUp.setEnabled(True \
                if len(self.tW_workbench.selectionModel().selectedRows()) >= 1 \
                                         else False)
        except IndexError:
            self.ACTmoveDown.setEnabled(False)
            self.ACTmoveUp.setEnabled(False)

        pass

    def __moveCenter(self):
        """
        Placing the windows in the middle of the screen
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def createConnections(self):
        """
        Create permanent Connections. Other necessary connections are created dynamically in my engine
        """
        self.tW_workbench.itemSelectionChanged.connect(self.checkActions)   # Enable / Disable the button depending on selection
        self.tW_workbench.sig_setProgressValue.connect(self.setProgressValue)   # Enable / Disable the button depending on selectionevent.accept()
        self.tW_workbench.sig_filesAccepted.connect(self.tV_Fileview.clearSelection)   # Clear selection in tv after drop
        self.tV_Fileview.selectionModel().selectionChanged.connect(self.checkActions)  # dangeroous for segfaults!?
        self.sig_setProgressValue.connect(self.setProgressValue)

    ##################################################################################################Override built in

    def closeEvent(self, QCloseEvent):
        """
        Catch the QCloseEvent, when the user wants to close the window by clicken the "x" in the Window Corner or
        via Menues. Ask the engine if something is "dirty" this means not in "stored" condition.
        If yes, the user will be asked by the engine if he want to save his changes.
        If the user aborting, nothing will happen, because the signal will be ignored.

        :param QCloseEvent: QCloseEvent()
        :return: close, or not close the window
        """

        QCloseEvent.accept()              # close Window

    ############################################################################################################# Slots

    @pyqtSlot()                      #caller:      self.ACTaddPos
    def on_addPos(self):

        self.tW_workbench.addFiles(self.tv_selectedFiles())

    @pyqtSlot()                        #caller:      self.ACTprintCalc
    def printingDlg(self):
        """
        Create a new Webview which is used to render HTML which is generated from the engine and submitted to a
        QPrinter (QPrintPreviewDialog).
        """
        pass

    @pyqtSlot()                        #caller:      self.ACThelp
    def show_help(self):
        '''
        Displays a non-modal help window which is basically a web-browser which browses pre-definded html-pages
        :return:
        '''
        pass

    @pyqtSlot()                        #caller:      self.ACTabout
    def show_about(self):
        '''
        Displays a non-modal about window which is basically a web-browser which browses pre-definded html-pages
        :return:
        '''
        pass

    ###################################################################################################Helper Functions

    def tv_selectedFiles(self, filters=["png","jpg","jpeg","gif"]):
        selected_files = []
        selected_indexes = self.tV_Fileview.selectedIndexes()
        for index in selected_indexes:
            filename = self.tV_Fileview.model().filePath(index)
            if os.path.isfile(filename):
                for entry in filters:
                    if filename.endsWith(entry, Qt.CaseInsensitive):
                        selected_files.append(filename)
                        break
        return selected_files

    @pyqtSlot()
    def showStatusBarText(self, text, time=5000):
        """
        Show the "text" for "5000" ms in statusbar
        :param text: String
        :param time: int
        """
        self.statusBar().showMessage(text, time)

    @pyqtSlot(int)
    def setProgressValue(self, value):

        if value == -1:                        #pulse
            if self.progressBar.isHidden():
                #app.setOverrideCursor(QCursor(Qt.WaitCursor))
                self.progressBar.setVisible(True)
            self.progressBar.setRange(0, 0)   #show busy
        elif value >= 0 and value <= 99:

            if self.progressBar.isHidden():
                self.progressBar.setVisible(True)
            self.progressBar.setRange(0, 100)
            self.progressBar.setValue(value)
            if value == 0:
                if self.progressBar.isVisible():
                    self.progressBar.setVisible(False)
                #app.restoreOverrideCursor()
            #else:
                #app.setOverrideCursor(QCursor(Qt.WaitCursor))
        elif value == 100:
            print("Restore")
            if self.progressBar.isHidden():
                self.progressBar.setVisible(True)
            self.progressBar.setRange(0, 100)
            self.progressBar.setValue(100)
            #app.processEvents()
            self.showStatusBarText(self.tr("Finished!"))
            QTimer.singleShot(1000, lambda: self.setProgressValue(0))
            #app.restoreOverrideCursor()

        #app.processEvents()

    @pyqtSlot()                        #caller:       self.engine (direct)   self.engine.view.model()
    def askQuestion(self, TITLE, TEXT1, BTN1, TEXT2=None, BTN2=None):
        '''
        Bring up a modal QMessageBox

        :param TITLE: Windwtitle
        :param TEXT1: First Textline
        :param BTN1:  First Buttontext
        :param TEXT2: Second Textline
        :param BTN2:  Second Buttontext
        :return: 0 if the dialog button1 was clicked, 1 of button2 was clicked
        '''

        title = str(unicode(TITLE).encode("utf-8")) if isinstance(TITLE, QString) else str(TITLE)
        text1 = str(unicode(TEXT1).encode("utf-8")) if isinstance(TEXT1, QString) else str(TEXT1)
        btn1 = str(unicode(BTN1).encode("utf-8")) if isinstance(BTN1, QString) else str(BTN1)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle(title.decode("utf-8"))
        msgBox.setText("%s" % text1.decode("utf-8"))
        if TEXT2 is not None:
            msgBox.setInformativeText("%s" % str(unicode(TEXT2).encode("utf-8")) \
                                          if isinstance(TEXT2, QString) else str(TEXT2).decode("utf-8"))
        msgBox.addButton("%s" % btn1.decode("utf-8"), QMessageBox.ActionRole)                             # ret = 0
        if BTN2 is not None: msgBox.addButton("%s" % str(unicode(BTN2).encode("utf-8")) \
                                                  if isinstance(BTN2, QString) else str(BTN2).decode("utf-8"),
                                              QMessageBox.RejectRole)        # ret = 2
        ret = msgBox.exec_()
        ret = int(ret)

        if ret == 0:
            return 0       # Result Button 1 (OK)
        else:
            return 1       # Result Button 2 (Cancel)

    def dummy(self):
        print("DUMMY: Not implemented yet!")


class WorkerThread(QThread):

    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self._result = None
        self._result = self.function(*self.args,**self.kwargs)
        return

    def result(self):
        return self._result




if __name__ == "__main__":
    ######################################## Read Command-Line Arguments and store it into a dict. call e.g. args["all"]
    parser = argparse.ArgumentParser(description='*** '+__title__+' ***  by Matthias Laumer')
    parser.add_argument("-d", "--debug", action='store_true', help='Debug-Mode.',
                        required=False)
    args = vars(parser.parse_args())
    ############################################################################################################# Logger
    setupLogger(console=True, File=True, Filebackupcount=1, Variable=False)
    sys.excepthook = excepthook  # log uncaught exceptions to the log-file

    ################################################################################################### SIGTERM Handling
    # sigterm is distributed when linux is going to halt or ctrl+c is pressed to abort the script-execution
    # but maybe some cleanup actions are necessary
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    app = QApplication([])
    try:  # windows only http://stackoverflow.com/questions/12432637/pyqt4-set-windows-taskbar-icon
        import ctypes
        myappid = u'matthias_laumer.{0}.subproduct.{1}'.format(__title__, __version__) # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        print("running in Linux")
    app.setApplicationName(__title__)

    language = unicode(QLocale.system().name())
    qtTranslator = QTranslator()
    qtTranslator.load("qt_{0}".format(language), QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    mytranslator = QTranslator()
    mytranslator.load("local_{0}".format(language), os.path.join(cwd, "locale"))
    app.installTranslator(mytranslator)

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

"""
Version-History:

0.0.1   Initial Version

ToDo's:

-

"""