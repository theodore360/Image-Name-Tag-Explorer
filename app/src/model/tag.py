class Tag:
    def __init__(self, id, tag_name, folder_id):
        self.id = id
        self.tag_name = tag_name
        self.folder_id = folder_id

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id

    def get_tag_name(self):
        return self.tag_name

    def set_tag_name(self, new_tag_name):
        self.tag_name = new_tag_name

    def get_folder_id(self):
        return self.folder_id

    def set_folder_id(self, new_folder_id):
        self.folder_id = new_folder_id
