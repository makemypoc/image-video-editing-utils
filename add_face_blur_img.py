""" This module is the usage example of the face blurring feature using face parser for human in the given images
and superimpose the blurrred face with the rest
"""
from socialmediautils import blur
from typing import Any

import argparse
import os
import numpy as np
import random

from datetime import datetime


def main(args: Any) -> None:
    '''
    This function executes the process for making face blurring to the human face for either a
    single image or the given set of images in the folder

    :param args: It holds the user given arguments for controlling the program flow as per the
    user expectation
    :type args: Any
    '''
    image_names: list = []
    input_images: list = []
    output_images: list = []
    total_processing_images = 0

    input_folder_path = args.input_folder
    input_file = args.input_file
    output_folder_path = args.output_folder

    if args.model_name not in ['bisenet']:
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

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    total_processing_images = len(input_images)

    if args.vdebug:
        blur.enable_visual_debug_fb(True)

    model_session, dev_accl = blur.get_face_parser_model(args.model_name)

    for img_index in range(total_processing_images):
        print('\nStarted processing file named {} {}/{}'.format(input_images[img_index], img_index + 1,
              total_processing_images))

        blur.add_face_blur(model_session, dev_accl, input_images[img_index], output_images[img_index], 25)


def parse_args() -> Any:
    """This function recieves and parses the input arguments.

    :return: Argument parser that holds the user input to this program
    :rtype: Any
    """
    parser = argparse.ArgumentParser(description='Add face blurring to the human face images')
    parser.add_argument('-m', '--model_name', type=str, default='bisenet',
                        help='key in the supported model name [bisenet]')
    parser.add_argument('-d', '--input_folder', type=str, default='',
                        help='input directory path for human face images.')
    parser.add_argument('-i', '--input_file', default='sample/input/me.png',
                        type=str, help='input file path for single human face image.')
    parser.add_argument('-o', '--output_folder', type=str,
                        default=datetime.now().strftime("%Y%m%d-%H%M%S"), help='Folder where the output is stored.')
    parser.add_argument('-b', '--blur_factor', type=int, default=33, help='Feed the blurring factor')
    parser.add_argument('-p', '--vdebug', type=bool, default=False, help='storing the debug images in the debug folder')

    args = parser.parse_args()

    print('\n\n\n!!! Face blurring functionality using face parser for the human images !!!\n\n')
    print('Starting the Application with instance ID:', datetime.now().strftime("%Y%m%d-%H%M%S"))
    return args


if __name__ == '__main__':
    """
    This is the entry point of the program
    """
    main(parse_args())
