from PyQt5.Qsci import QsciLexerCustom
from PyQt5.QtGui import QColor, QFont,QSyntaxHighlighter, QTextCharFormat
import re
from PyQt5.QtCore import QRegExp

class Moni_R_Lexer(QsciLexerCustom):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDefaultFont(QFont("Fira Code", 11))

        # Estilos personalizados
        self.styles = {
            'default': 0,
            'keyword': 1,
            'comment': 2,
            'string': 3,
            'number': 4,
            'function': 5,
        }

        self._define_styles()

        # Palabras clave básicas de R
        self.keywords = set([
            "if", "else", "for", "while", "function", "return", "break", "next",
            "TRUE", "FALSE", "NULL", "NA", "NaN", "Inf", "in", "repeat", "switch"
        ])

    def _define_styles(self):
        self.setColor(QColor("#cccccc"), self.styles['default'])
        self.setColor(QColor("#ff79c6"), self.styles['keyword'])  # rosado
        self.setColor(QColor("#6272a4"), self.styles['comment'])  # azul gris
        self.setColor(QColor("#f1fa8c"), self.styles['string'])   # amarillo pastel
        self.setColor(QColor("#bd93f9"), self.styles['number'])   # violeta
        self.setColor(QColor("#8be9fd"), self.styles['function']) # cian

        self.setFont(QFont("Fira Code", 11), -1)

    def language(self):
        return "R"

    def description(self, style):
        return {
            0: "Default",
            1: "Keyword",
            2: "Comment",
            3: "String",
            4: "Number",
            5: "Function"
        }.get(style, "")

    def styleText(self, start, end):
        editor = self.editor()
        if not editor:
            return
    
        text = editor.text()[start:end]
        length = len(text)
    
        # Buffer para saber qué estilo aplicar a cada posición
        styles_buffer = [self.styles['default']] * length
    
        def apply_regex(regex, style, condition=None):
            for match in re.finditer(regex, text):
                if condition and not condition(match.group()):
                    continue
                for i in range(match.start(), match.end()):
                    if 0 <= i < length:
                        styles_buffer[i] = style
    
        apply_regex(r"#.*", self.styles['comment'])
        apply_regex(r'"[^"]*"|\'[^\']*\'', self.styles['string'])
        apply_regex(r"\b\d+(\.\d+)?\b", self.styles['number'])
        apply_regex(r"\b[a-zA-Z_]\w*(?=\s*\()", self.styles['function'])
        apply_regex(r"\b[a-zA-Z_]\w*\b", self.styles['keyword'],
                    condition=lambda word: word in self.keywords)
    
        # Aplica los estilos desde el buffer
        self.startStyling(start)
        i = 0
        while i < length:
            current_style = styles_buffer[i]
            count = 1
            while i + count < length and styles_buffer[i + count] == current_style:
                count += 1
            self.setStyling(count, current_style)
            i += count







class Moni_Python_Lexter(QsciLexerCustom):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDefaultFont(QFont("Fira Code", 11))

        # Estilos personalizados
        self.styles = {
            'default': 0,
            'keyword': 1,
            'comment': 2,
            'string': 3,
            'number': 4,
            'function': 5,
            'operator': 6,
            'class': 7,
            'builtin': 8,
        }

        self._define_styles()

        # Palabras clave de Python
        self.keywords = set([
            "False", "None", "True", "and", "as", "assert", "async", "await",
            "break", "class", "continue", "def", "del", "elif", "else", "except",
            "finally", "for", "from", "global", "if", "import", "in", "is",
            "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
            "try", "while", "with", "yield"
        ])

        # Funciones embebidas (built-in)
        self.builtins = set([
            "abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes",
            "callable", "chr", "classmethod", "compile", "complex", "delattr",
            "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
            "float", "format", "frozenset", "getattr", "globals", "hasattr",
            "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass",
            "iter", "len", "list", "locals", "map", "max", "memoryview", "min",
            "next", "object", "oct", "open", "ord", "pow", "print", "property",
            "range", "repr", "reversed", "round", "set", "setattr", "slice",
            "sorted", "staticmethod", "str", "sum", "super", "tuple", "type",
            "vars", "zip"
        ])

    def _define_styles(self):
        self.setColor(QColor("#cccccc"), self.styles['default'])    # gris claro
        self.setColor(QColor("#ff79c6"), self.styles['keyword'])    # rosado
        self.setColor(QColor("#6272a4"), self.styles['comment'])    # azul gris
        self.setColor(QColor("#f1fa8c"), self.styles['string'])     # amarillo pastel
        self.setColor(QColor("#bd93f9"), self.styles['number'])     # violeta
        self.setColor(QColor("#8be9fd"), self.styles['function'])   # cian
        self.setColor(QColor("#ffb86c"), self.styles['operator'])   # naranja pastel
        self.setColor(QColor("#ff5555"), self.styles['class'])      # rojo pastel
        self.setColor(QColor("#caa9fa"), self.styles['builtin'])    # lavanda

        self.setFont(QFont("Fira Code", 11), -1)

    def language(self):
        return "Python"

    def description(self, style):
        return {
            0: "Default",
            1: "Keyword",
            2: "Comment",
            3: "String",
            4: "Number",
            5: "Function",
            6: "Operator",
            7: "Class",
            8: "Builtin Function",
        }.get(style, "")

    def styleText(self, start, end):
        editor = self.editor()
        if not editor:
            return

        text = editor.text()[start:end]
        length = len(text)

        styles_buffer = [self.styles['default']] * length

        def apply_regex(regex, style, condition=None):
            for match in re.finditer(regex, text):
                word = match.group()
                if condition and not condition(word):
                    continue
                for i in range(match.start(), match.end()):
                    if 0 <= i < length:
                        styles_buffer[i] = style

        # Aplicar estilos
        apply_regex(r"#.*", self.styles['comment'])  # Comentarios
        apply_regex(r'"""(?:.|\n)*?"""|\'\'\'(?:.|\n)*?\'\'\'|"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'', self.styles['string'])  # Strings
        apply_regex(r"\b\d+(\.\d+)?\b", self.styles['number'])  # Números
        apply_regex(r"\b[a-zA-Z_]\w*(?=\s*\()", self.styles['function'])  # Funciones
        apply_regex(r"\b[A-Z][a-zA-Z0-9_]*\b", self.styles['class'])  # Clases (CamelCase)
        apply_regex(r"\b[a-zA-Z_]\w*\b", self.styles['keyword'], condition=lambda w: w in self.keywords)  # Palabras clave
        apply_regex(r"\b[a-zA-Z_]\w*\b", self.styles['builtin'], condition=lambda w: w in self.builtins)  # Built-ins
        apply_regex(r"[+\-*/%=<>!&|^~]+", self.styles['operator'])  # Operadores

        # Aplicar estilos
        self.startStyling(start)
        i = 0
        while i < length:
            current_style = styles_buffer[i]
            count = 1
            while i + count < length and styles_buffer[i + count] == current_style:
                count += 1
            self.setStyling(count, current_style)
            i += count