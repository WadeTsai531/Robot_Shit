from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(640, 480)
        self.frame = QtWidgets.QFrame(Frame)
        self.frame.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(Frame)
        self.pushButton.setGeometry(QtCore.QRect(340, 430, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.timeEdit = QtWidgets.QTimeEdit(Frame)
        self.timeEdit.setGeometry(QtCore.QRect(40, 440, 118, 22))
        self.timeEdit.setObjectName("timeEdit")

        self.image = QtGui.QPixmap('hand 5.png')
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(self.image)
        self.label.setGeometry(QtCore.QRect(10, 10, 320, 320))

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.pushButton.setText(_translate("Frame", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
