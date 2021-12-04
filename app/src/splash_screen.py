from main import *


# Globals
counter = 0

# splash screen window
class SplashScreen(QMainWindow):
    def __init__(self, parent=False):
        super(SplashScreen, self).__init__() # Call the inherited classes __init__ method
        loadUi('../assets/uis/splash_screen.ui', self) # Load the .ui file
        self.settings()
        self.setup_ui()

    def settings(self):
        self.center()
        # Remove title bar
        self.setWindowFlags(Qt.Window)
        #self.setWindowFlags(Qt.FramelessWindowHint) # Set the form without borders
        self.setAttribute(Qt.WA_TranslucentBackground) # Set background transparency
        # self.setMouseTracking(True)  # Set widget mouse tracking

        # drop shadow effect
        radius = 20
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def setup_ui(self):
        # Start timer
        self.progress_bar = self.findChild(QProgressBar, 'progress_bar')
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(20)

        # Change description
        self.description_lbl = self.findChild(QLabel, 'description_lbl')
        QTimer().singleShot(1, lambda: self.description_lbl.setText("Image Name Tag Explorer"))
        QTimer().singleShot(1, lambda: self.description_lbl.setText("<strong>LOADING</strong> DATABASE"))
        db = DatabaseRepository()
        db.create_tables()
        QTimer().singleShot(3000, lambda: self.description_lbl.setText("\
        <strong>LOADING</strong> USER INTERFACE"))

    def progress(self):
        global counter
        # Set value to progress bar
        self.progress_bar.setValue(counter)
        # Close Splash Screen AND open app
        if counter > 100:
            # stop timer
            self.timer.stop()
            # Show main window application
            self.main = MainWindow()
            self.main.show()
            # Close Splash Screen
            self.close()
        # Increase counter
        counter += 1

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())
