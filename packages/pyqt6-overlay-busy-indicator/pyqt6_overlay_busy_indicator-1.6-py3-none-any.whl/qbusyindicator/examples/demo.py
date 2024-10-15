from PyQt6 import QtGui, QtWidgets

from qbusyindicator import QOverlayBusyIndicator


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('PyQt6 Overlay Busy Indicator - Demo')

        vbox_layout = QtWidgets.QVBoxLayout(self)
        start_btn = QtWidgets.QPushButton('Start')
        stop_btn = QtWidgets.QPushButton('Stop')
        line_edit = QtWidgets.QLineEdit(self.tr('Please wait...'))
        line_edit.setPlaceholderText('Input your text here')
        block_keyboard_checkbox = QtWidgets.QCheckBox('Block Keyboard')
        block_mouse_checkbox = QtWidgets.QCheckBox('Block Mouse')
        fade_duration_spn = QtWidgets.QSpinBox()
        fade_duration_spn.setMinimum(0)
        fade_duration_spn.setMaximum(99999)
        fade_duration_spn.setValue(400)
        fade_duration_spn.setPrefix('Fade Duration: ')

        busy_duration_spn = QtWidgets.QSpinBox()
        busy_duration_spn.setMinimum(100)
        busy_duration_spn.setMaximum(999999)
        busy_duration_spn.setValue(5000)
        busy_duration_spn.setPrefix('Busy Duration: ')

        vbox_layout.addWidget(line_edit)
        vbox_layout.addWidget(block_keyboard_checkbox)
        vbox_layout.addWidget(block_mouse_checkbox)
        vbox_layout.addWidget(fade_duration_spn)
        vbox_layout.addWidget(busy_duration_spn)
        spacer = QtWidgets.QSpacerItem(40, 40,
                                       QtWidgets.QSizePolicy.Policy.Expanding,
                                       QtWidgets.QSizePolicy.Policy.Expanding)
        vbox_layout.addItem(spacer)
        vbox_layout.addWidget(start_btn)
        vbox_layout.addWidget(stop_btn)
        self.setLayout(vbox_layout)

        self.busy = QOverlayBusyIndicator(self, image_path='loading.gif')

        # you can also pass parameters while initializing instance
        # e.g. self.busy = QOverlayBusyIndicator(self, label_text='Loading...',
        # image_path=r'd:\\loading.gif', fade_duration=600, block_keyboard=False,
        # block_mouse=False)

        # changing the background of the widget
        # self.busy.setStyleSheet('background-color: rgba(204, 204, 204, 70);')

        # changing the style of the text
        # self.busy.label.setStyleSheet('padding-top: 10px; color: #000;')

        # if you prefer camel case syntax you can use following methods
        self.busy.setImagePath(r'loading.gif') #sets the busy image animation path
        self.busy.setBlockKeyboard(True) #blocks keyboard input while busy
        self.busy.setBlockMouse(True) #blocks mouse input while busy
        self.busy.setFadeDuration(1000) #sets fade in animation duration default is 400 msecs
        self.busy.setLabelFont(QtGui.QFont('Calibri', 20)) #sets the label font
        self.busy.setLabelText(line_edit.text()) #sets the label text

        line_edit.textChanged.connect(self.busy.setLabelText)
        block_keyboard_checkbox.toggled.connect(self.busy.setBlockKeyboard)
        block_mouse_checkbox.toggled.connect(self.busy.setBlockMouse)
        fade_duration_spn.valueChanged.connect(self.busy.setFadeDuration)
        start_btn.clicked.connect(self.busy.start)
        start_btn.clicked.connect(lambda: self.busy.stopAfter(
            busy_duration_spn.value()
        ))
        stop_btn.clicked.connect(self.busy.stop)

    def resizeEvent(self, event):
        self.busy.resize(event.size())
        return super().resizeEvent(event)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = Dialog()
    dialog.setMinimumSize(500, 500)
    dialog.show()
    sys.exit(app.exec())
