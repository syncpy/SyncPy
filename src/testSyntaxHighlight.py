# editor.py

from PyQt4 import QtGui
import ui.PythonSyntax

app = QtGui.QApplication([])
editor = QtGui.QPlainTextEdit()
highlight = ui.PythonSyntax.PythonHighlighter(editor.document())
editor.show()

# Load syntax.py into the editor for demo purposes
infile = open('Syncpy2.py', 'r')
editor.setPlainText(infile.read())

app.exec_()