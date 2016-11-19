import sys, os
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
        Takes a list with Filenames and creates new rows and populate with the given data
        :param filepathslist: [PyQt4.QtCore.QUrl(u'file:///home/matthias/Bilder/test1.jpg')]
        :return:
        '''
        if len(filepathslist) == 0:
            return False

        for i, file in enumerate(filepathslist):
            self.sig_setProgressValue.emit(100/len(filepathslist) * i)
            if isinstance(file, QUrl):
                file = file.toLocalFile()   # convert filepath from QUrl to a QString
            if not os.path.isfile(file):
                continue   # override dirs!

            i = self.rowCount()
            # Load Picture:
            pic = QPixmap(file).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            picture_entry = QTableWidgetItem()
            picture_entry.setData(Qt.DecorationRole, pic)

            # Load Name:
            name = os.path.basename(unicode(file))
            name_entry = QTableWidgetItem(name)
            name_entry.setData(Qt.UserRole, file)

            # Calculate Size
            size = self.humansize(os.path.getsize(file))
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