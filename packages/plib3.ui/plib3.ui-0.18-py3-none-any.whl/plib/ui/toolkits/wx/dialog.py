#!/usr/bin/env python3
"""
Module WX.DIALOG -- Python wxWidgets Dialog Widget
Sub-Package UI.TOOLKITS.WX of Package PLIB3 -- Python UI Toolkits
Copyright (C) 2008-2022 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the wxWidgets UI objects for the dialog widget.
"""

import wx

from plib.ui.defs import *
from plib.ui.base.dialog import PDialogBase

from .app import PWxWidget


class PDialog(PWxWidget, wx.Dialog, PDialogBase):
    
    def __init__(self, manager, parent, caption, client,
                 accept_buttons=('ok', 'yes'), reject_buttons=('cancel', 'no')):
        
        wx.Dialog.__init__(self, parent)
        PDialogBase.__init__(self, manager, parent, caption, client,
                             accept_buttons=accept_buttons, reject_buttons=reject_buttons)
        self.handlers = []
    
    def set_caption(self, caption):
        self.SetTitle(caption)
    
    def set_size(self, width, height):
        self.SetClientSize(width, height)
    
    def do_display(self):
        self.Show(True)
    
    def connect_target(self, signal, target):
        if signal == SIGNAL_FINISHED:
            # FIXME: wx dialogs do not seem to fire the EVT_CLOSE
            # event when the docs say they should
            self.handlers.append(target)
        else:
            super(PDialog, self).connect_target(signal, target)
    
    def EndDialog(self, accepted):
        for handler in self.handlers:
            handler(accepted)
        self.Show(False)
        self.Destroy()
    
    def accept_changes(self):
        self.EndDialog(True)
    
    def reject_changes(self):
        self.EndDialog(False)
