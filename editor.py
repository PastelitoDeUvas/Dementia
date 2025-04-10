import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QFont, QColor, QKeyEvent
from moni_r_lexer import MoniRLexer
from editor_widget import MoniEditorWidget
from PyQt5.QtCore import Qt


class MoniREditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoniEditor para R")
        self.setGeometry(100, 100, 800, 600)

        self.editor = MoniEditorWidget()
        self.editor.setLexer(MoniRLexer(self.editor))

        self.setCentralWidget(self.editor)

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")

        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", filter="Archivos R (*.R *.r)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setText(f.read())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", filter="Archivos R (*.R *.r)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoniREditor()
    window.show()
    sys.exit(app.exec_())
    
