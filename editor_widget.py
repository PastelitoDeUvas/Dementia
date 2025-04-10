from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QFont, QColor, QKeyEvent
from PyQt5.QtCore import Qt

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
        self.setMarginsBackgroundColor(QColor("#2e2e2e"))
        self.setMarginsForegroundColor(QColor("#aaaaaa"))

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

        if key in self.pairs:
            selected_text = self.selectedText()
            if selected_text:
                self.replaceSelectedText(f"{key}{selected_text}{self.pairs[key]}")
                return
            else:
                self.insert(key + self.pairs[key])
                self.setCursorPosition(cursor[0], cursor[1] + 1)
                return

        if event.key() == Qt.Key_Return:
            line, col = self.getCursorPosition()
            if self.text(line).rstrip().endswith('{'):
                super().keyPressEvent(event)
                self.insert("    ")
                return

        super().keyPressEvent(event)