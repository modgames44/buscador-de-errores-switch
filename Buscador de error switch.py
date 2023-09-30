import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QComboBox, QTextBrowser
from PyQt5.QtGui import QFont

import sqlite3

class ErrorLookupApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Buscador de errores NSwitch")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Cambiar el tamaño de la fuente en toda la interfaz
        font = QFont()
        font.setPointSizeF(font.pointSizeF() * 1.1)

        # Apartado central con "Código de error" y botón de búsqueda
        central_layout = QVBoxLayout()
        code_layout = QHBoxLayout()
        self.label = QLabel("Código de error:", central_widget)
        self.label.setFont(font)
        code_layout.addWidget(self.label)
        self.entry = QLineEdit(central_widget)
        self.entry.setFont(font)
        code_layout.addWidget(self.entry)
        central_layout.addLayout(code_layout)
        
        search_clear_layout = QHBoxLayout()
        self.button = QPushButton("Buscar", central_widget)
        self.button.clicked.connect(self.buscar_error)
        self.button.setFont(font)
        search_clear_layout.addWidget(self.button)
        self.clear_button = QPushButton("Limpiar", central_widget)
        self.clear_button.clicked.connect(self.limpiar_descripcion)
        self.clear_button.setFont(font)
        search_clear_layout.addWidget(self.clear_button)
        central_layout.addLayout(search_clear_layout)
        layout.addLayout(central_layout)

        # Pestaña para seleccionar el código de error desde la base de datos
        tab_widget = QTabWidget(central_widget)
        layout.addWidget(tab_widget)

        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        self.error_combobox = QComboBox(tab)
        self.error_combobox.setFont(font)
        tab_layout.addWidget(self.error_combobox)
        self.load_errors()
        self.error_combobox.currentIndexChanged.connect(self.mostrar_descripcion_error)
        self.result_label = QTextBrowser(tab)
        self.result_label.setFont(font)
        tab_layout.addWidget(self.result_label)
        tab_widget.addTab(tab, "Errores en DB")

        # Botón de Cerrar
        close_button = QPushButton("Cerrar", central_widget)
        close_button.clicked.connect(self.close)
        close_button.setFont(font)
        layout.addWidget(close_button)

        central_widget.setLayout(layout)

    def load_errors(self):
        conn = sqlite3.connect('errores.db')
        cursor = conn.cursor()
        cursor.execute('SELECT codigo FROM errores')
        resultados = cursor.fetchall()
        conn.close()
        for resultado in resultados:
            self.error_combobox.addItem(resultado[0])

    def mostrar_descripcion_error(self):
        codigo_seleccionado = self.error_combobox.currentText()
        descripcion_error = self._buscar_error_en_db(codigo_seleccionado)
        self.result_label.setText(descripcion_error)

    def buscar_error(self):
        codigo_buscar = self.entry.text()
        descripcion_error = self._buscar_error_en_db(codigo_buscar)
        self.result_label.setText(descripcion_error)

    def limpiar_descripcion(self):
        self.result_label.clear()

    def _buscar_error_en_db(self, codigo):
        conn = sqlite3.connect('errores.db')
        cursor = conn.cursor()
        cursor.execute('SELECT descripcion FROM errores WHERE codigo = ?', (codigo,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]
        else:
            return "Código de error no encontrado"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ErrorLookupApp()
    window.show()
    sys.exit(app.exec_())
