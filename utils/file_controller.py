import os

from utils.lib import get_caption_file_name

class FileController:

    def __init__(self,folder_dir:str,caption_file_type:str) -> None:
        self.folder_dir = folder_dir
        self.caption_file_type = caption_file_type

    def remove_data(self,file_name):
        os.remove(os.path.join(self.folder_dir,file_name))
        os.remove(os.path.join(self.folder_dir,get_caption_file_name(file_name,self.caption_file_type)))

    def save_caption(self,file_name,data):
        with open(os.path.join(self.folder_dir,file_name),'w') as file:
            file.write(data)
