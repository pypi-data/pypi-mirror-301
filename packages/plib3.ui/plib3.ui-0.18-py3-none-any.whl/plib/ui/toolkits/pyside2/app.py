#!/usr/bin/env python3
"""
Module PYSIDE2.APP -- Python PySide 2 Application Objects
Sub-Package UI.TOOLKITS.PYSIDE2 of Package PLIB3 -- Python UI Toolkits
Copyright (C) 2008-2022 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the PySide 2 UI application objects.
"""

import sys

from abc import ABCMeta

from PySide2 import QtCore as qtc, QtGui as qtg, QtWidgets as qt

from plib.ui.defs import *
from plib.ui.base.app import (
    PMessageBoxBase, PFileDialogBase, PAboutDialogBase, PProgressDialogBase,
    PTopWindowBase, PApplicationBase
)


align_map = {
    ALIGN_LEFT: qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter,
    ALIGN_CENTER: qtc.Qt.AlignCenter,
    ALIGN_RIGHT: qtc.Qt.AlignRight | qtc.Qt.AlignVCenter
}

color_map = dict(
    (color, qtg.QColor(color.lower()))
    for color in COLORNAMES
)

accel_map = {
    ACTION_FILE_NEW: qtg.QKeySequence.New,
    ACTION_FILE_OPEN: qtg.QKeySequence.Open,
    ACTION_FILE_SAVE: qtg.QKeySequence.Save,
    ACTION_FILE_SAVEAS: qtg.QKeySequence.SaveAs,
    ACTION_FILE_CLOSE: qtg.QKeySequence.Close,
    ACTION_EDIT_UNDO: qtg.QKeySequence.Undo,
    ACTION_EDIT_REDO: qtg.QKeySequence.Redo,
    ACTION_EDIT_CUT: qtg.QKeySequence.Cut,
    ACTION_EDIT_COPY: qtg.QKeySequence.Copy,
    ACTION_EDIT_PASTE: qtg.QKeySequence.Paste,
    ACTION_EDIT_DELETE: qtg.QKeySequence.Delete,
    ACTION_EDIT_SELECTALL: qtg.QKeySequence.SelectAll,
    ACTION_EDIT_SELECTNONE: qtg.QKeySequence.Deselect,
    ACTION_EDIT_OVERWRITE: "Ins",
    #ACTION_EDIT_CLEAR: qtg.QKeySequence.,
    #ACTION_VIEW: qtg.QKeySequence.,
    #ACTION_EDIT: qtg.QKeySequence.,
    #ACTION_OK: qtg.QKeySequence.,
    ACTION_CANCEL: qtg.QKeySequence.Cancel,
    ACTION_REFRESH: qtg.QKeySequence.Refresh,
    #ACTION_ADD: qtg.QKeySequence.,
    #ACTION_REMOVE: qtg.QKeySequence.,
    #ACTION_APPLY: qtg.QKeySequence.,
    #ACTION_COMMIT: qtg.QKeySequence.,
    #ACTION_ROLLBACK: qtg.QKeySequence.,
    ACTION_PREFS: qtg.QKeySequence.Preferences,
    ACTION_ABOUT: "Alt+B",
    ACTION_ABOUT_TOOLKIT: "Alt+T",
    ACTION_EXIT: qtg.QKeySequence.Quit,
}

message_funcs = {
    MBOX_INFO: qt.QMessageBox.information,
    MBOX_WARN: qt.QMessageBox.warning,
    MBOX_ERROR: qt.QMessageBox.critical,
    MBOX_QUERY: qt.QMessageBox.question
}


