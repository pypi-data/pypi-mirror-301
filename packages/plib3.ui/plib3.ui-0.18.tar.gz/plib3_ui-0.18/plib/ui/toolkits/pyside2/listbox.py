#!/usr/bin/env python3
"""
Module PYSIDE2.LISTBOX-- Python PySide 2 List Box Objects
Sub-Package UI.TOOLKITS.PYSIDE2 of Package PLIB3 -- Python UI Toolkits
Copyright (C) 2008-2022 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the PySide 2 UI objects for the tree/list view widgets.
"""

from PySide2 import QtWidgets as qt

from plib.ui.base.listbox import PListBoxBase, PSortedListBoxBase

from .app import PQtSequenceWidget


class PQtListBoxBase(PQtSequenceWidget, qt.QListWidget):
    
    fix_width_on_resize = True
    
    def __init__(self, parent):
        qt.QListWidget.__init__(self, parent)
        self.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
    
    #def item_height(self, index):
    #    return self.itemWidget(self.item(index)).height()
    
    def current_index(self):
        return self.currentRow()
    
    def set_current_index(self, index):
        self.setCurrentRow(index)
    
    def count(self, value):
        # Method name collision, we want it to be the Python sequence
        # count method here.
        return PListBoxBase.count(self, value)
    
    def _indexlen(self):
        # Let this method access the Qt combo box count method.
        return qt.QListWidget.count(self)
    
    def _get_data(self, index):
        return str(self.item(index).text())
    
    def _set_data(self, index, value):
        self.item(index).setText(str(value))
    
    def _add_data(self, index, value):
        self.insertItem(index, str(value))
    
    def _del_data(self, index):
        self.takeItem(index)


class PListBox(PQtListBoxBase, PListBoxBase):
    
    def __init__(self, manager, parent, items=None, value=None,
                 geometry=None, font=None):
        
        PQtListBoxBase.__init__(self, parent)
        PListBoxBase.__init__(self, manager, parent, items, value=value,
                              geometry=geometry, font=font)


class PSortedListBox(PQtListBoxBase, PSortedListBoxBase):
    
    def __init__(self, manager, parent, items=None, value=None,
                 geometry=None, font=None, key=None):
        
        PQtListBoxBase.__init__(self, parent)
        PSortedListBoxBase.__init__(self, manager, parent, items, value=value,
                                    geometry=geometry, font=font, key=key)
