from splash_screen import SplashScreen
from main import *


def main():
    app = QApplication(sys.argv)

    """ set style theme """
    # app.setLayoutDirection(QtCore.Qt.RightToLeft)
    # ====================================> setup stylesheet
    # app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment()) # dark style
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # qt_material.apply_stylesheet(app, theme='dark_blue.xml') # search qt_material and select theme
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # style_string = pyqtcss.get_style("dark_blue") # dark theme
    # app.setStyleSheet(style_string)
    
    # read style from .gss file
    stylesheet = app.styleSheet()
    with open('../assets/styles/Combinear.qss') as file:
        app.setStyleSheet(stylesheet + file.read())
    app.setStyle('Fusion')

    splash_screen = SplashScreen()
    # Show application's GUI
    splash_screen.show()
    # Run application's event loop (or main loop)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
