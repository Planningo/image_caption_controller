from tkinter import *
import customtkinter
from ui.base_ui import ControllerUI
import sys
import os 

def run():
    # data_dir = sys.argv[1]
    # if not os.path.exists(data_dir):
    #     raise Exception(f'there is no directory {data_dir}')
    dir = '/Users/planningo/Library/CloudStorage/GoogleDrive-ksw1996121@planningo.io/Shared drives/Planningo/photio_sd_model/images/30_photio'
    ui = ControllerUI(dir)
    ui.init_ui()
    
    ui.root.mainloop()

if __name__ =='__main__':
    run()

