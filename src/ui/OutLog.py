from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# Class to redirect std output to a widget
class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = out
        self.color = color

    def write(self, m):

        if self.color:
            prevColor = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.insertPlainText(_fromUtf8(m))

        if self.color:
            self.edit.moveCursor(QtGui.QTextCursor.End)
            self.edit.setTextColor(prevColor)

        if self.out:
            self.out.write(m)

    def flush(self):
        if self.out:
            self.out.flush()

