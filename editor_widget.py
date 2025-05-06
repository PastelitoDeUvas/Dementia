from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QFont, QColor, QKeyEvent
from PyQt5.QtCore import Qt

import re

class MoniEditorWidget(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFont(QFont("Fira Code", 11))
        self.setMarginsFont(QFont("Fira Code", 11))
        self.setMarginWidth(0, "00000")

        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Set the background color for the text area (where you're typing)
        self.setPaper(QColor("#F4C7D2"))  # Set pastel pink background for the text area
        
        # Set the text color (foreground color for the code)
        self.setColor(QColor("#2e2e2e"))  # Set the text color to a dark gray for the code



        # Set the margins' background color
        self.setMarginsBackgroundColor(QColor("#B8A9D4"))  # Pastel purple for the margin area
        self.setMarginsForegroundColor(QColor("#B8A9D4")) # Pastel purple for the margin text


        self.pairs = {
            '"': '"',
            "'": "'",
            '(': ')',
            '[': ']',
            '{': '}'
        }

    def keyPressEvent(self, event: QKeyEvent):
        key = event.text()
        cursor = self.getCursorPosition()
    
        # Autopareado de símbolos
        if key in self.pairs:
            selected_text = self.selectedText()
            if selected_text:
                self.replaceSelectedText(f"{key}{selected_text}{self.pairs[key]}")
                return
            else:
                self.insert(key + self.pairs[key])
                self.setCursorPosition(cursor[0], cursor[1] + 1)
                return
    
        # Indentación automática al presionar Enter
        if event.key() == Qt.Key_Return:
            line, index = self.getCursorPosition()
    
            # Obtener línea anterior
            prev_line = self.text(line - 1) if line > 0 else ""
    
            # Detectar espacios al inicio
            indent_match = re.match(r'^(\s*)', prev_line)
            current_indent = indent_match.group(1) if indent_match else ""
            new_indent = current_indent
    
            # Agregar indentación si termina en {
            if re.search(r'\{\s*(#.*)?$', prev_line.strip()):
                new_indent += ' ' * self.tabWidth()
    
            super().keyPressEvent(event)  # hacer salto de línea
            self.insert(new_indent)       # insertar indentación
            return
    
        # Comportamiento normal
        super().keyPressEvent(event)