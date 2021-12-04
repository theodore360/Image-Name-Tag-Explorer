from main import *


class UIFunctions(QMainWindow):

    # Maximize <-> Restore Function
    @pyqtSlot()
    def maximize_restore_window(self):
        path = QtGui.QPainterPath()
        # Maximization and recovery
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setToolTip("Restore")
            radius = 10
            rect = QtCore.QRect(0, 0, 994, 593)
            print (self.rect())
        else:
            self.showMaximized()
            self.maximize_btn.setToolTip("Maximize")
            radius = 0
            rect = QtCore.QRect(0, 0, 16777215, 16777215)
        self.setStyleSheet("""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
        """.format(radius))


    @pyqtSlot()
    def minimize_window(self):
        self.showMinimized()

    @pyqtSlot()
    def close_window(self):
        self.close()

    # Ui Definition
    def ui_definition(self):
        
        # Remove title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        radius = 10
        self.setStyleSheet("""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
        """.format(radius))


        # set dropshadow window
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))

        # apply dropshadow to frame
        self.drop_shadow_frame.setGraphicsEffect(self.shadow)

        # signal title bar button
        self.maximize_btn.clicked.connect(lambda: UIFunctions.maximize_restore_window(self))
        self.minimize_btn.clicked.connect(lambda: UIFunctions.minimize_window(self))
        self.close_btn.clicked.connect(lambda: UIFunctions.close_window(self))

        # create size grip to resize window
        # self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip = QSizeGrip(self.frame_grip)
        self.sizegrip.setToolTip("Resize Window")

