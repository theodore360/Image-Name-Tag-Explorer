class Image:
    def __init__(self, id, image_path, tag_id):
        self.id = id
        self.image_path = image_path
        self.tag_id = tag_id

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id

    def get_image_path(self):
        return self.image_path

    def set_image_path(self, new_image_path):
        self.image_path = new_image_path

    def get_tag_id(self):
        return self.tag_id

    def set_tag_id(self, new_tag_id):
        self.tag_id = new_tag_id
