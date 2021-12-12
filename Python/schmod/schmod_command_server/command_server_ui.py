from os import terminal_size
import sys
from threading import Thread

from schmod.schmod_command_server.command_server import *
from PyQt5 import QtCore, QtGui, QtWidgets

class CommandServerUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CommandServerUI, self).__init__()

        # Class Variables
        self.command_server = CommandServer(False)
        self.server_thread = None
        self.client_list = {}

        # UI
        widgMain = QtWidgets.QWidget()
        self.setCentralWidget(widgMain)
        self.lyo_main = QtWidgets.QVBoxLayout()
        widgMain.setLayout(self.lyo_main)

        self.server_status_timer = QtCore.QTimer()
        self.server_status_timer.timeout.connect(self.on_update_server_status)
        self.server_status_timer.start(1000)

        self.server_client_connections_timer = QtCore.QTimer()
        self.server_client_connections_timer.timeout.connect(self.on_update_client_list)
        self.server_client_connections_timer.start(500)

        self.btn_start_server = None
        self.btn_stop_server = None
        self.lst_client_list = None
        self.cbx_command_type = None
        self.btn_command_send = None
        self.lne_command_input = None

        # Create UI
        self.build_ui()
        self.make_connections()

        # Auto Start
        self.on_start_server()

    def build_ui(self):
        # Create Connection Group
        gbx_grp_connection = QtWidgets.QGroupBox('Connection')
        lyo_grp_connection = QtWidgets.QVBoxLayout(gbx_grp_connection)
        self.lyo_main.addWidget(gbx_grp_connection)

        # Build Connection info layout
        lyo_connection_info = QtWidgets.QHBoxLayout()
        lyo_grp_connection.addLayout(lyo_connection_info)
        
        # Add Connection Info widgets
        lbl_port = QtWidgets.QLabel('Port: ')
        lyo_connection_info.addWidget(lbl_port)
        lne_port = QtWidgets.QLineEdit()
        lne_port.setText(str(self.command_server.PORT))
        lne_port.setEnabled(False)
        lyo_connection_info.addWidget(lne_port)
        self.btn_start_server = QtWidgets.QPushButton('Start Server')
        lyo_connection_info.addWidget(self.btn_start_server)
        self.btn_stop_server = QtWidgets.QPushButton('Stop Server')
        self.btn_stop_server.setVisible(False)
        lyo_connection_info.addWidget(self.btn_stop_server)
        self.lbl_connection_status = QtWidgets.QLabel('Status: Stopped')
        self.lbl_connection_status.setStyleSheet('background-color: red; border: 1px solid black;')
        lyo_connection_info.addWidget(self.lbl_connection_status)

        # Add Client List widget
        self.lst_client_list = QtWidgets.QListWidget()
        lyo_grp_connection.addWidget(self.lst_client_list)

        # Create Command Group
        gbx_grp_command = QtWidgets.QGroupBox('Commands')
        lyo_grp_command = QtWidgets.QVBoxLayout(gbx_grp_command)
        self.lyo_main.addWidget(gbx_grp_command)

        # Create Command Simulate Sections
        lyo_command_simulate = QtWidgets.QHBoxLayout()
        lyo_grp_command.addLayout(lyo_command_simulate)

        self.cbx_command_type = QtWidgets.QComboBox()
        self.cbx_command_type.addItems(['[CLIENT_TYPE]','[COMMAND]','[MESSAGE]','[BROADCAST]','[QUIT]'])
        lyo_command_simulate.addWidget(self.cbx_command_type)
        self.lne_command_input = QtWidgets.QLineEdit()
        lyo_command_simulate.addWidget(self.lne_command_input)
        self.btn_command_send = QtWidgets.QPushButton('Send')
        lyo_command_simulate.addWidget(self.btn_command_send)

    def make_connections(self):
        self.btn_start_server.clicked.connect(self.on_start_server)
        self.btn_stop_server.clicked.connect(self.on_stop_server)
        self.btn_command_send.clicked.connect(self.on_send_message)

    def on_start_server(self):
        if self.command_server and not self.command_server.is_running:
            self.server_thread = threading.Thread(target=self.command_server.start_server).start()

            self.lbl_connection_status.setText('Status: {0}'.format('Running'))
            self.lbl_connection_status.setStyleSheet('background-color: lightgreen; border: 1px solid black;')

            self.btn_start_server.setVisible(False)
            self.btn_stop_server.setVisible(True)

    def on_stop_server(self):
        if self.command_server and self.command_server.is_running:
            self.command_server.close_server()
            self.client_list.clear()
            self.lst_client_list.clear()

            self.lbl_connection_status.setText('Status: {0}'.format('Stopped'))
            self.lbl_connection_status.setStyleSheet('background-color: red; border: 1px solid black;')

            self.btn_start_server.setVisible(True)
            self.btn_stop_server.setVisible(False)

    def on_send_message(self):
        if self.lne_command_input.text() != '':
            msg = self.cbx_command_type.currentText() + ' ' + self.lne_command_input.text()
            self.command_server.interpret_command(msg)

    def on_update_server_status(self):
        if self.command_server.is_running:
            self.lbl_connection_status.setText('Status: {0}'.format('Running'))
            self.lbl_connection_status.setStyleSheet('background-color: lightgreen; border: 1px solid black;')

            self.btn_start_server.setVisible(False)
            self.btn_stop_server.setVisible(True)
        else:
            self.lbl_connection_status.setText('Status: {0}'.format('Stopped'))
            self.lbl_connection_status.setStyleSheet('background-color: red; border: 1px solid black;')

            self.btn_start_server.setVisible(True)
            self.btn_stop_server.setVisible(False)

    def on_update_client_list(self):
        if self.command_server.is_running:
            self.client_list = self.command_server.client_list
            curSel = self.lst_client_list.currentRow()
            
            self.lst_client_list.clear()
            for key, value in self.client_list.items():
                self.lst_client_list.addItem('{0} : {1}'.format(value.client_type, value.socket_address))
            
            if curSel > 0:
                self.lst_client_list.setCurrentRow(curSel)
            else:
                self.lst_client_list.setCurrentRow(0)

    def closeEvent(self, event):
        if self.command_server.is_running:
            self.command_server.close_server()

def open_ui():
    app = QtWidgets.QApplication(sys.argv)
    
    win = CommandServerUI()
    win.setWindowTitle("Schmod Command Server")
    win.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    open_ui()
    