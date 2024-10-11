#!/usr/bin/env python3
"""
Module PYSIDE2.IMAGEVIEW -- Python PySide 2 Image View Objects
Sub-Package UI.TOOLKITS.PYSIDE2 of Package PLIB3 -- Python UI Toolkits
Copyright (C) 2008-2022 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the PySide 2 UI objects for the panel widgets.
"""

from PySide2 import QtCore as qtc, QtGui as qtg, QtWidgets as qt

from plib.ui.base.imageview import PImageViewBase

from .app import PQtWidget


class PImageView(PQtWidget, qt.QScrollArea, PImageViewBase):
    
    image_view = None
    
    def __init__(self, manager, parent, filename=None, geometry=None):
        qt.QScrollArea.__init__(self, parent)
        self.setAlignment(qtc.Qt.AlignTop | qtc.Qt.AlignLeft)
        PImageViewBase.__init__(self, manager, parent, filename=filename, geometry=geometry)
    
    @staticmethod
    def supported_formats():
        # This must not be called until after the application object is created
        # Note: for some reason the obvious way of doing this, calling bytes on each
        # format (as is done in the qt5 toolkit), segfaults on PySide 2, so we have
        # to use the hack below
        return [b''.join(s for s in f).decode() for f in qtg.QImageReader.supportedImageFormats()]
    
    def load_from_file(self, filename):
        pixmap = qtg.QPixmap(filename)
        self.image_view = qt.QLabel()
        self.image_view.setAlignment(qtc.Qt.AlignTop | qtc.Qt.AlignLeft)
        self.image_view.setPixmap(pixmap)
        self.setWidget(self.image_view)
    
    def get_image_size(self):
        size = self.image_view.pixmap().size()
        return size.width(), size.height()
    
    def zoom_to(self, width, height):
        pixmap = self.image_view.pixmap()
        self.image_view.setPixmap(pixmap.scaled(width, height, qtc.Qt.KeepAspectRatio))
        self.image_view.resize(width, height)
    
    def rotate_90(self, clockwise):
        width, height = self.get_image_size()
        transform = qtg.QTransform()
        transform.rotate(90.0 * (1.0 if clockwise else -1.0))
        pixmap = self.image_view.pixmap()
        self.image_view.setPixmap(pixmap.transformed(transform))
        self.image_view.resize(height, width)
