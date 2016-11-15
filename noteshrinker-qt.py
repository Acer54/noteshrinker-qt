#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################################################################
# Description:
#
#
#
#######################################################################################################################


import sys, os, logging, logging.handlers, io, argparse, time, signal, ConfigParser
import res.res
from lib import global_vars
from ui.mainwindow import Ui_MainWindow_noteshrinker_qt
from lib.FileSystemView import LM_QFileSystemModel, FileIconProvider
from PyQt4.QtCore import *
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


def read_conf(filepath, extention=".ini"):
    '''
    Reading a ini-like configuration-File and return it in a dict. {section:{option:value}}
    :param filepath: absolute filepath to the configuration-file
    :param extention: ".ini", ".conf", ".whatever"
    :return: Dict {'General': {'second': '1', 'thisisabool': True, 'key': '"value"'}}
    '''

    if not os.path.exists(filepath):
        logger.error(_('Configuration-File "{0}" does not exist').format(filepath))
        return False
    else:
        basename = os.path.basename(filepath)

    logger.info(_('Reading Configuration-File "{0}"').format(basename))
    if not os.path.isfile(filepath):
        logger.error(_('Configuration "{0}" does not exist or can not be accessed.').format(basename))
        raise IOError

    if not os.path.splitext(filepath)[1] == extention:
        logger.error(_('Configuration-File "{0}" has wrong file-format (need {1})').format(basename, extention))
        raise IOError
    target = {}
    try:
        config = ConfigParser.RawConfigParser(allow_no_value=False)
        config.read(filepath)
        sections = config.sections()
        for section in sections:
            target.setdefault(section, {})
            options = config.options(section)
            for option in options:
                try:
                    # this is the Value
                    tempopt = config.get(section, option)
                    # Check if the value should be a boolian Value... and convert if necessary
                    if tempopt in ["true", "True", "TRUE"]:
                        logger.debug(_("Convert value '{0}' from Option {1} to bool").format(tempopt, option))
                        tempopt = True
                    elif tempopt in ["false", "False", "FALSE"]:
                        logger.debug(_("Convert value '{0}' from Option {1} to bool").format(tempopt, option))
                        tempopt = False
                    elif tempopt in [None, ""]:
                        logger.debug(_("Setting Value '{0}' from Option {1} to None-Type").format(tempopt, option))
                        tempopt = None

                    target[section][option] = tempopt
                except:
                    e = sys.exc_info()[0]
                    logger.error(_("exception on {0} with {1}! Will override this with 'None-Type'").format(option, e))
                    target[section][option] = None
        logger.info(_("Reading Configurations-File complete."))
        return target
    except:
        e = sys.exc_info()[0]
        logger.error(_("Configuration {0} can not be read! Error: {1}").format(filepath, e))
        raise IOError


###################### Read Configuration-File (webradio.conf) #######################
if os.path.isfile(os.path.join(cwd, "noteshrinker.conf")):
    global_vars.configuration = read_conf(os.path.join(cwd, "noteshrinker.conf"), ".conf")
else:
    raise ImportError("No Configuration-File found! Check webradio.conf")


class MainWindow(QMainWindow, Ui_MainWindow_noteshrinker_qt):
    '''
    All the visible aspects which have to be handled are in this class.
    '''

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

        self.tW_workbench.setHorizontalHeaderLabels(['Preview', 'Filename', 'Size', ''])

        items = [('/home/matthias/Bilder/test1.jpg',
                  'Simone', str(os.path.getsize('/home/matthias/Bilder/test1.jpg')), 'BTN'),
                 ('/home/matthias/Bilder/test2.jpg',
                  'Willi', str(os.path.getsize('/home/matthias/Bilder/test2.jpg')), 'BTN'),
                 ('/home/matthias/Bilder/test3.jpg',
                  'Walter', str(os.path.getsize('/home/matthias/Bilder/test3.jpg')), 'BTN')]
        for i, (path, name, size, btn) in enumerate(items):
            c = QTableWidgetItem()
            pic = QPixmap(path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            c.setData(Qt.DecorationRole, pic)
            m = QTableWidgetItem(name)
            n = QTableWidgetItem(size)
            o = QTableWidgetItem(btn)


            self.tW_workbench.insertRow(self.tW_workbench.rowCount())
            self.tW_workbench.setItem(i, 0, c)
            self.tW_workbench.setItem(i, 1, m)
            self.tW_workbench.setItem(i, 2, n)
            self.tW_workbench.setItem(i, 3, o)

        #item = QTableWidgetItem()
        #pic = QPixmap("/home/matthias/Bilder/noteshring_qt_first_draft.png")
        #small = pic.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #item.setData(Qt.DecorationRole, small)
        #self.tW_workbench.setItem(0, 0, item)

        self.tW_workbench.resizeRowsToContents()    # enlarge the hight of the row, according to the preview


    def createActions(self):
        """
        Create Actions which are used in Toolbar, Menue and context-menues
        """
        pass


    def createMenus(self):
        """
        Create the Mainwindow meneu   " Datei  |   Bearbeiten   |   Extras   |   Hilfe "
        :return:
        """
        pass

    def createToolBars(self):
        """
        A single Toolbar is used.
        """
        pass

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
        pass

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

    @pyqtSlot()
    def showStatusBarText(self, text, time=5000):
        """
        Show the "text" for "5000" ms in statusbar
        :param text: String
        :param time: int
        """
        self.statusBar().showMessage(text, time)

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
    user_lang = global_vars.configuration.get("GENERAL").get("language")
    if user_lang is not None:
        logger.info("Load Userspecific Language")
        language = user_lang
        mytranslator.load("local_{0}".format(language), os.path.join(cwd, "locale"))

    #app.installTranslator(mytranslator)  # Installation will be handeled by the GUI

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

"""
Version-History:

0.0.1   Initial Version

ToDo's:

-

"""