# -*- coding: utf-8 -*-

# o===================| Import Libraries |===================o #

# Pillow Library
from PIL import Image
import PIL.ImageQt as ImageQt

# PyQt5 Library
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi, loadUiType
from PyQt5.QtCore import QPoint, QRect, QRectF, QSize, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QColor, QCursor, QFont, QIcon, QPainterPath, QPainter, QPixmap, QRegion
from PyQt5.QtWidgets import (
    QListWidgetItem, QDesktopWidget, QInputDialog, QApplication,
    QGraphicsDropShadowEffect, QProgressBar, QMainWindow, QMessageBox,
    QHBoxLayout, QSizeGrip, QPushButton, QSizePolicy, QToolButton,
    QVBoxLayout, QFileDialog, QListWidget, QListView, QGridLayout,
    QLineEdit, QTextEdit, QDialog,
    QFrame, QLabel, QStyle,
    QWidget
)

# My Modules
# from splash_screen import SplashScreen
from model.database_repository import DatabaseRepository
from ui_functions import UIFunctions
from image_dialog import ImageDialog
from update_tag import UpdateTag

# Our Libraries
import qt_material
import qdarkstyle
import mimetypes
import platform
import shutil
import sys
import os
import slugify
import sqlite3
import logging
import functools


# set the environment variable to use a specific wrapper
# it can be set to pyqt, pyqt5, pyside or pyside2 (not implemented yet)
# you do not need to use QtPy to set this variable
os.environ['QT_API'] = 'pyqt5'

# set the version and author app
__version__ = '0.1'
__author__ = 'Morteza Abdollahi'
__description__ = 'This is my projects tag image'

# get extenstion for type -? example: send 'images' value and returned '.jpg', '.png' and ...
def get_extensions_for_type(general_type):
    # mimetypes initial and starting
    mimetypes.init()
    # iterate to all type extentions
    for extention in mimetypes.types_map:
        # check type extentoin if is equail > yelid all type extenstion general_type
        if mimetypes.types_map[extention].split('/')[0] == general_type:
            yield extention
    # return ['.png', '.jpg', '.jpeg']


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


class Bubble(QLabel):
    def __init__(self, text):
        super(Bubble, self).__init__(text)
        self.word = text
        self.setContentsMargins(5, 5, 5, 5)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing,True)
        p.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 5, 5)
        super(Bubble, self).paintEvent(e)


