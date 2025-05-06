import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction,QInputDialog,QMessageBox

from PyQt5.QtGui import QFont
from moni_r_lexer import Moni_R_Lexer,Moni_Python_Lexter
from editor_widget import MoniEditorWidget



class MoniREditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoniEditor para R")
        self.setGeometry(100, 100, 800, 600)

        self.editor = MoniEditorWidget()
        self.editor.setFont(QFont("Fira Code", 11))
        self.editor.setMarginsFont(QFont("Fira Code", 11))

        self.setCentralWidget(self.editor)
        self.lenguaje_actual = "Plain text"
        self.highlighter = None

        self._create_menu()  



    def _create_menu(self):     
        # Principal menu bar
        menubar = self.menuBar()


        # File menu
        file_menu = menubar.addMenu("Archivo")
        file_menu.setStyleSheet("background-color: #B8A9D4; color: #2e2e2e;")  # Pastel purple background for the menu
        file_menu.setFont(QFont("Fira Code", 11))


        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(self.new_File)
        file_menu.addAction(new_action)

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

    def new_File(self):
        lenguajes = ["Python", "R", "Plain text"]
        lenguaje, ok = QInputDialog.getItem(
            self, "Selecciona el lenguaje", "Lenguaje:", lenguajes, 0, False
        )

        if ok and lenguaje:
            self.lenguaje_actual = lenguaje
            self.editor.clear()
            

            # Aplicar resaltador
            if self.highlighter:
                self.highlighter.setDocument(None)  # Desactivar el anterior

            if lenguaje == "Python":
                self.highlighter = Moni_Python_Lexter(self.editor)
                
                self.editor.setLexer(self.highlighter)
            else:
                self.highlighter = None  # Desactivar resaltador para otros lenguajes




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoniREditor()
    window.show()
    sys.exit(app.exec_())
    
