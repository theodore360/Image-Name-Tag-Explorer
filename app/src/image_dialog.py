from main import *


# open image
class ImageDialog(QDialog):
    def __init__(self, parent=None):
        super(ImageDialog, self).__init__() # Call the inherited classes __init__ method
        loadUi('../assets/uis/image_dialog.ui', self) # Load the .ui file
        self.setup_ui()
    
    def setup_ui(self):
        self.close_image_btn = self.findChild(QPushButton, 'close_image_btn')
        self.close_image_btn.clicked.connect(lambda: self.close_image())
        self.show_image_lbl = self.findChild(QLabel, 'show_image_lbl')

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.show_image_lbl.setPixmap(pixmap.scaled(self.show_image_lbl.size()))
        self.resize(pixmap.width(), pixmap.height())

    def close_image(self):
        self.close()
