class Folder:
    def __init__(self, id, folder_name, folder_path):
        self.id = id
        self.folder_name = folder_name
        self.folder_path = folder_path

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id

    def get_folder_name(self):
        return self.folder_name

    def set_folder_name(self, new_folder_name):
        self.folder_name = new_folder_name

    def get_folder_name(self):
        return self.folder_name

    def set_folder_path(self, new_folder_path):
        self.folder_path = new_folder_path
