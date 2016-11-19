#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QFileSystemModel, QFileIconProvider, QIcon
from PyQt4.QtCore import pyqtSignal, Qt


class LM_QFileSystemModel(QFileSystemModel):

    directoryLoading = pyqtSignal()
    def __init__(self, parent=None):
        QFileSystemModel.__init__(self, parent)
        self.setNameFilterDisables(False)
        self.isReady = True
        self.directoryLoading.connect(self.__busy)
        self.directoryLoaded.connect(self.__ready)

    def __busy(self, arg=None):
        self.isReady = False

    def __ready(self, arg=None):
        self.isReady = True

    def isReady(self):
        return self.isReady

    def fetchMore(self, QModelIndex):
        #self.emit(SIGNAL("loading"))
        self.directoryLoading.emit()
        return QFileSystemModel.fetchMore(self, QModelIndex)

    def get_childs(self, QModelIndex):
        childlist = []
        for i in xrange(self.rowCount(QModelIndex)):
            child = self.index(i,0, QModelIndex)
            childlist.append(child)
        return childlist

class FileIconProvider(QFileIconProvider):

    def __init__(self):
        QFileIconProvider.__init__(self)

    def icon(self, arg):
        if arg.completeSuffix() in ["PNG", "png", "jpg", "JPG", "JPEG", "jpeg", "GIF", "gif"]:
            return QIcon(":/image.png")
        else:
            return QFileIconProvider.icon(self, arg)