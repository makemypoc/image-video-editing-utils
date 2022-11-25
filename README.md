# About

 This repo helps editing the images and or videos. There are some utilities available for making social media content look appealing.

 [Image stroke feature explanation video in English](https://youtu.be/vCa1K3FmNr8)

 [Image stroke feature explanation video in Tamil](https://youtu.be/it19s6FjSRA)

## Package Name: socialmediautils

 This package implements the various utilities for making social media content

## Sub Package Name: stroke

 This sub package implements the outline stroke feature for human in the given images and videos

### Module: stroke_img

 This module implements the outline stroke feature for human in the given set of images

### Module Usage: add_stroke_img

```python
def parse_args() -> Any:
    """This function recieves and parses the input arguments.

    :return: Argument parser that holds the user input to this program
    :rtype: Any
    """
    parser = argparse.ArgumentParser(description='Add outline stroking to the human image for appealing visual')
    parser.add_argument('-m', '--model_name', type=str, default='u2net_human_seg',
                        help='key in the supported model name [u2net_human_seg, u2netp]')
    parser.add_argument('-d', '--input_folder', type=str, default='sample', help='input directory path.')
    parser.add_argument('-i', '--input_file', default='sample/me.png',
                        type=str, help='image file with human to be stroked.')
    parser.add_argument('-o', '--output_folder', type=str,
                        default=datetime.now().strftime("%Y%m%d-%H%M%S"), help='CSV data file name with full path.')
    parser.add_argument('-c', '--color', type=str, default='yellow', help='Feed the color as per W3C color naming')
    parser.add_argument('-p', '--vdebug', type=bool, default=False, help='storing the debug images in the debug folder')

    args = parser.parse_args()

    print('\n\n\n!!! Outline stroking functionality for the human images !!!\n\n')
    print('Starting the Application with instance ID:', datetime.now().strftime("%Y%m%d-%H%M%S"))
    return args
```
