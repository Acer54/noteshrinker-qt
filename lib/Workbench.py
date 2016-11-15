import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Workbench_Tablewidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        QTableWidget.__init__(self, *args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDragDropOverwriteMode(False)

        self.verticalHeader().setMovable(True)  #Keep Numbering
        self.verticalHeader().sectionMoved.connect(self.renumberHeader)

        # self.setSelectionMode(QAbstractItemView.SingleSelection)

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

        #print("Drop!")
        if event.source() == self:
            #print("internal")
            # The QTableWidget from which selected rows will be moved
            sender = event.source()

            # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
            QTableWidget.dropEvent(self, event)
            # Now we know where to insert selected row(s)
            dropRow = self.last_drop_row

            selectedRows = sender.getselectedRowsFast()

            # Allocate space for transfer
            for _ in selectedRows:
                self.insertRow(dropRow)

            # if sender == receiver (self), after creating new empty rows selected rows might change their locations
            sel_rows_offsets = [0 if self != sender or srow < dropRow else len(selectedRows) for srow in selectedRows]
            selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]

            # copy content of selected rows into empty ones
            for i, srow in enumerate(selectedRows):
                for j in range(self.columnCount()):
                    cellWidget = None
                    item = sender.item(srow, j)
                    if item is None:
                        cellWidget = sender.cellWidget(srow, j)
                    if item:
                        source = QTableWidgetItem(item)
                        self.setItem(dropRow + i, j, source)
                        #self.selectRow(dropRow + i)
                        self.setItemSelected(source, True)
                    elif cellWidget is not None:
                        self.setCellWidget(dropRow + i, j, cellWidget)

            # delete selected rows
            for srow in reversed(selectedRows):
                sender.removeRow(srow)

            self.resizeRowsToContents()
            self.renumberHeader()
            event.accept()
        elif event.mimeData().hasFormat('text/uri-list'):
            self.addFiles(event.mimeData().urls()) # This is a list with QURLs
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
        for file in filepathslist:
            if isinstance(file, QUrl):
                file = file.toLocalFile()   # convert filepath from QUrl to a QString
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
            size = self.humansize(os.path.getsize('/home/matthias/Bilder/test2.jpg'))
            size_entry = QTableWidgetItem(size)

            # Create a "Delete-Button"
            btn = QPushButton(self.tr("Remove"))
            btn.object = name_entry   # this attr will be read by "remove" to identifie the corret row to remove
            #TODO: Create connection to "Remove"

            self.insertRow(i)
            self.setItem(i, 0, picture_entry)
            self.setItem(i, 1, name_entry)
            self.setItem(i, 2, size_entry)
            self.setCellWidget(i, 3, btn)
            self.resizeRowsToContents()

    def onRemoveBtn(self, btn):
        pass

    def removeFiles(self, filelist):
        pass


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