signal_map = {
    SIGNAL_ACTIVATED: "triggered",
    SIGNAL_CLICKED: "clicked",
    SIGNAL_TOGGLED: "toggled",
    SIGNAL_SELECTED: "currentIndexChanged",
    SIGNAL_LISTVIEWSELECTED: "currentItemChanged",
    SIGNAL_LISTBOXSELECTED: "currentRowChanged",
    SIGNAL_CELLSELECTED: "currentCellChanged",
    SIGNAL_TABLECHANGED: "cellChanged",
    SIGNAL_TEXTCHANGED: "textChanged",
    SIGNAL_TEXTMODCHANGED: "modificationChanged",
    SIGNAL_EDITCHANGED: "textChanged",
    SIGNAL_VALUECHANGED: "valueChanged",
    SIGNAL_ENTER: "returnPressed",
    SIGNAL_TABSELECTED: "currentChanged",
    SIGNAL_NOTIFIER: "activated",
    SIGNAL_FINISHED: "finished",
    SIGNAL_BEFOREQUIT: "aboutToQuit",
}

event_map = {
    SIGNAL_BUTTONSELECTED: ("sig_buttonSelected", (int,)),
    SIGNAL_NUMEDITCHANGED: ("sig_numEditChanged", (int,)),
    SIGNAL_CELLCHANGED: ("sig_cellChanged", (int, int)),
    SIGNAL_TEXTSTATECHANGED: ("sig_textStateChanged", ()),  # using selectionChanged above does not work
    SIGNAL_QUERYCLOSE: ("sig_canClose", ()),
    SIGNAL_CLOSING: ("sig_closeEvent", ()),
    SIGNAL_SHOWN: ("sig_showEvent", ()),
    SIGNAL_HIDDEN: ("sig_hideEvent", ()),
    
    SIGNAL_FOCUS_IN: ("sig_focusInEvent", ()),
    SIGNAL_FOCUS_OUT: ("sig_focusOutEvent", ()),
    SIGNAL_LEFTCLICK: ("sig_leftClickEvent", ()),
    SIGNAL_RIGHTCLICK: ("sig_rightClickEvent", ()),
    SIGNAL_MIDDLECLICK: ("sig_middleClickEvent", ()),
    SIGNAL_LEFTDBLCLICK: ("sig_leftDblClickEvent", ()),
    SIGNAL_RIGHTDBLCLICK: ("sig_rightDblClickEvent", ()),
    SIGNAL_MIDDLEDBLCLICK: ("sig_middleDblClickEvent", ()),
}


# This is provided to support the custom API; it must be called before
# any widget classes are declared

# Note: args must be the types of arguments for the event handler (as
# in event_map above)

def add_custom_signal(signame, *args):
    # Importing all from defs above will have retrieved the custom signal by name
    sig = getattr(sys.modules[__name__], signame)
    event_name = signame.lower()
    event_map[sig] = (event_name, args)


def map_args(signal):
    return (
        (signal_map[signal], ()) if signal in signal_map else
        event_map[signal] if signal in event_map else
        None
    )


def map_attr(signal):
    return map_args(signal)[0]


# Ugly hacks to fix metaclass conflicts for widget classes
# and to allow auto-construction of event signals without
# a lot of boilerplate code in each widget class

QtMeta = type(qtc.QObject)


def setup_event_signals(attrs, attrname='event_signals'):
    # This has to be done in a metaclass because new signals cannot be
    # dynamically added after a QObject subclass is created
    for signal in attrs.get(attrname, ()):
        signame, args = map_args(signal)
        attrs[signame] = qtc.Signal(*args, name=signame)


class PQtMeta(QtMeta):
    # Metaclass for non-sequence objects
    
    def __new__(meta, name, bases, attrs):
        setup_event_signals(attrs)
        return super(PQtMeta, meta).__new__(meta, name, bases, attrs)


# We need a different metaclass for sequence-like widgets
# because ABCMeta needs to be included

class PQtSequenceMeta(QtMeta, ABCMeta):
    # Metaclass for sequence objects
    
    def __init__(cls, name, bases, attrs):
        QtMeta.__init__(cls, name, bases, attrs)
        ABCMeta.__init__(cls, name, bases, attrs)


