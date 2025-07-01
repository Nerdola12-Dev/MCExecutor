from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QTextEdit, QListWidget, QLabel, QSizePolicy
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import sys
import os
import requests
import json



_p_ = ""

with open(f"config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    
_p_ = config["path"]

class ExecutorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MCExecutor")
        self.setFixedSize(800, 500)  # Tamanho fixo da janela
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon("logo.ico"))

        '''
        # Lista de scripts carregados
        self.script_list = QListWidget()
        self.script_list.setMaximumHeight(30)
        self.script_list.setFlow(QListWidget.Flow.LeftToRight)
        self.script_list.setSpacing(10)
        self.script_list.setStyleSheet("border: none;")
        '''


        # Editor
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 12))
        self.editor.setPlaceholderText("# Write your Python script here...")
        self.editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)  # desabilita quebra de linha automática

        # Botões
        open_btn = QPushButton("📂 Open")
        open_btn.clicked.connect(self.abrir_arquivo)

        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self.salvar_arquivo)

        inject_btn = QPushButton("💉 Inject")
        inject_btn.clicked.connect(self.executar_script)

        # Layout de botões
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(inject_btn)

        # Área da direita (scripts + editor + botões)
        right_layout = QVBoxLayout()
        #right_layout.addWidget(self.script_list)
        right_layout.addWidget(self.editor)
        right_layout.addLayout(btn_layout)

        # Área da esquerda (configurações)
        config_layout = QVBoxLayout()
        config_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        folder_btn = QPushButton("📁 Select World Folder")
        folder_btn.clicked.connect(self.selecionar_pasta)
        config_layout.addWidget(QLabel("Settings"))
        config_layout.addWidget(folder_btn)

        '''
        clear_btn = QPushButton("🧹 Clear Injected Scripts")
        clear_btn.clicked.connect(self.limpar_scripts_injetados)
        config_layout.addWidget(clear_btn)
        '''


        config_widget = QWidget()
        config_widget.setLayout(config_layout)
        config_widget.setMaximumWidth(200)

        # Layout principal horizontal
        main_layout = QHBoxLayout()
        main_layout.addWidget(config_widget)
        main_layout.addLayout(right_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Dentro da classe ExecutorWindow

    def limpar_scripts_injetados(self):
        if not _p_:
            print("No world folder selected.")
            return

        datapacks_dir = os.path.join(_p_, "datapacks")
        if not os.path.exists(datapacks_dir):
            print("No datapacks folder found.")
            return

        for nome_pasta in os.listdir(datapacks_dir):
            caminho_pasta = os.path.join(datapacks_dir, nome_pasta)
            pack_path = os.path.join(caminho_pasta, "pack.mcmeta")

            if not os.path.isfile(pack_path):
                continue

            try:
                with open(pack_path, "r", encoding="utf-8") as f:
                    import json
                    pack_data = json.load(f)
                    if pack_data.get("script", False) is True:
                        import shutil
                        shutil.rmtree(caminho_pasta)
                        print(f"[Deleted Script Datapack] {nome_pasta}")
            except Exception as e:
                print(f"[Error deleting '{nome_pasta}']: {e}")

    def executar_script(self):

        def loadstring(url: str):
            response = requests.get(url)
            if response.status_code == 200:
                code = response.text
                exec(code, globals())  # executa o código no escopo global
            else:
                raise Exception(f"Err: {response.status_code}")

        try:

            codigo = self.editor.toPlainText()
            exec(codigo + f"\nMCData.inject(r\"{_p_}\\datapacks\")\nMCData.path = \"{_p_}\"")

        except Exception as e:
            print("Execution error:", e)

    def abrir_arquivo(self):
        nome_arquivo, _ = QFileDialog.getOpenFileName(self, "Open script", "", "Python (*.py)")
        if nome_arquivo:
            with open(nome_arquivo, "r", encoding="utf-8") as file:
                self.editor.setPlainText(file.read())
            nome = os.path.basename(nome_arquivo)
            if nome not in [self.script_list.item(i).text() for i in range(self.script_list.count())]:
                self.script_list.addItem(nome)

    def salvar_arquivo(self):
        nome_arquivo, _ = QFileDialog.getSaveFileName(self, "Save script", "", "Python (*.py)")
        if nome_arquivo:
            with open(nome_arquivo, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())

    def selecionar_pasta(self):
        global _p_
        folder = QFileDialog.getExistingDirectory(self, "Select World Folder")
        if folder:
            print("World folder selected:", folder)
            _p_ = folder

            config = {
                "path": _p_
            }

            with open("config.json", "w", encoding="utf-8") as file:
                json.dump(config, file, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExecutorWindow()
    window.show()
    sys.exit(app.exec())
