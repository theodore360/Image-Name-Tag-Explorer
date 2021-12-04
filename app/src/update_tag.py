from main import *

import sqlite3
import os

# create icon and return
# def create_QIcon(image_path, width, hieght):
#     # create QIcon
#     try:
#         picture = Image.open(image_path)
#         picture.thumbnail((width, hieght), Image.ANTIALIAS)
#         icon = QIcon(QPixmap.fromImage(ImageQt(picture)))
#         return icon
#     except FileNotFoundError as error:
#         print (error)

# create icon and return
def create_QIcon(image_path, width, hieght):
    # create QIcon
    try:
        # scaled_picture = picture.scaled(QSize(100, 100))
        # picture = Image.open(image_path)
        # picture.thumbnail((width, hieght), Image.ANTIALIAS)
        # icon = QIcon(QPixmap.fromImage(ImageQt(picture)))
        picture = QPixmap(image_path)
        icon = QIcon(picture)
        return icon
    except FileNotFoundError as error:
        print(error)

def get_extensions_for_type(general_type):
    return ['.png', '.jpg', '.jpeg']


# open image
class AddImageFileDialog(QDialog, DatabaseRepository):
    def __init__(self, tag_name, folder_name, parent=None):
        self.tag_name = tag_name
        self.folder_name = folder_name

        super(AddImageFileDialog, self).__init__() # Call the inherited classes __init__ method
        loadUi('../assets/uis/add_images_file_dialog.ui', self) # Load the .ui file
        self.setup_ui()

    def setup_ui(self):
        self.add_images_file_btn = self.findChild(QPushButton, 'add_images_file_btn')
        self.images_path_list_widget = self.findChild(QFrame, 'images_path_list_widget')
        self.add_images_file_btn.clicked.connect(lambda: self.add_images_file_path())
        self.show_files_path_by_folder()


    def get_selected_images_path(self):
        images_path = [] # images selected path
        for image_path in self.images_path_list_widget.selectedItems():
            images_path.append(image_path.text()) # append image path to images path
        return images_path

    def show_files_path_by_folder(self):
        images_path = [image.image_path for image in self.images_view_by_tag(self.tag_name, self.folder_name)]
        self.images_path_list_widget.clear()
        images_file_extension = tuple(get_extensions_for_type('image'))
        get_folder_path = self.get_folder_path(self.folder_name)
        for (root, dirs, files) in os.walk(get_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_path in images_path:
                    filename, file_extension = os.path.splitext(file_path)
                    if file_extension in images_file_extension:
                        file_path_item = QListWidgetItem(file_path)
                        image_icon = create_QIcon(file_path, 20, 20)
                        file_path_item.setIcon(image_icon)
                        self.images_path_list_widget.addItem(file_path_item)
                    else:
                        pass

    def add_images_file_path(self):
        images_path = self.get_selected_images_path()
        insert_to_tag = self.insert_to_images_in_tag( # insert to tag and image
            self.tag_name, # this is tag name
            self.folder_name, # this is folder path
            images_path
        )
        # update images list widget
        self.show_files_path_by_folder()
        self.close()


class UpdateTag(QDialog, DatabaseRepository):
    def __init__(self, images, tag_name, folder_name, parent=None):
        self.images = images
        self.tag_name = tag_name
        self.folder_name = folder_name

        super(UpdateTag, self).__init__() # Call the inherited classes __init__ method
        loadUi('../assets/uis/update_tag_dialog.ui', self) # Load the .ui file
        self.setWindowTitle('Update "%s"' % self.tag_name)
        self.setup_ui()


    def setup_ui(self):
        self.close_btn = self.findChild(QPushButton, 'close_btn')
        self.add_images_file_btn = self.findChild(QPushButton, 'add_images_file_btn')
        self.delete_images_file_btn = self.findChild(QPushButton, 'delete_images_file_btn')
        self.delete_images_file_btn.clicked.connect(lambda: self.delete_selected_images_path())
        self.add_images_file_btn.clicked.connect(lambda: self.add_images_path())
        self.close_btn.clicked.connect(lambda: self.close_update_tag_dialog())

        self.images_path_list_widget = self.findChild(QFrame, 'images_path_list_widget')
        self.show_images_path_by_tag()


    def get_selected_images_path(self):
        images_path = [] # images selected path
        for image_path in self.images_path_list_widget.selectedItems():
            images_path.append(image_path.text()) # append image path to images path
        return images_path

    def show_images_path_by_tag(self):
        self.images_path_list_widget.clear()
        images = self.images_view_by_tag(self.tag_name, self.folder_name)
        for image in images:
            image_path = image.image_path
            image_path_item = QListWidgetItem(image_path)
            image_icon = create_QIcon(image_path, 20, 20)
            if image_icon is not None:
                image_path_item.setIcon(image_icon)
            self.images_path_list_widget.addItem(image_path_item)

    def add_images_path(self):
        add_images_file_dialog = AddImageFileDialog(self.tag_name, self.folder_name)
        add_images_file_dialog.exec_()
        # update images list widget
        self.show_images_path_by_tag()

    def delete_selected_images_path(self):
        images_path = self.get_selected_images_path()
        if images_path:
            self.delete_images_file_from_tag(
                self.tag_name,
                self.folder_name,
                images_path
            )
            # update images list widget
            self.show_images_path_by_tag()

    def close_update_tag_dialog(self):
        self.close()
