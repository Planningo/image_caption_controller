import os

def get_caption_file_name(file_name:str,caption_file_type:str):
    image_type = file_name.split('.')[-1]
    return file_name.replace(image_type,caption_file_type)

def get_file_names_only_has_caption(files_dir:str,caption_file_type:str):
    def check_has_caption(file_name):
        if caption_file_type in file_name:
            return False
        caption_file_name = get_caption_file_name(file_name,caption_file_type)
        return os.path.exists(os.path.join(files_dir,caption_file_name))
    
    return [file_name for file_name in os.listdir(files_dir) if check_has_caption(file_name)] 