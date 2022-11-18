from socialmediautils import stroke
from typing import Any

import argparse
import os
import numpy as np

from colour import Color
from datetime import datetime


def main(args: Any) -> None:

    image_names: list = []
    input_images: list = []
    output_images: list = []
    total_processing_images = 0

    input_folder_path = args.input_folder
    input_file = args.input_file
    output_folder_path = args.output_folder

    if args.model_name not in ['u2net_human_seg', 'u2netp']:
        print('This model is not supported! Please check the correct model name')
        exit()

    elif input_folder_path == '':
        if not os.path.isfile(input_file):
            print('This input file is not valid! Please check the correct path with file name')
            exit()
        else:
            input_images[0] = input_file
            output_images[0] = os.path.join(output_folder_path, os.path.basename(input_file))

    elif input_folder_path != '':

        image_names = os.listdir(input_folder_path)

        for file in image_names:
            if file.endswith(('png', 'jpg', 'jpeg')):
                input_images.append(os.path.join(input_folder_path, file))
                output_images.append(os.path.join(output_folder_path, file))

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    total_processing_images = len(input_images)

    model_session = stroke.get_stroke_session(args.model_name)
    if args.vdebug:
        stroke.enable_visual_debug(True)

    for img_index in range(total_processing_images):
        print('\nStarted processing file named {} {}/{}'.format(image_names[img_index], img_index + 1,
              total_processing_images))

        stroke_color = np.interp(Color(args.color).get_rgb(), [0, 1], [0, 255]).astype('uint8').tolist()

        stroke.add_img_stroke(model_session, input_images[img_index], output_images[img_index], stroke_color, 1.07)


def parse_args() -> Any:
    """Parse input arguments."""

    parser = argparse.ArgumentParser(description='Add outline stroking to the human image for appealing visual')
    parser.add_argument('-m', '--model_name', type=str, default='u2net_human_seg',
                        help='key in the supported model name [u2net_human_seg, u2netp]')
    parser.add_argument('-d', '--input_folder', type=str, default='sample', help='input directory path.')
    parser.add_argument('-i', '--input_file', default='sample/me.jpg',
                        type=str, help='image file with human to be stroked.')
    parser.add_argument('-o', '--output_folder', type=str,
                        default=datetime.now().strftime("%Y%m%d-%H%M%S"), help='CSV data file name with full path.')
    parser.add_argument('-c', '--color', type=str, default='yellow', help='Feed the color as per W3C color naming')
    parser.add_argument('-p', '--vdebug', type=bool, default=False, help='storing the debug images in the debug folder')

    args = parser.parse_args()

    print('\n\n\n!!! Outline stroking functionality for the human images !!!\n\n')
    print('Starting the Application with instance ID:', datetime.now().strftime("%Y%m%d-%H%M%S"))
    return args


if __name__ == '__main__':
    """ Entry point """
    main(parse_args())