# class main application
class MainWindow(QMainWindow, DatabaseRepository):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__() # Call the inherited classes __init__ method
        loadUi('../assets/uis/main.ui', self) # Load the .ui file
        self.settings()
        self.setup_ui()

    def settings(self):
        # self.adjustSize()
        self.center() # move window to center position
        self.setWindowTitle('Image Name Tag Explorer') # set title window
        self.setWindowIcon(QIcon('assets/icons/tag.png'))

        self.dragPos = QtCore.QPoint()

        # move window
        def mouseMoveEvent(event):
            if self.isMaximized():
                self.showNormal()
            elif event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # set title bar
        self.title_bar = self.findChild(QFrame, 'title_bar')
        self.title_bar.mouseMoveEvent = mouseMoveEvent

        # Set Ui Definition
        UIFunctions.ui_definition(self)

    def setup_ui(self):
        # buttons title bar
        self.maximize_btn = self.findChild(QPushButton, 'maximize_btn')
        self.drop_shadow_frame = self.findChild(QFrame, 'drop_shadow_frame')
        self.minimize_btn = self.findChild(QPushButton, 'minimize_btn')
        self.close_btn = self.findChild(QPushButton, 'close_btn')
        self.frame_grip = self.findChild(QFrame, 'frame_grip')

        # buttons folder
        self.add_folder_btn = self.findChild(QPushButton, 'add_folder_btn')
        self.open_folder_btn = self.findChild(QPushButton, 'open_folder_btn')
        self.delete_folder_btn = self.findChild(QPushButton, 'delete_folder_btn')
        self.delete_folder_btn.clicked.connect(lambda: self.delete_selected_folder())
        self.open_folder_btn.clicked.connect(lambda: self.open_selected_folder())
        self.add_folder_btn.clicked.connect(lambda: self.add_folder())

        # list widgets
        self.tag_list_widget = self.findChild(QListWidget, 'tag_list_widget')
        self.folder_list_widget = self.findChild(QListWidget, 'folder_list_widget')
        self.images_path_list_widget = self.findChild(QListWidget, 'images_path_list_widget')
        self.folder_list_widget.itemClicked.connect(lambda: self.show_files_path_by_folder())
        self.tag_list_widget.itemClicked.connect(lambda: self.show_images_path_by_tag())
        self.update_folder_list_widget()

        # buttons tag
        self.add_tag_btn = self.findChild(QPushButton, 'add_tag_btn')
        self.tag_line_edit = self.findChild(QLineEdit, 'tag_line_edit')
        self.delete_tag_btn = self.findChild(QPushButton, 'delete_tag_btn')
        self.search_tag_btn = self.findChild(QPushButton, 'search_tag_btn')
        self.update_tag_btn = self.findChild(QPushButton, 'update_tag_btn')
        self.add_tag_btn.clicked.connect(lambda: self.add_tag_with_selected_images())
        self.delete_tag_btn.clicked.connect(lambda: self.delete_selected_tag())
        self.update_tag_btn.clicked.connect(lambda: self.update_selected_tag())
        self.search_tag_btn.clicked.connect(lambda: self.search_tag())

        # buttons files
        self.rename_image_file_btn = self.findChild(QPushButton, 'rename_image_file_btn')
        self.delete_image_file_btn = self.findChild(QPushButton, 'delete_image_file_btn')
        self.move_image_file_btn = self.findChild(QPushButton, 'move_image_file_btn')
        self.copy_image_file_btn = self.findChild(QPushButton, 'copy_image_file_btn')
        self.move_image_file_btn.clicked.connect(lambda: self.move_or_copy_image_file_path('move'))
        self.copy_image_file_btn.clicked.connect(lambda: self.move_or_copy_image_file_path('copy'))
        self.rename_image_file_btn.clicked.connect(lambda: self.rename_image_file_path())
        self.delete_image_file_btn.clicked.connect(lambda: self.delete_image_file_path())
        self.open_image_btn = self.findChild(QPushButton, 'open_image_btn')
        self.add_images_btn = self.findChild(QPushButton, 'add_images_btn')
        self.open_image_btn.clicked.connect(lambda: self.open_image_dialog())
        self.add_images_btn.clicked.connect(lambda: self.add_images())

        # our buttons
        self.exit_btn = self.findChild(QPushButton, 'exit_btn')
        self.exit_btn.clicked.connect(lambda: self.close_window())


    def update_folder_list_widget(self):
        # delete invalid folder
        self.delete_invalid_folder()
        folders = self.folders_view()
        self.folder_list_widget.clear()
        for folder in folders:
            if platform.system() == 'Linux': split_mode = '/'
            elif platform.system() == 'Windows': split_mode = '\\'
            folder_name = folder.folder_name.split(split_mode)[-1]
            folder_name_item = QListWidgetItem(folder_name)
            self.folder_list_widget.addItem(folder_name_item)

    def update_tag_list_widget(self):
        get_folder_name = self.get_selected_folder_name()
        if get_folder_name:
            tags = self.tags_view(get_folder_name)
            self.tag_list_widget.clear()
            for tag in tags:
                tag_name_item = QListWidgetItem(tag.tag_name)
                self.tag_list_widget.addItem(tag_name_item)
            return
        self.tag_list_widget.clear()


    def get_selected_folder_name(self):
        if len(self.folders_view()) > 0 and \
           self.folder_list_widget.count() > 0 and \
           len(self.folder_list_widget.selectedItems()) == 1:
                for folder_name in self.folder_list_widget.selectedItems():
                    get_folder_name = folder_name.text()
                    return get_folder_name

    def get_selected_tag_name(self):
        if self.get_selected_folder_name() and \
           len(self.tags_view(self.get_selected_folder_name())) > 0 and \
           len(self.tag_list_widget.selectedItems()) == 1 and \
           self.tag_list_widget.count() > 0:
                for tag_name in self.tag_list_widget.selectedItems():
                    get_tag_name = tag_name.text()
                    return get_tag_name

    def get_selected_images_path(self):
        images_path = []
        if self.get_selected_folder_name(): # check selected folder name
            for image_path in self.images_path_list_widget.selectedItems():
                images_path.append(image_path.text()) # append image path to list
        return images_path # return image_path

    def show_images_path_by_tag(self):
        """ showing images path by tag """
        get_folder_name = self.get_selected_folder_name() # get selected folder name
        get_tag_name = self.get_selected_tag_name() # get selected tag name
        if get_folder_name and get_tag_name: # check selected folder and tag
            self.images_path_list_widget.clear() # clear images_path_list_widget for new deta
            images = self.images_view_by_tag(get_tag_name, get_folder_name) # images path
            for image in images: # iterate images_path
                image_path = image.image_path # get image path from tuple
                image_path_item = QListWidgetItem(image_path) # create item
                image_path_icon = create_QIcon(image_path, 20, 20) # create icon \
                if image_path_icon is not None: # check if image path is not None \
                    image_path_item.setIcon(image_path_icon) # set image path icon \
                # add created item with icon in images_path_list_widget
                self.images_path_list_widget.addItem(image_path_item)
            # set get_tag_name text for tag_line_edit
            self.tag_line_edit.setText(get_tag_name)
    
    def show_files_path_by_folder(self):
        """ Show the path of all the selected files in the folder marked with the extension """
        # get all images file extendion
        images_file_extension = tuple(get_extensions_for_type('image'))
        self.update_tag_list_widget() # update tags list widget
        self.tag_line_edit.setText('') # reset line edit
        get_folder_name = self.get_selected_folder_name() # get selected folder name
        if get_folder_name:
            get_folder_path = self.get_folder_path(get_folder_name) # get folder path
            # os.chdir(get_folder_path) # change directory
            self.images_path_list_widget.clear() # clear the images path list widget
            for (root, dirs, files) in os.walk(get_folder_path): # get (root, dirs, files)
                for file in files: # file in [files] -> example: main.py in [..., main.py ,...]
                    file_path = os.path.join(root, file) # get the full file path
                    filename, file_extension = os.path.splitext(file_path) # extracting extension from filename
                    # Checks if there is a file with the specified extension in the folder, show it if there is one
                    if file_extension in images_file_extension:
                        # The last step is to add the file to the files path list widget
                        # Create the row with Icon + Text - - - - \
                        file_path_item = QListWidgetItem(file_path) # create item for list widget
                        # set size of the item
                        ## size = QtCore.QSize()
                        ## size.setHeight(17)
                        ## size.setWidth(400)
                        ## file_path_item.setSizeHint(size)
                        # file_path_item.setFlags(file_path_item.flags() | Qt.ItemIsUserCheckable)
                        # file_path_item.setCheckState(Qt.Unchecked)
                        # file_path_item.setFixedWidth(file_path_item.sizeHint().width())
                        image_icon = create_QIcon(file_path, 20, 20)
                        file_path_item.setIcon(image_icon) # set size of the item
                        self.images_path_list_widget.addItem(file_path_item) # Put the item into the widget
                    else:
                        pass
                # */
                #    * We break the loop so that it does not repeat
                #    * itself and only retrieves the files that
                #    * are in the current path.
                # /*
                break


    def search_tag(self):
        """ search files by tag """
        get_folder_name = self.get_selected_folder_name()
        if get_folder_name:
            get_tag_name = self.tag_line_edit.text()
            if len(get_tag_name) != 0:
                images_path = self.get_images_path_by_tag(get_folder_name, get_tag_name)
                self.images_path_list_widget.clear()
                for image_path in images_path:
                    file_path = image_path[1]
                    file_path_item = QListWidgetItem(file_path)
                    image_icon = create_QIcon(file_path, 20, 20)
                    file_path_item.setIcon(image_icon)
                    self.images_path_list_widget.addItem(file_path_item)
            else:
                self.show_files_path_by_folder()

    # folder functions

    def add_folder(self):
        # open dialog and select folder path
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder_path != '':
            # get folder name from folder path
            folder_name = folder_path.split('/')[-1]
            ok = self.insert_to_folder(folder_name, folder_path) # insert to folder
            # add folder if folder not exists
            if ok['message'] == 'inserted to folder':
                self.images_path_list_widget.clear()
                self.update_folder_list_widget() # update folder list widget
                self.update_tag_list_widget() # update tag list widget
            # if folder exists show message
            else:
                message = QMessageBox()
                message.setIcon(QMessageBox.Warning)
                message.setWindowTitle('Warning Message')
                message.setText(ok['message'])
                message.exec()

    def delete_selected_folder(self):
        #=> first step \
         # delete invalid folder
        self.delete_invalid_folder()
        get_folder_name = self.get_selected_folder_name()
        if get_folder_name:
            reply = QMessageBox.question(self,
                'Delete', 'Are you sure you want to delete?',
                QMessageBox.Yes |
                QMessageBox.No,
                QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delete_folder(get_folder_name)
                self.images_path_list_widget.clear()
                self.update_folder_list_widget() # update folder list widget
                self.update_tag_list_widget() # update tag list widget
            else:
                pass

    def open_selected_folder(self):
        get_folder_name = self.get_selected_folder_name()
        if get_folder_name:
            get_folder_path = self.get_folder_path(get_folder_name)
            if get_folder_path:
                if platform.system() == 'Linux':
                    os.system('xdg-open "%s"' % get_folder_path)
                elif platform.system() == 'Windows':
                    os.startfile(get_folder_path)

    # tag functions

    def add_tag_with_selected_images(self):
        images_path = self.get_selected_images_path()
        if len(images_path) >= -1:
            get_folder_name = self.get_selected_folder_name()
            tag_name, success = QInputDialog.getText(self, 'Add Tag', 'Please Enter Tag Name?')
            if success is True:
                if tag_name != '':
                    ok = self.insert_to_tag( # insert to tag and image
                        tag_name, # this is tag name
                        get_folder_name, # this is folder path
                        images_path, # this is images path
                    )
                    if ok:
                        self.show_files_path_by_folder()
                        self.update_tag_list_widget()
                    else:
                        pass

    def delete_selected_tag(self):
        get_folder_name = self.get_selected_folder_name()
        get_tag_name = self.get_selected_tag_name()
        if get_tag_name:
            reply = QMessageBox.question(self,
                'Delete', 'Are you sure you want to delete?',
                QMessageBox.Yes |
                QMessageBox.No,
                QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delete_tag(get_tag_name, get_folder_name)
                self.show_files_path_by_folder()
                self.update_tag_list_widget()
            else:
                pass

    def update_selected_tag(self):
        get_folder_name = self.get_selected_folder_name()
        get_tag_name = self.get_selected_tag_name()
        if get_folder_name and get_tag_name:
            images = self.images_view_by_tag(get_tag_name, get_folder_name)
            update_tag_dialog = UpdateTag(images, get_tag_name, get_folder_name)
            update_tag_dialog.exec_()
            self.show_images_path_by_tag()

    # images functions

    def rename_image_file_path(self):
        images_path = self.get_selected_images_path()
        if len(images_path) == 1:
            image_path = images_path[0]
            if platform.system() == 'Linux': split_mode = '/'
            if platform.system() == 'Windows': split_mode = '\\'
            old_image_file_name = image_path.split(split_mode)[-1]
            file_name, file_extension = os.path.splitext(old_image_file_name)
            new_name, success = QInputDialog.getText(self,
                'input new image file name',
                'please input new image file name?',
                text=file_name)
            if success is True:
                dirname = os.path.dirname(image_path)
                new_image_file_name = os.path.join(dirname, slugify.slugify(new_name) + file_extension)
                old_image_file_name = os.path.join(dirname, old_image_file_name)
                # enclosing inside try-except
                try:
                    os.rename(old_image_file_name, new_image_file_name)
                    self.rename_image_file_name(old_image_file_name, new_image_file_name)
                    self.show_files_path_by_folder()
                except FileExistsError:
                    message = QMessageBox()
                    message.setIcon(QMessageBox.Warning)
                    message.setWindowTitle('Error Message')
                    message.setText('File already Exists')
                    message.exec()

    def delete_image_file_path(self):
        images_path = self.get_selected_images_path()
        if len(images_path) >= 1:
            reply = QMessageBox.question(self,
                'Delete', 'Are you sure you want to delete?',
                QMessageBox.Yes |
                QMessageBox.No,
                QMessageBox.No)
            if reply == QMessageBox.Yes:
                for image_path in images_path:
                    os.remove(image_path)
                    self.delete_image_file_name(image_path)
                    self.show_files_path_by_folder()

    def move_or_copy_image_file_path(self, value):
        images_path = self.get_selected_images_path()
        if len(images_path) >= 1:
            folder_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if folder_path != '':
                for image_path in images_path:
                    if value == 'move': shutil.move(image_path, folder_path)
                    elif value == 'copy': shutil.copy(image_path, folder_path)
                self.delete_image_file_name(image_path)
                self.show_files_path_by_folder()
            else: pass
        else: pass

    def open_image_dialog(self):
        images_path = self.get_selected_images_path()
        if len(images_path) >= 1:
            for image_path in images_path:
                image_dialog = ImageDialog()
                image_dialog.show_image(image_path)
                image_dialog.exec_()

    def add_images(self):
        # help(QFileDialog.getOpenFileName)
        get_folder_name = self.get_selected_folder_name()
        if get_folder_name:
            images_path = QFileDialog.getOpenFileNames(self, "Select Images", filter="*.png *.jpeg *.png")[0]
            get_tag_name = self.get_selected_tag_name()
            if get_tag_name:
                insert_to_tag = self.insert_to_images_in_tag( # insert to tag and image
                    get_tag_name, # this is tag name
                    get_folder_name, # this is folder path
                    images_path
                ); self.show_images_path_by_tag()
            else:
                get_folder_path = self.get_folder_path(get_folder_name)
                if get_folder_path:
                    for image_path in images_path:
                        try:
                            shutil.copy(image_path, get_folder_path)
                            self.show_files_path_by_folder()
                        except FileExistsError:
                            message = QMessageBox()
                            message.setIcon(QMessageBox.Warning)
                            message.setWindowTitle('Error Message')
                            message.setText('File already Exists')
                            message.exec()

    # our functions ...

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def mousePressEvent(self, event):
        radius = 10
        self.setStyleSheet("""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
        """.format(radius))

        self.dragPos = event.globalPos()

    def close_window(self):
        self.close()
