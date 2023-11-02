from customtkinter import CTk, CTkButton, CTkImage, CTkLabel, CTkTextbox
from CTkMessagebox import CTkMessagebox
from tkinter import END
from PIL import Image
import os
from utils.file_controller import FileController
from utils.lib import get_file_names_only_has_caption, get_caption_file_name


def get_resized_image(image_dir, max_height=600):
    pil_image = Image.open(image_dir)
    pixels_x, pixels_y = tuple(
        [int(max_height / pil_image.size[1] * x) for x in pil_image.size]
    )
    return pil_image.resize((pixels_x, pixels_y))


class ControllerUI:
    def __init__(
        self, folder_dir: str, caption_file_type="txt", start_index=0, preload_range=10
    ):
        self.window_size = "1000x900"
        self.root = CTk()
        self.root.title("Image Caption Controller")
        self.folder_dir = folder_dir
        self.caption_file_type = caption_file_type
        self.image_captioned_list = get_file_names_only_has_caption(
            folder_dir, caption_file_type
        )
        self.current_data_index = start_index
        self.file_controller = FileController(
            folder_dir, caption_file_type, preload_range
        )
        self.caption_changed = False
        self.initial_caption = ''

    def init_ui(self) -> None:
        self.root.geometry(self.window_size)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=100)
        self.root.grid_rowconfigure(2, weight=50)
        self.root.grid_rowconfigure(3, weight=1)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.titlebox = CTkLabel(
            master=self.root,
            bg_color= 'white',
            corner_radius=5,
        )
        self.root.titlebox.grid(
            row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=2
        )
        self.root.titlebox.configure(text = self.image_captioned_list[self.current_data_index])

        self.root.numberbox = CTkLabel(
            master=self.root,
            corner_radius=5,
            bg_color= 'white',
        )
        self.root.numberbox.grid(
            row=0, column=2, padx=20, pady=20, sticky="nsew"
        )
        self.root.numberbox.configure(text = f'{self.current_data_index}/{len(self.image_captioned_list)}')

        pil_image = get_resized_image(
            os.path.join(
                self.folder_dir, self.image_captioned_list[self.current_data_index]
            )
        )
        ctk_image = CTkImage(light_image=pil_image, size=pil_image.size)
        self.image_label = CTkLabel(
            master=self.root,
            image=ctk_image,
            text="",
        )
        self.image_label.grid(
            column=0, row=1, padx=20, pady=20, columnspan=3, rowspan=1
        )

        f = open(
            os.path.join(
                self.folder_dir,
                get_caption_file_name(
                    self.image_captioned_list[self.current_data_index],
                    self.caption_file_type,
                ),
            ),
            "r",
        )
        data = f.read()
        self.initial_caption = data
        f.close()
        self.root.textbox = CTkTextbox(
            master=self.root,
            corner_radius=5,
            undo=True,
            autoseparators=True,
            maxundo=-1,
        )
        self.root.textbox.grid(
            row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=3
        )
        self.root.textbox.insert("0.0", data)


        button = CTkButton(master=self.root, text="Prev", command=self.prev_index)
        button.grid(row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=1)

        button = CTkButton(master=self.root, text="Next", command=self.next_index)
        button.grid(row=3, column=1, padx=20, pady=20, sticky="ew", columnspan=1)

        button = CTkButton(
            master=self.root,
            text="Delete",
            command=self.delete_confirm_modal,
            fg_color="red",
            hover_color="orange",
        )
        button.grid(row=3, column=2, padx=20, pady=20, sticky="ew", columnspan=1)

        self.root.bind("<Key>", self.on_key_down)

        self.file_controller.preload_images(
            self.image_captioned_list, self.current_data_index
        )

    def show_image(self, image_dir: str) -> None:
        pil_image = get_resized_image(image_dir)
        ctk_image = CTkImage(light_image=pil_image, size=pil_image.size)
        self.image_label.configure(image=ctk_image, text="")

    def caption_edited(self, e):
        self.caption_changed = True

    def show_caption(self, caption_dir: str) -> None:
        f = open(caption_dir, "r")
        data = f.read()
        self.initial_caption = data
        f.close()
        self.root.textbox.delete("0.0", END)
        self.root.textbox.insert("0.0", data)

    def next_index(self) -> None:
        self.set_index(self.current_data_index + 1)

    def prev_index(self) -> None:
        self.set_index(self.current_data_index - 1)

    def set_index(self, index) -> None:
        if self.root.textbox.edit_modified() and self.initial_caption != self.root.textbox.get("1.0", END).strip():
            self.file_controller.save_caption(
                get_caption_file_name(
                    self.image_captioned_list[self.current_data_index],
                    self.caption_file_type,
                ),
                self.root.textbox.get("1.0", END).strip(),
            )
        self.caption_changed = False

        if index >= len(self.image_captioned_list):
            index -= len(self.image_captioned_list)
        elif index < 0:
            index += len(self.image_captioned_list)
        self.current_data_index = index
        self.set_data()

    def set_data(self) -> None:
        self.show_image(
            os.path.join(
                self.folder_dir, self.image_captioned_list[self.current_data_index]
            )
        )
        self.show_caption(
            os.path.join(
                self.folder_dir,
                get_caption_file_name(
                    self.image_captioned_list[self.current_data_index],
                    self.caption_file_type,
                ),
            )
        )

        self.file_controller.preload_images(
            self.image_captioned_list, self.current_data_index
        )
        self.set_header()
    
    def set_header(self) -> None:
        self.root.titlebox.configure(text = self.image_captioned_list[self.current_data_index])
        self.root.numberbox.configure(text= f'{self.current_data_index}/{len(self.image_captioned_list)}')


    def delete_confirm_modal(self):
        msg = CTkMessagebox(
            title="Delete this image data!",
            message="Are you sure?",
            icon="warning",
            option_1="Cancel",
            option_2="Delete",
            option_focus=2,
        )
        if msg.get() == "Delete":
            print("delete", self.image_captioned_list[self.current_data_index])
            self.file_controller.remove_data(
                self.image_captioned_list[self.current_data_index]
            )
            del self.image_captioned_list[self.current_data_index]
            self.set_data()
            # self.root.bind("<Key>", self.on_key_down)
        # self.root.bind("<Key>", self.on_key_down)
        def on_end():
            self.root.grab_set()
            self.root.textbox.focus_set()
        msg.after_cancel(on_end)
        msg.after_idle(on_end)
        
        
    def on_key_down(self, e):
        if e.keysym == "Right":
            self.next_index()
        elif e.keysym == "Left":
            self.prev_index()
        elif e.keysym == "BackSpace" and e.state == 8:
            self.delete_confirm_modal()
