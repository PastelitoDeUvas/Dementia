import os
import sys
import subprocess
import tempfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, \
                            QInputDialog, QMessageBox
from PyQt5.QtGui import QFont
from moni_r_lexer import Moni_R_Lexer, Moni_Python_Lexter
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

    # ---------- MENÚ ----------
    def _create_menu(self):
        menubar = self.menuBar()

        # Archivo
        file_menu = menubar.addMenu("Archivo")
        file_menu.setStyleSheet(
            "background-color: #B8A9D4; color: #2e2e2e;")
        file_menu.setFont(QFont("Fira Code", 11))

        actions = [
            ("Nuevo", self.new_File),
            ("Abrir", self.open_file),
            ("Guardar", self.save_file),
            ("Ejecutar código R", self.run_r_code),
        ]
        for text, slot in actions:
            act = QAction(text, self)
            act.triggered.connect(slot)
            file_menu.addAction(act)

    # ---------- I/O ----------
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", filter="Archivos R (*.R *.r)")
        if path:
            with open(path, encoding="utf-8") as f:
                self.editor.setText(f.read())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", filter="Archivos R (*.R *.r)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.text())

    # ---------- NUEVO ----------
    def new_File(self):
        lenguajes = ["Python", "R", "Plain text"]
        lenguaje, ok = QInputDialog.getItem(
            self, "Selecciona el lenguaje", "Lenguaje:", lenguajes, 0, False)

        if ok and lenguaje:
            self.lenguaje_actual = lenguaje
            self.editor.clear()

            # Desvincular resaltador anterior
            if self.highlighter:
                self.highlighter.setDocument(None)

            if lenguaje == "Python":
                self.highlighter = Moni_Python_Lexter(self.editor)
                self.editor.setLexer(self.highlighter)
            elif lenguaje == "R":
                self.highlighter = Moni_R_Lexer(self.editor)
                self.editor.setLexer(self.highlighter)
            else:
                self.highlighter = None  # Sin resaltado

    # ---------- EJECUTAR R ----------
    def run_r_code(self):
        if self.lenguaje_actual != "R":
            QMessageBox.warning(
                self, "Lenguaje incorrecto",
                "El documento actual no está marcado como R.")
            return

        # 1. Obtener código
        codigo = self.editor.text()
        if not codigo.strip():
            QMessageBox.information(
                self, "Nada que ejecutar",
                "El código R está vacío, princesa.")
            return

        # 2. Crear archivo temporal
        with tempfile.NamedTemporaryFile(
                mode='w', suffix=".R", delete=False, encoding='utf-8') as tmp:
            tmp.write(codigo)
            tmp_path = tmp.name

        # 3. Ejecutar con Rscript
        try:
            result = subprocess.run(
                ["Rscript", tmp_path],
                capture_output=True, text=True, timeout=600)

            salida = result.stdout.strip()
            error = result.stderr.strip()

            if result.returncode == 0:
                QMessageBox.information(
                    self, "Ejecución correcta",
                    f"⚜️ Tu código R se ejecutó sin problemas, princesa:\n\n{salida or '(Sin salida)'}")
            else:
                QMessageBox.critical(
                    self, "Error al ejecutar R",
                    f"Hubo un problema, mi señora:\n\n{error or '(Sin detalles)'}")

        except FileNotFoundError:
            QMessageBox.critical(
                self, "Rscript no encontrado",
                "No pude encontrar el comando `Rscript`. "
                "Asegúrate de que R esté instalado y su carpeta bin esté en el PATH.")
        except subprocess.TimeoutExpired:
            QMessageBox.critical(
                self, "Ejecución muy larga",
                "El código tardó demasiado. Aborta o revisa tu script.")
        finally:
            # 4. Limpiar archivo temporal
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoniREditor()
    window.show()
    sys.exit(app.exec_())