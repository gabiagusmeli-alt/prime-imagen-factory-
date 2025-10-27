import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QScrollArea, QTextEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal

# Importa tyyyu backend con la función main()
from back.python.main import *

# --- CLASE WORKER ---
# Esta clase hará el trabajo pesado en un hilo separado

class Worker(QObject):
    """
    Worker que se mueve a un hilo secundario para ejecutar tareas
    que consumen mucho tiempo.
    """
    # Señal que emite el resultado (un objeto, en tu caso el número)
    finished = pyqtSignal(object)
    # Señal que emite un mensaje de error (string)
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """
        Esta es la función que se ejecutará en el hilo secundario.
        Llama a tu función main() del backend.
        """
        try:
            # Llamada a tu función de backend
            result = main(self.file_path)
            # Emite la señal de finalizado con el resultado
            self.finished.emit(result)
        except Exception as e:
            # Emite la señal de error si algo falla
            self.error.emit(str(e))


# --- VENTANA PRINCIPAL ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Procesador de Imágenes - PyQt6 Front")
        self.setMinimumSize(800, 1100)

        # --- Widgets principales ---
        self.image_label = QLabel("No se ha seleccionado una imagen")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; padding: 20px;")

        self.button_select = QPushButton("Elegir Imagen")
        self.button_select.clicked.connect(self.choose_image)

        self.result_label = QLabel("Resultado del procesamiento:")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        
        self.text_output = QTextEdit()
        self.text_output.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
        self.text_output.setLineWrapColumnOrWidth(50)
        self.text_output.setReadOnly(True)
        self.text_output.setStyleSheet("font-family: 'Arial Black'; font-size: 11pt;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.text_output)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.button_select)
        layout.addWidget(self.result_label)
        layout.addWidget(scroll)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Referencias para que el hilo y el worker no sean eliminados
        # por el recolector de basura
        self.thread = None
        self.worker = None

    # --- Lógica ---

    def choose_image(self):
        """
        Abre el diálogo para seleccionar imagen e inicia el
        procesamiento en un hilo separado.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            self.display_image(file_path)

            # --- Inicio del procesamiento en hilo ---
            
            # 1. Deshabilitar botón y mostrar mensaje
            self.button_select.setEnabled(False)
            self.text_output.setPlainText("Procesando, por favor espere...")

            # 2. Crear el Hilo (QThread) y el Worker
            self.thread = QThread()
            self.worker = Worker(file_path)

            # 3. Mover el worker al hilo
            self.worker.moveToThread(self.thread)

            # 4. Conectar señales y slots
            # Cuando el hilo arranca, ejecuta la función run() del worker
            self.thread.started.connect(self.worker.run)

            # Cuando el worker emite 'finished', llamamos a 'display_result'
            self.worker.finished.connect(self.display_result)
            
            # Cuando el worker emite 'error', llamamos a 'display_error'
            self.worker.error.connect(self.display_error)

            # Limpieza: Cuando el worker termine, le decimos al hilo que pare
            self.worker.finished.connect(self.thread.quit)
            # Limpieza: Marcamos ambos para ser borrados
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # 5. Iniciar el hilo
            # Esto NO bloquea la GUI
            self.thread.start()

    def display_image(self, path):
        pixmap = QPixmap(path)
        pixmap = pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def display_result(self, number):
        """
        Slot: Se activa cuando el worker emite la señal 'finished'.
        Recibe el resultado y lo muestra.
        """
        text = str(number)
        # Lo cortamos cada 50 caracteres
        lines = [text[i:i + 50] for i in range(0, len(text), 50)]
        formatted = "\n".join(lines)
        
        self.text_output.setPlainText(formatted)
        
        # Reactivamos el botón
        self.button_select.setEnabled(True)

    def display_error(self, error_message):
        """
        Slot: Se activa cuando el worker emite la señal 'error'.
        Muestra el error en la GUI.
        """
        self.text_output.setPlainText(f"Error al procesar:\n{error_message}")
        # Reactivamos el botón
        self.button_select.setEnabled(True)


# --- EJECUCIÓN ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())