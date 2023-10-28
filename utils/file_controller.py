import os
from PIL import Image
from utils.lib import get_caption_file_name
import threading


def get_nearby_elements(input_list, current_index, range_length):
    result = []
    list_length = len(input_list)

    for i in range(current_index - range_length, current_index + range_length + 1):
        index = (
            i % list_length
        )  # Ensure the index wraps around if it goes out of bounds
        result.append(input_list[index])

    return result


class FileController:
    def __init__(
        self, folder_dir: str, caption_file_type: str, range_length: int
    ) -> None:
        self.folder_dir = folder_dir
        self.caption_file_type = caption_file_type
        self.preload_image_range_length = range_length

    def remove_data(self, file_name):
        os.remove(os.path.join(self.folder_dir, file_name))
        os.remove(
            os.path.join(
                self.folder_dir,
                get_caption_file_name(file_name, self.caption_file_type),
            )
        )

    def save_caption(self, file_name, data):
        with open(os.path.join(self.folder_dir, file_name), "w") as file:
            file.write(data)

    def preload_images(self, file_list: list, current_index: int):
        def load_data(file_dir: str):
            Image.open(file_dir)
            file_type = file_dir.split(".")[-1]
            open(file_dir.replace(file_type, "txt"))

        threads = []
        filter_range = self.preload_image_range_length

        preload_list = [
            os.path.join(self.folder_dir, file_name)
            for file_name in get_nearby_elements(file_list, current_index, filter_range)
        ]

        for target_file_dir in preload_list:
            t = threading.Thread(target=load_data, args=(target_file_dir,))
            t.start()
            threads.append(t)

        # for t in threads:
        #     t.join()
