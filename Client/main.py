import sys
from PyQt5.QtWidgets import QApplication, QDialog
from Client.UploadDlg import UploadDlg

app = QApplication(sys.argv)
window = UploadDlg()

window.show()
sys.exit(app.exec_())