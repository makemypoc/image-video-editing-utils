""" This module implements the face blurring feature for the given human face in the given images
"""
from facexlib.parsing import init_parsing_model
from facexlib.utils.misc import img2tensor
from torchvision.transforms.functional import normalize
from typing import Any
from typing import Tuple
from typing import List
from typing import Union

import os
import cv2
import numpy as np
import torch

visual_debug = False


def get_face_parser_model(model_type: str = 'bisenet') -> Any:
    """
    _summary_

    :param model_type: Name of the model, i.e., face parsing model is bisenet by default, defaults to 'bisenet'
    :type model_type: str, optional
    :return: returns the model net for the given model type. It is usually Bisenet in this case
    :rtype: Any
    """
    dev_acc = 'cuda' if torch.cuda.is_available() else 'cpu'
    net = init_parsing_model(model_name=model_type, device=dev_acc,
                             model_rootpath=os.path.join(os.path.expanduser('~'), '.iveu'))

    return net, dev_acc


def enable_visual_debug_fb(enable: bool) -> None:
    """
    This function invokes the visual debug infomration to be stored or not as image files.

    :param enable: It activates the visual debugging for testin purpose.
    :type enable: bool
    """
    global visual_debug
    visual_debug = enable
    if (visual_debug is True):
        if not os.path.exists('debug'):
            os.makedirs('debug')


def overlay_blurred_face(base_img: Any, face_blur_img: Any, mask: Any) -> Any:
    """
    It merges the background and the forground based on the orignal, colored and mask image.

    :param base_img: This image is the original image to be processed
    :type base_img: Any
    :param overlay_img: This is the generated image based on the stroke color
    :type overlay_img: Any
    :param mask: This image is the mask image that holds the stroke area
    :type mask: Any
    :return: It returns the merged image
    :rtype: Any
    """
    global visual_debug

    fg_img = cv2.bitwise_or(face_blur_img, face_blur_img, mask=mask)

    mask_inv = cv2.bitwise_not(mask)
    bg_img = cv2.bitwise_or(base_img, base_img, mask=mask_inv)

    overlaid_img = cv2.bitwise_or(fg_img, bg_img)

    if (visual_debug is True):
        cv2.imwrite(os.path.join('debug', 'd005_01_foreground_image_mask.png'), mask)
        cv2.imwrite(os.path.join('debug', 'd005_02_foreground_image.png'), fg_img)
        cv2.imwrite(os.path.join('debug', 'd005_03_background_image_mask.png'), mask_inv)
        cv2.imwrite(os.path.join('debug', 'd005_04_background_image.png'), bg_img)
        cv2.imwrite(os.path.join('debug', 'd005_05_output_resized.png'), overlaid_img)

    return overlaid_img


def add_face_blur(net: Any, dev_acc: str, in_file_path: str, out_file_path: str,
                  blurring_factor: int = 33) -> Any:
    """
    _summary_

    :param net: _description_
    :type net: Any
    :param dev_acc: _description_
    :type dev_acc: str
    :param in_file_path: _description_
    :type in_file_path: str
    :param out_file_path: _description_
    :type out_file_path: str
    :param blurring_factor: _description_, defaults to 33
    :type blurring_factor: int, optional
    :return: _description_
    :rtype: Any
    """
    global visual_debug

    img_org = cv2.imread(in_file_path)
    height, width = img_org.shape[:2]

    img_resized = cv2.resize(img_org, (512, 512), interpolation=cv2.INTER_LINEAR)
    img = img2tensor(img_resized.astype('float32') / 255., bgr2rgb=True, float32=True)
    normalize(img, (0.485, 0.456, 0.406), (0.229, 0.224, 0.225), inplace=True)

    if dev_acc == 'cuda':
        img = torch.unsqueeze(img, 0).cuda()
    elif dev_acc == 'cpu':
        img = torch.unsqueeze(img, 0)

    with torch.no_grad():
        face_parsed = net(img)[0]
    face_parsed = face_parsed.squeeze(0).cpu().numpy().argmax(0)

    mask_face = np.zeros((face_parsed.shape[0], face_parsed.shape[1]), dtype="uint8")
    rep = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17]
    mask_face = np.where(np.isin(face_parsed, rep), 255, mask_face)

    ksize = (blurring_factor, blurring_factor)
    img_input_blur = cv2.blur(img_resized, ksize)

    overlaid_img = overlay_blurred_face(img_resized, img_input_blur, mask_face)

    final_img = cv2.resize(overlaid_img, (width, height), interpolation=cv2.INTER_LINEAR)

    if (visual_debug is True):
        cv2.imwrite(os.path.join('debug', 'd001_input_image.png'), img_org)
        cv2.imwrite(os.path.join('debug', 'd002_input_resized.png'), img_resized)
        cv2.imwrite(os.path.join('debug', 'd003_face_mask.png'), mask_face)
        cv2.imwrite(os.path.join('debug', 'd004_input_blurred.png'), img_input_blur)
        cv2.imwrite(os.path.join('debug', 'd006_final.png'), final_img)

    cv2.imwrite(out_file_path, final_img)
