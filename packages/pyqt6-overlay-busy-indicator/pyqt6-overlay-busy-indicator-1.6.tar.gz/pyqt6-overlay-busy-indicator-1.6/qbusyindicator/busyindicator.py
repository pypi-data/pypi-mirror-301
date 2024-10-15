from enum import Enum

from PyQt6 import QtGui, QtCore, QtWidgets


class QOverlayState(Enum):
    BUSY = 'Busy'
    STOPPING = 'Stopping'
    STOPPED = 'Stopped'


class QOverlayBusyIndicator(QtWidgets.QWidget):
    started = QtCore.pyqtSignal()
    stopped = QtCore.pyqtSignal()

    def __init__(self, parent=None, label_text='', image_path='',
                 fade_duration=400, block_keyboard=False, block_mouse=False):
        super().__init__(parent)
        self.hide()
        self.window().installEventFilter(self)

        palette = QtGui.QPalette(self.palette())
        self.setPalette(palette)
        self.setStyleSheet('background-color: rgba(204, 204, 204, 70);')
        self.effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0)

        self._movie = QtGui.QMovie(image_path, QtCore.QByteArray(), self)
        size = self._movie.scaledSize()
        self.setGeometry(0, 0, size.width(), size.height())

        self._movie_label = QtWidgets.QLabel(self)
        self._movie_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )
        self._movie_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom |
                                       QtCore.Qt.AlignmentFlag.AlignHCenter)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self._movie_label)

        self.label = QtWidgets.QLabel(label_text)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                 QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop |
                                QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label.setStyleSheet('color: #808080; padding-top: 5px;')
        main_layout.addWidget(self.label)
        self.setLayout(main_layout)

        self._movie.setCacheMode(QtGui.QMovie.CacheMode.CacheAll)
        self._movie.setSpeed(100)
        self._movie_label.setMovie(self._movie)

        self._current_state = QOverlayState.STOPPED
        self.label_text = label_text
        self.fade_duration = fade_duration
        self.block_keyboard = block_keyboard
        self.block_mouse = block_mouse
        self.image_path = image_path

    def is_busy(self):
        return self._current_state == QOverlayState.BUSY

    def is_stopping(self):
        return self._current_state == QOverlayState.STOPPING

    def is_stopped(self):
        return self._current_state == QOverlayState.STOPPED

    def start(self):
        if not self.is_busy():
            self.show()
            if self.block_keyboard:
                self.grabKeyboard()
            if self.block_mouse:
                self.grabMouse()
            self._current_state = QOverlayState.BUSY
            self._movie.start()
            animation = QtCore.QVariantAnimation(self)
            animation.setStartValue(0.)
            animation.setEndValue(1.)
            animation.setDuration(self.fade_duration)
            animation.valueChanged.connect(self.graphicsEffect().setOpacity)
            animation.finished.connect(self.started.emit)
            animation.start()

    def stop(self):
        if self.is_busy() or self.is_stopping():
            self._current_state = QOverlayState.STOPPED
            self._movie.stop()
            animation = QtCore.QVariantAnimation(self)
            animation.setStartValue(1.)
            animation.setEndValue(0.)
            animation.setDuration(self.fade_duration)
            animation.valueChanged.connect(self.graphicsEffect().setOpacity)
            animation.finished.connect(self.hide)
            animation.finished.connect(self.stopped.emit)
            if self.block_keyboard:
                animation.finished.connect(self.releaseKeyboard)
            if self.block_mouse:
                animation.finished.connect(self.releaseMouse)
            animation.start()

    def stop_after(self, msecs):
        self._current_state = QOverlayState.STOPPING
        QtCore.QTimer.singleShot(msecs, self.stop)

    @property
    def label_text(self):
        return self.label.text()

    @label_text.setter
    def label_text(self, s):
        self.label.setText(s)

    @property
    def label_font(self):
        return self.label.font()

    @label_font.setter
    def label_font(self, f):
        self.label.setFont(f)

    @property
    def image_path(self):
        return self._movie.fileName()

    @image_path.setter
    def image_path(self, p):
        return self._movie.setFileName(p)

    def imagePath(self):
        return self.image_path

    def setImagePath(self, p):
        self.image_path = p

    def labelText(self):
        return self.label_text

    def setLabelText(self, s):
        self.label_text = s

    def labelFont(self):
        return self.label_font

    def setLabelFont(self, f):
        self.label_font = f

    def keyboardBlocked(self):
        return self.block_keyboard

    def setBlockKeyboard(self, b):
        self.block_keyboard = b

    def mouseBlocked(self):
        return self.block_mouse

    def setBlockMouse(self, b):
        self.block_mouse = b

    def isBusy(self):
        return self.is_busy()

    def isStopping(self):
        return self.is_stopping()

    def isStopped(self):
        return self.is_stopped()

    def stopAfter(self, msecs):
        self.stop_after(msecs)

    def fadeDuratrion(self):
        return self.fade_duration

    def setFadeDuration(self, msecs):
        self.fade_duration = msecs

    def eventFilter(self, obj, event):
        if self.is_busy() and event.type() in (QtCore.QEvent.KeyPress,
                                               QtCore.QEvent.KeyRelease):
            return True
        return super().eventFilter(obj, event)
