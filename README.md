# image_caption_controller

A Python app for check image data caption result, edit caption and delete. (can use in Mac too!)

### `Train image files and caption files have to be in same directory with same name but different type.`

(for example: images/A.png ,images/A.txt,images/b.jpg ,images/A.txt,...)

# License

This code is licensed under the MIT License. See [here](https://github.com/brilam/remove-bg/blob/master/LICENSE) for more details.

# Installation

```
git clone https://github.com/Planningo/image_caption_controller.git
cd image_caption_controller
pip install -r requiremetns.txt
```

# Start app

`python3 main.py --dir {your images and caption dir}`

# Usage

### `check and edit caption of the image, and delete the data set in the directory`

press arrow left and right to view images, `cmd+backspace` in mac can delete the image without click the button.

| Parameter         | Default Value | Description                                                                                                                                     |
| ----------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| dir               | req. param    | path to the image and caption data set                                                                                                          |
| caption_file_type | `'txt'`       | file type of the caption file                                                                                                                   |
| start_index       | `0`           | initial start index of the dataset                                                                                                              |
| preload_range     | `10`          | Numbers of preload range. if 10, range current index -10 to current index +10 images would be preloaded, this if for image dataset in the cloud |

# Contributions

Contributions and feature requests are always welcome.
