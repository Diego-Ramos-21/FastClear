import os
import sys
import shutil
import getpass
import threading
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QApplication


# Limpar pasta indicada
def _limpar_diretorio(path):
    dir = os.walk(path)
    for directory, subdirectorys, files in dir:
        for subdirectory in subdirectorys[:]:
            print(f"Directory: {directory} \nSubdirectory: {subdirectory}")
            form.lbl_log.addItem(f"Directory: {directory} \nSubdirectory: {subdirectory}")
            subdirectorys.remove(subdirectory)
            shutil.rmtree(os.path.join(directory, subdirectory), True)
            print(fr"{directory}\{subdirectory} FOI REMOVIDO COM SUCESSO!")
            form.lbl_log.addItem(fr"{directory}\{subdirectory} FOI REMOVIDO COM SUCESSO!")
        for file in files:
            print(f"Directory: {directory} \nSubdirectory: {file}")
            form.lbl_log.addItem(f"Directory: {directory} \nSubdirectory: {file}")
            try:
                os.remove(os.path.join(directory, file))
                print(fr"{directory}\{file} FOI REMOVIDO COM SUCESSO!")
                form.lbl_log.addItem(fr"{directory}\{file} FOI REMOVIDO COM SUCESSO!")
            except PermissionError:
                print(fr"{directory}\{file} FALHA AO REMOVER O ARQUIVO!")
                form.lbl_log.addItem(fr"{directory}\{file} FALHA AO REMOVER O ARQUIVO!")
                continue


# Limpeza de temporarias padrão no disco local C
def default_clear():
    origins_path = (
        fr"C:\Users\{getpass.getuser()}\AppData\Local\Temp", r"C:\Windows\Temp", r"C:\Program Files (x86)\Temp"
    )
    for origin_path in origins_path:
        _limpar_diretorio(origin_path)


# interação de clique do Menu
def btn_menu_eventclick():
    ...


def btn_fast_clear_eventclick():
    global form
    form.fast_clear.show()


def btn_home_eventclick():
    global form
    form.fast_clear.hide()


def btn_start_eventclick():
    global exec_clear
    if exec_clear is False:
        form.lbl_log.clear()
        exec_clear = True
        default_clear()
        form.lbl_log.addItem("COMPLETE PROCESS")
        exec_clear = False


def combo_box_eventchange():
    if form.combo_box.currentText() == "default":
        form.txt_path.setDisabled(True)
        form.btn_search_path.setDisabled(True)
        form.btn_start.setDisabled(False)
    else:
        form.txt_path.setDisabled(True)
        form.btn_search_path.setDisabled(True)
        form.btn_start.setDisabled(True)


def btn_exit_eventclick():
    response = QMessageBox.question(
        form,
        "Window close",
        "Are you sure you want to close the window?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    if response == QMessageBox.Yes:
        sys.exit()
    else:
        pass


# Teste de usabilidade
if __name__ == '__main__':
    exec_clear = False

    app = QApplication(sys.argv)
    form = uic.loadUi("../Views/Main.ui")
    # Ação dos componentes
    form.fast_clear.hide()
    form.txt_path.setDisabled(True)
    form.btn_search_path.setDisabled(True)
    form.btn_start.setDisabled(True)

    form.combo_box.addItems(["", "default"])

    form.btn_menu.clicked.connect(btn_menu_eventclick)
    form.btn_fast_clear.clicked.connect(btn_fast_clear_eventclick)
    form.btn_home.clicked.connect(btn_home_eventclick)
    form.combo_box.currentTextChanged.connect(combo_box_eventchange)
    form.btn_start.clicked.connect(lambda: threading.Thread(target=btn_start_eventclick).start())
    form.btn_exit.clicked.connect(btn_exit_eventclick)

    form.show()
    sys.exit(app.exec_())
