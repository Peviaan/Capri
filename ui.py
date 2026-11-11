import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QLineEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from brain import processar_mensagem

class BrainThread(QThread):
    """Roda o processamento do Ollama em segundo plano para não travar a janela"""
    resposta_pronta = pyqtSignal(str)

    def __init__(self, mensagem_usuario):
        super().__init__()
        self.mensagem_usuario = mensagem_usuario

    def run(self):
        resposta = processar_mensagem(self.mensagem_usuario)
        self.resposta_pronta.emit(resposta)


class CapriUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #config
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Capri OS // Link Neural")
        self.resize(380, 420)

        #cabeçalho status
        self.label_status = QLabel("[ CAPRI_OS V1.0 ]\nStatus: Ociosa", self)
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #histórico leitura
        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        self.chat_area.append("<b>Capri ></b> Link neural ativo. Eai oq que vamos rodar hj?<br>") 

        #campo pra digitar
        self.input_campo = QLineEdit(self)
        self.input_campo.setPlaceholderText("Digite um comando ou mensagem e aperte Enter")
        self.input_campo.returnPressed.connect(self.enviar_mensagem)

        #estilo cyberpunk
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0f;
                color: #00FF41;
                font-family: Consolas, monospace;
            }
            QLabel {
                font-size: 13px;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #00FF41;
                background-color: #12121a;
            }
            QTextEdit {
                background-color: #0d0d14;
                color: #e0e0e0;
                border: 1px solid #1f1f2e;
                font-size: 13px;
                padding: 8px;
            }
            QLineEdit {
                background-color: #12121a;
                color: #00FF41;
                border: 1px solid #00FF41;
                padding: 8px;
                font-size: 13px;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label_status)
        layout.addWidget(self.chat_area)
        layout.addWidget(self.input_campo)
        self.setLayout(layout)

    def enviar_mensagem(self):
        texto = self.input_campo.text().strip()
        if not texto:
            return

        #fala na tela
        self.chat_area.append(f"<span style='color: #00d9ff;'><b>Você ></b></span> {texto}")
        self.input_campo.clear()
        self.input_campo.setDisabled(True)

        #mostra oq ela ta pensando
        self.label_status.setText("[ CAPRI_OS V1.0 ] - Status: Processando...")
        self.label_status.setStyleSheet("color: #ff0055; border: 1px solid #ff0055; background-color: #12121a;")

        # Inicia a Thread do cérebro
        self.thread = BrainThread(texto)
        self.thread.resposta_pronta.connect(self.exibir_resposta)
        self.thread.start()

    def exibir_resposta(self, resposta):
        # Exibe a resposta da Capri e restaura o status para Ociosa
        self.chat_area.append(f"<span style='color: #00FF41;'><b>Capri ></b></span> {resposta}<br>")
        
        self.label_status.setText("[ CAPRI_OS V1.0 ] - Status: Ociosa")
        self.label_status.setStyleSheet("color: #00FF41; border: 1px solid #00FF41; background-color: #12121a;")
        
        self.input_campo.setDisabled(False)
        self.input_campo.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = CapriUI()
    janela.show()
    sys.exit(app.exec())