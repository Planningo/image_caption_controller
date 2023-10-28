from ui.base_ui import ControllerUI
import sys
import os
import argparse

parser = argparse.ArgumentParser(
    description="image_caption_controller needs images folder dir"
)
parser.add_argument(
    "--dir",
    required=True,
    default="images",
    help="image and caption folder directory",
)
parser.add_argument(
    "--caption_file_type",
    required=False,
    default="txt",
    help="file type of caption default: txt",
)
parser.add_argument(
    "--start_index",
    required=False,
    default=0,
    help="index that want to start default: 0",
)
parser.add_argument(
    "--preload_range",
    required=False,
    default=10,
    help="""number of images that want to preload near from current index.
      its for images saved at clouds default: 10""",
)
args = parser.parse_args()


def run():
    ui = ControllerUI(
        args.dir,
        args.caption_file_type,
        args.start_index,
        args.preload_range,
    )
    ui.init_ui()

    ui.root.mainloop()


if __name__ == "__main__":
    run()
