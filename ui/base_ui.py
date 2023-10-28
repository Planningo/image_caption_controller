from customtkinter import CTk,CTkButton,CTkImage,CTkLabel,CTkTextbox
from tkinter import *
from PIL import Image
import os
from utils.file_controller import FileController
from utils.lib import get_file_names_only_has_caption,get_caption_file_name



class ControllerUI:

    def __init__(self,folder_dir:str,caption_file_type='txt',start_index=0):
        self.window_size = "1000x900"
        self.root = CTk()
        self.folder_dir = folder_dir
        self.caption_file_type = caption_file_type
        self.image_captioned_list =get_file_names_only_has_caption(folder_dir,caption_file_type) 
        self.current_data_index = self.set_index(start_index) 
        self.file_controller = FileController(folder_dir,caption_file_type)
        self.caption_changed = False

    def init_ui(self)->None:
        self.root.geometry(self.window_size)

        self.root.grid_rowconfigure(0, weight=10)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=1)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        button = CTkButton(master=self.root, text='Hello World!')
        button.grid(row=2, column=0, padx=20,pady=20, sticky="ew", columnspan=1)

        button = CTkButton(master=self.root, text='Hello World!')
        button.grid(row=2, column=1, padx=20,pady=20, sticky="ew", columnspan=1)

        button = CTkButton(master=self.root, text='Hello World!')
        button.grid(row=2, column=2, padx=20,pady=20, sticky="ew", columnspan=1)

        self.root.bind('<Key>',self.on_key_down)


        self.set_data(self.current_data_index)
  
    def set_image(self,image_dir:str)->None:
        pil_image = Image.open(image_dir)
        max_height = 600
    
        pixels_x, pixels_y = tuple([int(max_height/pil_image.size[1] * x)  for x in pil_image.size])
        pil_image = pil_image.resize((pixels_x, pixels_y))
        ctk_image = CTkImage(light_image=pil_image, size=pil_image.size)
        label = CTkLabel(master=self.root, image=ctk_image, text='')
        label.grid(column=0, row=0,padx=20,pady=20,columnspan=3,rowspan=1)

    def caption_edited(self,e):
        self.caption_changed = True

    def set_caption(self,caption_dir:str)->None:
        f = open(caption_dir, 'r')
        data = f.read()
        self.root.textbox = CTkTextbox(master=self.root,  corner_radius=5,undo=True,autoseparators=True,maxundo=-1)
        self.root.textbox.grid(row=1, column=0,padx=20,pady=20, sticky="nsew",columnspan=3)
        self.root.textbox.insert("0.0",data)
        self.root.textbox.bind('<Key>',self.caption_edited)
        f.close()

    def set_index(self,index)->int:
        if index> len(self.image_captioned_list):
            index -= len(self.image_captioned_list)
        elif index < 0:
            index += len(self.image_captioned_list)
        return index

    def set_data(self,index:int)->None:
        self.set_image(os.path.join(self.folder_dir,self.image_captioned_list[index]))
        self.set_caption(os.path.join(self.folder_dir,get_caption_file_name(self.image_captioned_list[index],self.caption_file_type)))

    def on_key_down(self,e):
        if(e.keysym=='Right'):
            self.set_index(self.current_data_index+1)
        elif (e.keysym=='Left'):
            self.set_index(self.current_data_index+1)
        elif (e.keysym=='Delete' or e.keysym=='BackSpace'):
            
        print(e)
        print(e.keysym, )
