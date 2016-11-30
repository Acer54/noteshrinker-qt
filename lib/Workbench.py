import sys, os
from argparse import Namespace
from copy import deepcopy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Workbench_Tablewidget(QTableWidget):

    """
    A Tablewidget which supports Drag and Drop for internal move (Drag/Drop by moving vertical Headers or Rows)
    You also can call "moveUp" , "moveDown" to move (single or multiple) rows up or down or drag an drop multiple rows.
    """

    # custom signal with an integer value telling the status when doing a long process
    sig_setProgressValue = pyqtSignal(int)
    sig_filesAccepted = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QTableWidget.__init__(self, *args, **kwargs)
        #======================= Settings ============================================================================#
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)    # disable editable items
        self.setDragEnabled(True)                                 # Drag (internal) is allowed
        self.setAcceptDrops(True)                                 # Drops (internal & external) are allowed
        self.viewport().setAcceptDrops(True)                      # My Viewport (mainwindow) also accept Drops
        self.setSelectionBehavior(QAbstractItemView.SelectRows)   # Only complete rows can be selected
        self.setDragDropMode(QAbstractItemView.DragDrop)          # normal Drag-Drop behaviour
        self.setDragDropOverwriteMode(False)                      # do not "replace" Items with dropped content
        self.verticalHeader().setMovable(True)                    # this keeps the numbering, we do not want this
        self.verticalHeader().sectionMoved.connect(self.renumberHeader)  # Renumber 1.2.3... after move (custom-funct)
        # self.setSelectionMode(QAbstractItemView.SingleSelection) # multiple rows can be selected for drag or removal
        #======================= Variables ===========================================================================#
        self.last_drop_row = None
        self.generalOption = self.empty_default_options()
        self.global_active = False

    def empty_default_options(self):
        '''
        Initial "empty" options, representing the default values of noteshrink (without filename!)
        :return: Namespace-Obj (argparse)
        '''
        return Namespace(basename='page', filenames=[], global_palette=False,
                         num_colors=8, pdf_cmd='convert %i %o', pdfname='output.pdf', postprocess_cmd=None,
                         postprocess_ext='_post.png', quiet=False, sample_fraction=0.05, sat_threshold=0.2,
                         saturate=True, sort_numerically=True, value_threshold=0.25, white_bg=False)

    def set_global_option(self, namespace_obj):
        '''
        Takes a namespace_object, extracts the filename and sets the rest to all listed Items in the workbench.
        The filename is replaced with the unique on.
        :param namespace_obj: Namespace()
        :return: True / False
        '''
        # get the cleaned Namespace obj (without filename) (deepcopy) for self.generalOption (affecting all new)
        # list all items,
        # iter over each item and set the new option including the correct filename
        # set self.global_active to True
        # return True if it was successful
        return True

    def is_global_aktive(self):
        '''
        self.global_active is only a softwareswith, holding the state of "Apply_to_all" Button
        :return: True or False, depending on the state
        '''
        return self.global_active

    def unset_global_active(self):
        '''
        Setting the defaults back to standard (does only affect new items)
        :return: True
        '''
        self.generalOption = self.empty_default_options()   #set the standard-default values for ne items
        self.global_active = False
        return True

    def reset_option(self, item):
        '''
        Take an item and resetting his options to the programm defaults.
        :param item:
        :return: True / False
        '''
        # extract the options obj.
        # set empty default with the right filename
        return True

    def reset_all(self):
        '''
        Reset all listed items (this is called when "self.global_active" is True)
        :return: True / False
        '''
        # iter over each item and reset the option (self.reset_option())

        return True

    def get_selected_Item(self, pic_or_name):
        '''
        Returns the currently selected Item (pic or name) of the current selected row. But only if there is exactely
        one.
        :param pic_or_name: str()
        :return: QTablewidgetItem()
        '''
        # do not provide if more than one is selected or if nothing is selected
        if len(self.getselectedRowsFast()) > 1 or len(self.getselectedRowsFast()) == 0:
            return list()
        # this is only executed if there is exactly one selected item
        if pic_or_name == "name":
            for item in self.selectedItems():
                if item.column() == 1:  # choose the "Name" Item
                    nameItem = item
                    break
            else:
                return False
            return nameItem
        elif pic_or_name == "pic":
            for item in self.selectedItems():
                if item.column() == 0:  # choose the "picture" Item
                    pictureItem = item
                    break
            else:
                return False
            return pictureItem

    def renumberHeader(self, *args):

        headers = []
        realOrder = []
        changed = []
        for i in range(0, self.rowCount()):
            realOrder.append(self.verticalHeader().visualIndex(i))
        for j in range(1, self.rowCount()+1):
            headers.append(j)
        for k, index in sorted(zip(headers, realOrder)):
            changed.append(str(index+1))
        self.setVerticalHeaderLabels(changed)

    # Override this method to get the correct row index for insertion
    def dropMimeData(self, row, col, mimeData, action):
        self.last_drop_row = row
        return True

    def dropEvent(self, event):

        if event.source() == self:
            # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
            QTableWidget.dropEvent(self, event)
            # Now we know where to insert selected row(s)
            dropRow = self.last_drop_row
            selectedRows =self.getselectedRowsFast()
            self.moveRows(selectedRows, dropRow)

            event.accept()
        elif event.mimeData().hasFormat('text/uri-list'):
            self.addFiles(event.mimeData().urls()) # This is a list with QURLs
            event.accept()
        else:
            event.ignore()

    def getselectedRowsFast(self):
        selectedRows = []
        for item in self.selectedItems():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
        selectedRows.sort()
        return selectedRows

    def dragEnterEvent(self, e):
        #print(e.mimeData().formats()[0])
        if e.mimeData().hasFormat('text/uri-list') or e.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        e.accept()

    def addFiles(self, filepathslist):
        '''
        Takes a list with Filepathes or Folderpathes and creates new rows and populate with the given data
        :param filepathslist: [PyQt4.QtCore.QUrl(u'file:///home/matthias/Bilder/test1.jpg')]  or QString or str list
        :return:
        '''
        if len(filepathslist) == 0:
            return False

        additionalFilePaths = []
        for j, path in enumerate(filepathslist):
            if isinstance(path, QUrl):
                path = path.toLocalFile()   # convert filepath from QUrl to a QString
            if not os.path.isfile(unicode(path)):           #if a folder is included
                filepathslist.pop(j)   # remove the folder path from filelist
                for filetocheck in os.listdir(unicode(path)):
                    print("Check:", filetocheck)
                    if filetocheck.endswith(tuple(['.png', '.jpg', '.jpeg', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF'])):
                        print("adding", os.path.join(unicode(path), unicode(filetocheck)))
                        additionalFilePaths.append(os.path.join(unicode(path), unicode(filetocheck)))

        filepathslist = filepathslist + additionalFilePaths


        for i, file in enumerate(filepathslist):
            self.sig_setProgressValue.emit(100/len(filepathslist) * i)
            if isinstance(file, QUrl):
                file = file.toLocalFile()   # convert filepath from QUrl to a QString
            if not os.path.isfile(unicode(file)):
               continue   # override dirs!  just to be sure

            i = self.rowCount()
            # Load Picture:
            pic = QPixmap(file).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            picture_entry = QTableWidgetItem()
            picture_entry.setData(Qt.DecorationRole, pic)
            picture_entry.setData(Qt.UserRole, [None, None])   # there is no valid preview

            # Load Name:
            name = os.path.basename(unicode(file))
            name_entry = QTableWidgetItem(name)
            options = deepcopy(self.generalOption)  # Namespace(basename='page', filenames=[unicode(file)], global_palette=False,
            options.filenames = [unicode(file)]
            name_entry.setData(Qt.UserRole, options)

            # Calculate Size
            size = self.humansize(os.path.getsize(unicode(file)))
            size_entry = QTableWidgetItem(size)

            # Create a "Delete-Button"
            btn = QPushButton(self.tr("Remove"))
            btn.object = name_entry   # this attr will be read by "remove" to identifie the corret row to remove
            btn.clicked.connect(self.onRemoveBtn)

            self.insertRow(i)
            self.setItem(i, 0, picture_entry)
            self.setItem(i, 1, name_entry)
            self.setItem(i, 2, size_entry)
            self.setCellWidget(i, 3, btn)
            self.resizeRowsToContents()

        self.sig_setProgressValue.emit(100)
        self.sig_filesAccepted.emit()

    @pyqtSlot()                              # Connected to "clicked" of the "Remove" Buttons
    def onRemoveBtn(self):
        button = self.sender()
        index = self.indexAt(button.pos())
        if index.isValid():
            self.removeRow(index.row())
            self.renumberHeader()

    @pyqtSlot()                              # Connected to "clicked" of the "Remove" Buttons
    def removeMarked(self):
        index_list = []
        for model_index in self.selectionModel().selectedRows():
            index = QPersistentModelIndex(model_index)
            index_list.append(index)

        for index in index_list:
            self.removeRow(index.row())
        self.renumberHeader()

    @pyqtSlot()                              # Connected to "clicked" of the "Remove" Buttons
    def moveDown(self):

        selectedRows = self.getselectedRowsFast()
        dropRow = selectedRows[0] +len(selectedRows) +1
        if dropRow < self.rowCount()+1:
            self.moveRows(selectedRows, dropRow)

    @pyqtSlot()                              # Connected to "clicked" of the "Remove" Buttons
    def moveUp(self):
        selectedRows = self.getselectedRowsFast()
        dropRow = selectedRows[0] -1
        if dropRow >= 0:
            self.moveRows(selectedRows, dropRow)

    def moveRows(self, selectedRows, targetrow):
        # Allocate space for transfer
        for _ in selectedRows:
            self.insertRow(targetrow)
        # if self == receiver (self), after creating new empty rows selected rows might change their locations
        sel_rows_offsets = [0 if srow < targetrow else len(selectedRows) for srow in selectedRows]
        selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]

        # copy content of selected rows into empty ones
        for i, srow in enumerate(selectedRows):
            for j in range(self.columnCount()):
                cellWidget = None
                item = self.item(srow, j)
                #TODO: Maybe Data have to be saved here ??? > Preview Image, Options-Data, md5_hash aso.
                if item is None:
                    cellWidget = self.cellWidget(srow, j)
                if item:
                    source = QTableWidgetItem(item)
                    self.setItem(targetrow + i, j, source)
                elif cellWidget is not None:
                    self.setCellWidget(targetrow + i, j, cellWidget)
        #select the new rows
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        for selection in range(len(selectedRows)):
            self.selectRow(targetrow+selection)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # delete selected rows
        for srow in reversed(selectedRows):
            self.removeRow(srow)

        self.resizeRowsToContents()
        self.renumberHeader()

    def humansize(self, nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])





class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.table_widget = Workbench_Tablewidget()
        layout.addWidget(self.table_widget)

        # setup table widget
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Colour', 'Model'])

        items = [('Red', 'Toyota'), ('Blue', 'RV'), ('Green', 'Beetle')]
        for i, (colour, model) in enumerate(items):
            c = QTableWidgetItem(colour)
            m = QTableWidgetItem(model)

            self.table_widget.insertRow(self.table_widget.rowCount())
            self.table_widget.setItem(i, 0, c)
            self.table_widget.setItem(i, 1, m)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())