class PQtSignal(object):
    """Base class for common signal/slot functionality in Qt.
    """
    
    def connect_target(self, signal, target):
        sig = map_attr(signal)
        if sig is not None:
            try:
                getattr(self, sig).connect(target)
            except AttributeError:
                pass
    
    def do_notify(self, signal, *args):
        sig = map_attr(signal)
        if sig is not None:
            try:
                getattr(self, sig).emit(*args)
            except AttributeError:
                pass


class PQtActionMixin(object):
    
    def load_icon_from_data(self, data):
        px = qtg.QPixmap()
        px.loadFromData(data)
        return qtg.QIcon(px)
    
    def load_icon_from_file(self, filename):
        return qtg.QIcon(qtg.QPixmap(filename))
    
    def get_accel_str(self, key):
        return accel_map.get(key)


class PQtSequence(PQtSignal, metaclass=PQtSequenceMeta):
    """Base class for non-widgets that also appear as sequences.
    """
    pass


QtWidgetMeta = type(qt.QWidget)


class PQtWidgetMeta(QtWidgetMeta):
    # Metaclass for non-sequence widgets
    
    def __new__(meta, name, bases, attrs):
        setup_event_signals(attrs)
        setup_event_signals(attrs, 'signals')  # for custom signals
        return super(PQtWidgetMeta, meta).__new__(meta, name, bases, attrs)


class PQtSequenceWidgetMeta(PQtWidgetMeta, ABCMeta):
    # Metaclass for sequence widgets
    
    def __init__(cls, name, bases, attrs):
        PQtWidgetMeta.__init__(cls, name, bases, attrs)
        ABCMeta.__init__(cls, name, bases, attrs)


def qt_font_object(font_name, font_size=None, bold=None, italic=None):
    font = qtg.QFont(font_name)
    if font_size is not None:
        font.setPointSize(font_size)
    if bold is not None:
        font.setBold(bold)
    if italic is not None:
        font.setItalic(italic)
    return font


class PQtWidget(PQtSignal, metaclass=PQtWidgetMeta):
    """Base class for common Qt widget methods.
    """
    
    fn_enable_get = 'isEnabled'
    fn_enable_set = 'setEnabled'
    
    fix_width_on_resize = False
    fix_height_on_resize = False
    
    def update_widget(self):
        self.update()
    
    def preferred_width(self):
        return max(self.minimumSize().width(), self.sizeHint().width())
    
    def preferred_height(self):
        return max(self.minimumSize().height(), self.sizeHint().height())
    
    def get_width(self):
        return self.width()
    
    def get_height(self):
        return self.height()
    
    def set_size(self, width, height):
        self.resize(width, height)
    
    def get_left(self):
        return self.x()
    
    def get_top(self):
        return self.y()
    
    def set_position(self, left, top):
        self.move(left, top)
    
    def set_min_size(self, width, height):
        self.setMinimumSize(width, height)
    
    def set_min_width(self, width):
        self.setMinimumWidth(width)
    
    def set_min_height(self, height):
        self.setMinimumHeight(height)
    
    def fix_width(self, width):
        self.setMinimumWidth(width)
    
    def fix_height(self, height):
        self.setMinimumHeight(height)
    
    def set_width(self, width):
        super(PQtWidget, self).set_width(width)
        if self.fix_width_on_resize:
            self.fix_width(width)
    
    def set_height(self, height):
        super(PQtWidget, self).set_height(width)
        if self.fix_height_on_resize:
            self.fix_height(height)
    
    def _mapped_color(self, color):
        if isinstance(color, qtg.QColor):
            return color
        return color_map[color]
    
    def set_colors(self, fg=None, bg=None):
        palette = qtg.QPalette(self.palette())
        if fg is not None:
            palette.setColor(self.foregroundRole(), self._mapped_color(fg))
        if bg is not None:
            self.setAutoFillBackground(True)
            palette.setColor(self.backgroundRole(), self._mapped_color(bg))
        self.setPalette(palette)
    
    def set_foreground_color(self, color):
        self.set_colors(fg=color)
    
    def set_background_color(self, color):
        self.set_colors(bg=color)
    
    def get_font_name(self):
        return self.font().family()
    
    def get_font_size(self):
        return self.font().pointSize()
    
    def get_font_bold(self):
        return self.font().bold()
    
    def get_font_italic(self):
        return self.font().italic()
    
    def set_font_object(self, font_name, font_size, bold, italic):
        self.setFont(qt_font_object(font_name, font_size, bold, italic))
    
    def set_focus(self):
        self.setFocus()


