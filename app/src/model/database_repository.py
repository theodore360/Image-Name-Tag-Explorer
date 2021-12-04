# Import the sqlite3 module
import sqlite3
import shutil
import os


from model import (
    database_config,
    folder,
    image,
    tag,
)


# create a default path to connect to and create (if necessary) a database
# called "tags.db" in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), database_config.DATABASE_NAME)


class DatabaseRepository:

    def db_connect(self, db_path=DEFAULT_PATH):
        # if there is not database, it builds else, it just connect
        connection = sqlite3.connect(db_path)
        return connection

    def create_tables(self):
        # with or connection.close command are close from database opened
        with self.db_connect() as connection:
            # Creating cursor
            cursor = connection.cursor()

            # creation tables
            # create folders table if not exists
            cursor.execute(f"""\
                CREATE TABLE IF NOT EXISTS {database_config.TABLE_FOLDER_NAME} (
                    {database_config.COLUMN_FOLDER_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {database_config.COLUMN_FOLDER_NAME} TEXT NOT NULL,
                    {database_config.COLUMN_FOLDER_PATH} TEXT NOT NULL
                    );""")
            
            # create tags table if not exists
            cursor.execute(f"""\
                CREATE TABLE IF NOT EXISTS {database_config.TABLE_TAG_NAME} (
                    {database_config.COLUMN_TAG_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {database_config.COLUMN_TAG_NAME} TEXT NOT NULL,
                    {database_config.COLUMN_TAG_FOLDER_ID} INTEGER,
                    FOREIGN KEY({database_config.COLUMN_TAG_FOLDER_ID}) REFERENCES \
                        {database_config.TABLE_FOLDER_NAME}({database_config.COLUMN_TAG_ID})
                    );""")
            
            # create images table if not exists
            cursor.execute(f"""\
                CREATE TABLE IF NOT EXISTS {database_config.TABLE_IMAGE_NAME} (
                    {database_config.COLUMN_IMAGE_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {database_config.COLUMN_IMAGE_PATH} TEXT NOT NULL,
                    {database_config.COLUMN_IMAGE_TAG_ID} INTEGER,
                    FOREIGN KEY({database_config.COLUMN_IMAGE_TAG_ID}) REFERENCES \
                        {database_config.TABLE_TAG_NAME}({database_config.COLUMN_IMAGE_ID})
                    );""")

            connection.commit() # commit


    def get_folder_path(self, folder_name):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT {database_config.COLUMN_FOLDER_PATH} FROM \
            {database_config.TABLE_FOLDER_NAME} WHERE {database_config.COLUMN_FOLDER_NAME}=?", (
                folder_name,
            )); folder_path = cursor.fetchall()[0][0]
            return folder_path

    def get_images_path_by_tag(self, folder_name, tag_name):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            folder_path = self.get_folder_path(folder_name)
            tag_id = self.get_tag_id(tag_name, folder_path)
            cursor.execute(f"SELECT * FROM {database_config.TABLE_IMAGE_NAME} WHERE \
                {database_config.COLUMN_IMAGE_TAG_ID}=?", (tag_id, ))
            image_rows = cursor.fetchall()
            return image_rows

    def check_exists_folders(self, folder_path):
        # this is function check exists folders for insert to folder
        with self.db_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {database_config.TABLE_FOLDER_NAME} WHERE \
                {database_config.COLUMN_FOLDER_PATH}=?", (
                    folder_path, # this is folder path
            )); folder_rows = cursor.fetchall()
            # checking len folder rows if 0 returing True else False
            if len(folder_rows) == 0:
                return True
            return False

    def check_exists_image_path(self, old_images_path):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {database_config.TABLE_IMAGE_NAME} WHERE \
                {database_config.COLUMN_IMAGE_PATH}=?", (
                    old_images_path,
            )); image_rows = cursor.fetchall()
            if len(image_rows) >= 0:
                return True
            return False

    # get id functions
    def get_folder_id(self, folder_path):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT {database_config.COLUMN_FOLDER_ID} FROM \
                {database_config.TABLE_FOLDER_NAME} WHERE {database_config.COLUMN_FOLDER_PATH}=?", (
                    folder_path,
            )); folder_id = cursor.fetchall()[0][0]
        return folder_id

    def get_tag_id(self, tag_name, folder_path):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            try:
                folder_id = self.get_folder_id(folder_path)
                cursor.execute(f"SELECT {database_config.COLUMN_TAG_ID} FROM \
                    {database_config.TABLE_TAG_NAME} WHERE \
                    {database_config.COLUMN_TAG_NAME}=? AND \
                    {database_config.COLUMN_TAG_FOLDER_ID}=?", (
                        tag_name,
                        folder_id
                )); tag_id = cursor.fetchall()[0][0]
                return tag_id
            except IndexError:
                pass

    # views function
    def folders_view(self):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {database_config.TABLE_FOLDER_NAME}")
            folder_rows = cursor.fetchall()

            # TODO: create folder object and add to folders list
            folders = []
            for folder_row in folder_rows:
                _folder = folder.Folder(
                    id=folder_row[0],
                    folder_name=folder_row[1],
                    folder_path=folder_row[2]
                ); folders.append(_folder)

        # return folder list objects
        return folders

    def tags_view(self, folder_name):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            folder_path = self.get_folder_path(folder_name)
            folder_id = self.get_folder_id(folder_path)
            cursor.execute(f"SELECT * FROM {database_config.TABLE_TAG_NAME} WHERE \
                {database_config.COLUMN_TAG_FOLDER_ID}=?", (folder_id, ))
            tag_rows = cursor.fetchall()

            # TODO: create tag object and add to tags list
            tags = []
            for tag_row in tag_rows:
                _tag = tag.Tag(
                    id=tag_row[0],
                    tag_name=tag_row[1],
                    folder_id=tag_row[2]
                ); tags.append(_tag)

        # return tag list objects
        return tags

    def images_view_by_tag(self, tag_name, folder_name):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            folder_path = self.get_folder_path(folder_name)
            tag_id = self.get_tag_id(tag_name, folder_path)
            cursor.execute(f"SELECT * FROM {database_config.TABLE_IMAGE_NAME} WHERE \
                {database_config.COLUMN_IMAGE_TAG_ID}=?", (tag_id, ))
            image_rows = cursor.fetchall()

            # TODO: create image object and add to images list
            images = []
            for image_row in image_rows:
                _image = image.Image(
                    id=image_row[0],
                    image_path=image_row[1],
                    tag_id=image_row[2]
                ); images.append(_image)

        # return image list objects
        return images


    # inserts function
    def insert_to_folder(self, folder_name, folder_path):
        if self.check_exists_folders(folder_path):
            with self.db_connect() as connection:
                # dainamic generic folder name
                count_folder_name = 0
                folder_rows = self.folders_view()
                for folder_row in folder_rows:
                    old_folder_name = folder_row.folder_name
                    if folder_name == folder_row.folder_name or \
                    folder_name in old_folder_name:
                        count_folder_name += 1
                new_folder_name = '%s (%i)' % (folder_name, count_folder_name) if count_folder_name !=0 \
                    else folder_name
                # get a connection cursor for commit commands
                cursor = connection.cursor()
                # insert new data to folders
                cursor.execute(f"INSERT INTO {database_config.TABLE_FOLDER_NAME} VALUES (NULL,?,?)", (
                    new_folder_name,
                    folder_path
                )); connection.commit()
                # send success message
                return {'message': 'inserted to folder'}
        else:
            # send exists folder path message
            return {'message': 'exists folder path'}

    def insert_to_tag(self, tag_name, folder_name, images_path=[]):
        with self.db_connect() as connection:
            exists_tag_name = self.get_images_path_by_tag(folder_name, tag_name)
            folder_path = self.get_folder_path(folder_name)
            # searching to images if tag id is not define continue else dosn't insert to tag
            if exists_tag_name == []: # checking
                cursor = connection.cursor() # get cursor
                # create tag row
                folder_id = self.get_folder_id(folder_path) # get folder id \
                cursor.execute(f"INSERT INTO {database_config.TABLE_TAG_NAME} VALUES (NULL,?,?)", (tag_name, folder_id)) # insert to tag
                connection.commit() # connection commit
                # create image rows \
                if len(images_path) != 0: # check if selected images path is grid 0
                    tag_id = self.get_tag_id(tag_name, folder_path) # get tag id for insert
                    for image_path in images_path: # iterate on images path \
                        cursor.execute(f"INSERT INTO {database_config.TABLE_IMAGE_NAME} VALUES (NULL,?,?)", ( # insert to images
                            image_path, # send image path
                            tag_id # and send tag id
                        )) # inserted to tag
                    connection.commit() # connection commit
                    return True # send success message
                else: # end exists_tag_name if
                    pass # pass and send error message
            return False # send error message

    def insert_to_images_in_tag(self, tag_name, folder_name, images_path=None):
        with self.db_connect() as connection:
            cursor = connection.cursor() # get cursor
            # create image rows \
            if len(images_path) != 0: # check if selected images path is grid 0
                folder_path = self.get_folder_path(folder_name) # get folder id
                tag_id = self.get_tag_id(tag_name, folder_path) # get tag id for insert
                for image_path in images_path: # iterate on images path \
                    cursor.execute("INSERT INTO images VALUES (NULL,?,?)", ( # insert to images
                        image_path, # send image path
                        tag_id # and send tag id
                    )) # inserted to tag
                connection.commit() # connection commit
                return 'inserted to tag' # send success message
            else: # end exists_tag_name if
                pass # pass and send error message

    # deletes function
    def delete_folder(self, folder_name):
        """ deleting equial id from folders , from tags and images """
        with self.db_connect() as connection:
            cursor = connection.cursor()
            folder_path = self.get_folder_path(folder_name)
            folder_id = self.get_folder_id(folder_path)
            cursor.execute(f"DELETE FROM {database_config.TABLE_FOLDER_NAME} WHERE {database_config.COLUMN_FOLDER_ID}=?", (folder_id, )) # delete folder
            cursor.execute(f"DELETE FROM {database_config.TABLE_TAG_NAME} WHERE {database_config.COLUMN_TAG_FOLDER_ID}=?", (folder_id, )) # delete tags by folder
            # delete images path by tags
            for tag in self.tags_view(folder_name):
                tag_id = self.get_tag_id(tag.tag_name, folder_path)
                cursor.execute(f"DELETE FROM {database_config.TABLE_IMAGE_NAME} WHERE \
                    {database_config.COLUMN_IMAGE_TAG_ID}=?", (tag_id, ))
            connection.commit() # commit

    def delete_invalid_folder(self):
        with self.db_connect() as connection:
            folders_row = self.folders_view()
            for folder_row in folders_row:
                folder_path = folder_row.folder_path # get item folder path
                # check exists folder and return True or False
                exists_folder_path = os.path.exists(folder_path)
                if exists_folder_path is False: # if folder is not exists delete folder
                    folder_name = folder_row.folder_name # get folder name
                    self.delete_folder(folder_name) # delete folder
                else:
                    pass

    def delete_image_file_name(self, image_path):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            if self.check_exists_image_path(image_path) is not False:
                cursor.execute("DELETE FROM images WHERE image_path=?", (
                    image_path, # this is old image name
                )); connection.commit() # commit

    def delete_tag(self, tag_name, folder_name):
        """ deleting equial id from tag and images """
        with self.db_connect() as connection:
            cursor = connection.cursor()
            folder_path = self.get_folder_path(folder_name)
            folder_id = self.get_folder_id(folder_path)
            tag_id = self.get_tag_id(tag_name, folder_path)
            cursor.execute(f"DELETE FROM {database_config.TABLE_TAG_NAME} WHERE {database_config.COLUMN_TAG_ID}=?", (tag_id, )) # delete all tags in folder
            # delete all files in tags
            for tag in self.tags_view(folder_name):
                tag_id = self.get_tag_id(tag_id, folder_path)
                cursor.execute(f"DELETE FROM {database_config.TABLE_IMAGE_NAME} WHERE \
                    {database_config.COLUMN_IMAGE_TAG_ID}=?", (tag_id, ))
            connection.commit() # commit

    def delete_images_file_from_tag(self, tag_name, folder_name, images_path):
        global connection
        with self.db_connect() as connection:
            cursor = connection.cursor()
            folder_path = self.get_folder_path(folder_name)
            tag_id = self.get_tag_id(tag_name, folder_path)
            for image_path in images_path:
                cursor.execute(f"DELETE FROM {database_config.TABLE_IMAGE_NAME} WHERE \
                    {database_config.COLUMN_IMAGE_PATH}=? AND {database_config.COLUMN_IMAGE_TAG_ID}=?", (
                        image_path,
                        tag_id,
                    )); connection.commit() # commit 

    # rename function
    def rename_image_file_name(self, old_images_path, new_images_path):
        with self.db_connect() as connection:
            cursor = connection.cursor()
            if self.check_exists_image_path(old_images_path) is not False:
                cursor.execute(f"UPDATE {database_config.TABLE_IMAGE_NAME} SET \
                {database_config.COLUMN_IMAGE_PATH}=? WHERE {database_config.COLUMN_IMAGE_PATH}=?", (
                        new_images_path, # this is new image name
                        old_images_path  # this is old image name
                    )); connection.commit() # commit

    def export_query(self, folder_name):
        folder_path = self.get_folder_path(folder_name)
        tags = self.tags_view(folder_name)
        working_directory = os.getcwd()
        for tag in tags:
            tag_name = tag.tag_name # get tag name
            images = self.images_view_by_tag(tag_name, folder_name) # get images path by tag
            for image in images:
                os.chdir(folder_path) # change directory to folder path
                _folder_path = os.path.join(folder_path, tag_name) # join tag name to folder path
                _image_path = image.image_path # get image path from image
                try:
                    # make directory or create folder with geted tag name
                    os.makedirs(tag_name)
                except FileExistsError as error:
                    print (error)
                finally:
                    # copy image path from tag to created folder tag
                    shutil.copy(_image_path,
                        _folder_path
                    )
                # reverse to main directory
                os.chdir(working_directory)
