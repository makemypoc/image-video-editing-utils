""" This module is the usage example of the outline stroke feature for human in the given images and superimpose
the stroked human with the background image
"""
from socialmediautils import stroke
from typing import Any

import argparse
import os
import numpy as np
import random

from colour import Color
from datetime import datetime


def main(args: Any) -> None:
    '''
    This function executes the process for making stroke over the border of human for either a
    single image or the given set of images in the folder

    :param args: It holds the user given arguments for controlling the program flow as per the
    user expectation
    :type args: Any
    '''
    image_names: list = []
    input_images: list = []
    bg_images: list = []
    output_images: list = []
    total_bg_images_max_index = 0
    total_processing_images = 0

    input_folder_path = args.input_folder
    input_file = args.input_file
    bg_folder_path = args.bg_folder
    bg_file = args.bg_file
    output_folder_path = args.output_folder

    if args.model_name not in ['u2net_human_seg', 'u2netp']:
        print('This model is not supported! Please check the correct model name')
        exit()

    elif input_folder_path == '':
        if not os.path.isfile(input_file):
            print('This input file is not valid! Please check the correct path with file name')
            exit()
        else:
            input_images.append(input_file)
            output_images.append(os.path.join(output_folder_path, os.path.basename(input_file)))

    elif input_folder_path != '':

        image_names = os.listdir(input_folder_path)

        for file in image_names:
            if file.endswith(('png', 'jpg', 'jpeg')):
                input_images.append(os.path.join(input_folder_path, file))
                output_images.append(os.path.join(output_folder_path, file))

    if bg_file != '':
        if not os.path.isfile(bg_file):
            print('This background image file is not valid! Please check the correct path with file name')
            exit()
        else:
            bg_images.append(bg_file)

    elif bg_folder_path != '':
        bg_names = os.listdir(bg_folder_path)

        for file in bg_names:
            if file.endswith(('png', 'jpg', 'jpeg')):
                bg_images.append(os.path.join(bg_folder_path, file))

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    total_processing_images = len(input_images)
    total_bg_images_max_index = len(bg_images)

    model_session = stroke.get_stroke_session(args.model_name)
    if args.vdebug:
        stroke.enable_visual_debug(True)

    for img_index in range(total_processing_images):
        print('\nStarted processing file named {} {}/{}'.format(input_images[img_index], img_index + 1,
              total_processing_images))

        stroke_color = np.interp(Color(args.color).get_rgb(), [0, 1], [0, 255]).astype('uint8').tolist()

        if len(bg_images) != 0:
            stroke.add_img_stroke_with_bg(model_session, input_images[img_index],
                                          bg_images[random.randrange(total_bg_images_max_index)],
                                          output_images[img_index], stroke_color, 1.03)
        else:
            stroke.add_img_stroke(model_session, input_images[img_index], output_images[img_index], stroke_color, 1.03)


def parse_args() -> Any:
    """This function recieves and parses the input arguments.

    :return: Argument parser that holds the user input to this program
    :rtype: Any
    """
    parser = argparse.ArgumentParser(description='Add outline stroking to the human image for appealing visual')
    parser.add_argument('-m', '--model_name', type=str, default='u2net_human_seg',
                        help='key in the supported model name [u2net_human_seg, u2netp]')
    parser.add_argument('-d', '--input_folder', type=str, default='', help='input directory path for human images.')
    parser.add_argument('-i', '--input_file', default='sample/input/me.png',
                        type=str, help='input directory path for background images.')
    parser.add_argument('-g', '--bg_folder', default='',
                        type=str, help='image file with human to be stroked.')
    parser.add_argument('-b', '--bg_file', default='',
                        type=str, help='image file with human to be stroked.')
    parser.add_argument('-o', '--output_folder', type=str,
                        default=datetime.now().strftime("%Y%m%d-%H%M%S"), help='Folder where the output is stored.')
    parser.add_argument('-c', '--color', type=str, default='yellow', help='Feed the color as per W3C color naming')
    parser.add_argument('-p', '--vdebug', type=bool, default=False, help='storing the debug images in the debug folder')

    args = parser.parse_args()

    print('\n\n\n!!! Outline stroking functionality for the human images !!!\n\n')
    print('Starting the Application with instance ID:', datetime.now().strftime("%Y%m%d-%H%M%S"))
    return args


if __name__ == '__main__':
    """
    This is the entry point of the program
    """
    main(parse_args())