class PQtSequenceWidget(PQtWidget, metaclass=PQtSequenceWidgetMeta):
    """Base class for widgets that also appear as sequences.
    """
    pass


class PQtMessageBox(PMessageBoxBase):
    """Customized Qt message box.
    """
    
    question_map = {
        ANSWER_YES: qt.QMessageBox.Yes,
        ANSWER_NO: qt.QMessageBox.No,
        ANSWER_CANCEL: qt.QMessageBox.Cancel,
        ANSWER_OK: qt.QMessageBox.Ok
    }
    
    def message_box(self, type, caption, text, default,
                    button1, button2=None, button3=None):
        
        buttons = button1
        if button2 is not None:
            buttons |= button2
            if button3 is not None:
                buttons |= button3
        
        return message_funcs[type](self.parent, caption, text,
                                   buttons, default)
    
    value_fn_map = {
        str: qt.QInputDialog.getText,
        int: qt.QInputDialog.getInt,
    }
    
    def enter_value(self, value_type, caption, prompt):
        f = self.value_fn_map.get(value_type)
        if not f:
            raise ValueError("Unsupported value type: {}".format(value_type))
        result, accepted = f(self.parent, caption, prompt)
        if accepted:
            return result


class PQtFileDialog(PFileDialogBase):
    
    def choose_directory(self, curdir):
        return str(qt.QFileDialog.getExistingDirectory(
            self.parent, "Select Folder", curdir
        ))
    
    def _translate_filter_item(self, caption, ext_str):
        return "{} ({})".format(caption, ext_str)
    
    ext_sep = " "
    filter_sep = ";;"
    
    def _open_filename(self, path, filter, selected_filter):
        return qt.QFileDialog.getOpenFileName(self.parent, "Open",
                                              path, filter, selected_filter)[0]
    
    def _save_filename(self, path, filter, selected_filter):
        return qt.QFileDialog.getSaveFileName(self.parent, "Save",
                                              path, filter, selected_filter)[0]


class PQtAboutDialog(PAboutDialogBase):
    
    display_func = qt.QMessageBox.about


class PQtProgressDialog(PProgressDialogBase):
    
    def create_dialog(self, title, msg, max_num, stop_label, main_window):
        dlg = qt.QProgressDialog(msg, stop_label, 0, max_num, main_window)
        dlg.setWindowTitle(title)
        dlg.resize(len(title) * 14, dlg.height())  # kludge since qt doesn't automatically resize to the title
        dlg.setMinimumDuration(0)
        dlg.setWindowModality(qtc.Qt.WindowModal)
        return dlg
    
    def show_dialog(self):
        self.dialog.show()
        self.parent.app.processEvents()
    
    def was_canceled(self):
        return self.dialog.wasCanceled()
    
    def update_progress(self, num):
        self.dialog.setValue(num)
        self.parent.app.processEvents()
    
    def complete(self):
        self.dialog.close()
        self.parent.app.processEvents()
    
    def close_dialog(self):
        self.dialog.close()


