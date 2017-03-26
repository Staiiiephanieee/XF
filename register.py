import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMessageBox, QApplication, QPushButton, QDialog
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication)
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp



class Register(QDialog):
    def __init__(self, parent=None):
        super(Register, self).__init__(parent)

        self.initUI()

    def initUI(self):
        phonenumber = QLabel('Phone number')
        username = QLabel('username')
        password = QLabel('Password')
        self.tips = QLabel('')

        self.phonenumberEdit = QLineEdit()

       # self.phonenumberEdit.setMaxLength(13)
        #regx=QRegExp("1[0-9]+$")
        #validator = QRegExpValidator(regx, self.phonenumberEdit)
        #self.phonenumberEdit.setValidator(validator)
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.btn1 = QPushButton("OK", self)
        self.btn2 = QPushButton("Cancel", self)

        grid = QGridLayout()
        grid.setSpacing(5)

        # grid.addWidget(title, 1, 1)

        grid.addWidget(phonenumber, 2, 0)
        grid.addWidget(self.phonenumberEdit, 2, 1)

        grid.addWidget(username, 3, 0)
        grid.addWidget(self.usernameEdit, 3, 1)

        grid.addWidget(password, 4, 0)
        grid.addWidget(self.passwordEdit, 4, 1)

        grid.addWidget(self.btn1, 5, 3)
        grid.addWidget(self.btn2, 5, 2)
        grid.addWidget(self.tips, 5, 1)

        self.setLayout(grid)
        self.resize(400, 300)
        self.setWindowTitle('Register')

        self.btn1.clicked.connect(self.btn1Clicked)
        self.btn2.clicked.connect(self.btn2Clicked)
        self.phonenumberEdit.textChanged.connect(self.checkInput)

    def btn1Clicked(self):
        if self.phonenumberEdit.text() == "":
            QMessageBox.about(None, "Tip", "The phonenumber has to be filled")
            return
        conn = sqlite3.connect("XF.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT count(*) from user where phonenumber="%s"''' % (self.phonenumberEdit.text()))
        total = cursor.fetchone()
        if total[0] <= 0:
            try:
                conn.execute("INSERT INTO user(phonenumber, username, password) VALUES(%s, '%s', '%s')"
                         % (self.phonenumberEdit.text(), self.usernameEdit.text(), self.passwordEdit.text()))
                conn.commit()
                self.accept()
            except sqlite3.IntegrityError:
                QMessageBox.about(None, "Tip", "The username has already existed")
        else:
            QMessageBox.about(None, "Tip", "The account has already existed")

    def btn2Clicked(self):
        self.reject()

    def checkInput(self):
        if len(self.phonenumberEdit.text())!=11 or self.phonenumberEdit.text().isdigit()==False:
            self.tips.setText('Your enter is invalid for phone number')
        else:
            self.tips.setText('')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Register()
    ex.show()
    sys.exit(app.exec_())