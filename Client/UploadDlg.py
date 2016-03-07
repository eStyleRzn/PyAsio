import os
import asyncio
import sys
from pathlib import Path
from classes.ClientTransceiver import ClientTransceiver
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from Client.Ui_UploadDlg import Ui_UploadDlg

# ======================================================================================================================
class UploadDlg(QDialog):
    def __init__(self):
        super(UploadDlg, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_UploadDlg()
        self.ui.setupUi(self)

        # Connect up the buttons.
        self.ui.btnSelect.clicked.connect(self.__file_select)
        self.ui.btnStart.clicked.connect(self.__start)

    def __file_select(self):
        file_name = QFileDialog.getOpenFileName()

        if len(file_name):
             self.ui.lblSelectFile.setText(file_name[0])

    def __start(self):
        server_name = self.ui.editServerAddress.text()
        file_path = self.ui.lblSelectFile.text()  # 'c:/Temp/Oleg/Python/python-3.5.1-amd64.exe'

        path_obj = Path(file_path)

        # Validate mandatory parameters
        if path_obj.exists() and len(server_name):
            # Before we start new import session reset the progress
            self.ui.progressBar.setFormat('')
            self.ui.progressBar.setValue(0)
            self.ui.progressBar.setMaximum(os.path.getsize(file_path))

            try:
                self.__start_loop(server_name, file_path)

                # Finished or not
                if self.ui.progressBar.maximum() == self.ui.progressBar.value():
                    self.ui.progressBar.setValue(0)
                    self.ui.progressBar.setFormat('The file was successfully uploaded!!!')
            except:
                QMessageBox.critical(self, 'Error', 'Error uploading the file! {!r}'.format(sys.exc_info()))

    def progress_callback(self, val):
        # increment the progress
        self.ui.progressBar.setValue(self.ui.progressBar.value() + val)

    def __start_loop(self, server_name, file_path):
        event_loop = asyncio.new_event_loop()
        data_exchange = event_loop.create_connection(lambda: ClientTransceiver(file_path,
                                                                               event_loop,
                                                                               self.progress_callback),
                                                     server_name, 8888)
        event_loop.run_until_complete(data_exchange)
        event_loop.run_forever()
        event_loop.close()