class PTopWindow(PQtWidget, qt.QMainWindow, PTopWindowBase):
    """Customized Qt top window class.
    """
    
    event_signals = (SIGNAL_QUERYCLOSE, SIGNAL_CLOSING, SIGNAL_SHOWN, SIGNAL_HIDDEN)
    
    def __init__(self, manager):
        qt.QMainWindow.__init__(self)
        PTopWindowBase.__init__(self, manager)
        self._show_state = False  # to avoid multiple firings of shown/hidden events
    
    def set_client_widget(self, client_widget):
        PTopWindowBase.set_client_widget(self, client_widget)
        self.setCentralWidget(client_widget)
    
    def set_caption(self, caption):
        self.setWindowTitle(caption)
    
    def get_desktop_rect(self, primary=True):
        # Correctly handle virtual desktop across multiple screens
        desktop = self.app.desktop()
        l = desktop.x()
        t = desktop.y()
        w = desktop.width()
        h = desktop.height()
        if desktop.isVirtualDesktop() and primary:
            # Default to centering on the primary screen
            i = desktop.primaryScreen()
            n = desktop.numScreens()
            w = w / n
            # NOTE: We have to check for i > 0 here because in some
            # cases (e.g., when running in a VirtualBox), Qt thinks
            # the desktop is "virtual" but there's only one screen and
            # desktop.primaryScreen returns 0 instead of 1.
            if i > 0:
                l += w * (i - 1)
        else:
            i = 0
            n = 1
        return l, t, w, h
    
    def size_maximize(self):
        if self.shown:
            self.showMaximized()
        else:
            self._showMax = True
    
    def get_frame_size(self):
        return self.frameGeometry().width(), self.frameGeometry().height()
    
    def show_init(self):
        PTopWindowBase.show_init(self)
        if hasattr(self, '_showMax'):
            self.showMaximized()
            del self._showMax
        else:
            qt.QMainWindow.show(self)
    
    def do_exit(self):
        self.close()
    
    def closeEvent(self, event):
        self.do_notify(SIGNAL_QUERYCLOSE)  # a handler here can adjust state to be checked below
        
        # Note that Qt signals/slots are by default synchronous (and we don't use queued connections),
        # so ``do_notify`` will cause all handlers to execute before it returns
        if self.can_close():
            self.do_notify(SIGNAL_CLOSING)
            event.accept()
        else:
            event.ignore()
    
    def showEvent(self, event):
        if not self._show_state:
            self.do_notify(SIGNAL_SHOWN)
            self._show_state = True
    
    def hideEvent(self, event):
        if self._show_state:
            self.do_notify(SIGNAL_HIDDEN)
            self._show_state = False
    
    def set_iconfile(self, iconfile):
        self.setWindowIcon(qtg.QIcon(qtg.QPixmap(iconfile)))
    
    def get_current_geometry(self):
        p = self.pos()
        s = self.size()
        return p.x(), p.y(), s.width(), s.height()


QtAppMeta = type(qt.QApplication)


class PQtAppMeta(QtAppMeta):
    # Metaclass for application object
    
    def __new__(meta, name, bases, attrs):
        setup_event_signals(attrs, 'signals')
        return super(PQtAppMeta, meta).__new__(meta, name, bases, attrs)


class PApplication(PQtSignal, qt.QApplication, PApplicationBase,
                   metaclass=PQtAppMeta):
    """Customized Qt application class.
    """
    
    about_dialog_class = PQtAboutDialog
    message_box_class = PQtMessageBox
    file_dialog_class = PQtFileDialog
    progress_dialog_class = PQtProgressDialog
    
    def __init__(self, arglist=[]):
        PApplicationBase.__init__(self, arglist)
        qt.QApplication.__init__(self, arglist)
        
        self.do_create()  # Qt allows widget creation in constructor
        
        self.about_toolkit_func = self.aboutQt
    
    def setup_signals(self):
        # 'automagic' signal connection
        self.setup_notify(SIGNAL_BEFOREQUIT, self.before_quit)
        
        PApplicationBase.setup_signals(self)
    
    def event_loop(self):
        self.exec_()
    
    def process_events(self):
        self.processEvents()
