""" This module implements the outline stroke feature for human in the given images
"""
from rembg import remove
from typing import Any
from typing import Tuple
from typing import List
from typing import Union

import os
import cv2
import numpy as np

visual_debug = False


def enable_visual_debug(enable: bool) -> None:
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


def zoom_mask(mask_img: Any, zoom_factor: float = 1.05, angle: int = 0, zoom_option: int = 1) -> Any:
    """
    It scales the mask image to the given zoom factor as per the zoom option algorithm. This scaling
    is center focused regardles of the zoom option provided.

    :param mask_img: Numpy array that holds the mask image
    :type mask_img: Any
    :param zoom_factor: Scaling factor of the image. If 2 is provided, it scales the image twice,
    defaults to 1.05
    :type zoom_factor: float, optional
    :param angle: Rotating angle of the image for the zoom option 1, defaults to 0
    :type angle: int, optional
    :param zoom_option: It gives the option to select the zooming algorithm. If 1 then it is zooming
    with rotation of the image capability. If 2 then it just zooming. In both cases the zooming is
    centered around the midpoint of the image, defaults to 1
    :type zoom_option: int, optional
    :return: Returns the scaled mask image
    :rtype: Any
    """
    height, width = mask_img.shape

    if (zoom_option == 1):
        centerY, centerX = [i / 2 for i in mask_img.shape[:]]
        rot_mat = cv2.getRotationMatrix2D((centerX, centerY), angle, zoom_factor)
        result = cv2.warpAffine(mask_img, rot_mat, (width, height), flags=cv2.INTER_LANCZOS4)

    elif (zoom_option == 2):
        centerX, centerY = int(height / 2), int(width / 2)
        radiusX, radiusY = int(zoom_factor * centerX), int(zoom_factor * centerY)
        minX, maxX = abs(centerX - radiusX), abs(centerX + radiusX)
        minY, maxY = abs(centerY - radiusY) , abs(centerY + radiusY)

        cropped = mask_img[minX:maxX, minY:maxY]
        result = cv2.resize(cropped, (width, height))

    else:
        rot_mat = cv2.getRotationMatrix2D((centerX, centerY), angle, zoom_factor)
        result = cv2.warpAffine(mask_img, rot_mat, (height, width), flags=cv2.INTER_LANCZOS4)

    return result


def overlay_img(base_img: Any, overlay_img: Any, mask: Any) -> Any:
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

    fg_img = cv2.bitwise_or(overlay_img, overlay_img, mask=mask)

    mask_inv = cv2.bitwise_not(mask)
    bg_img = cv2.bitwise_or(base_img, base_img, mask=mask_inv)

    overlaid_img = cv2.bitwise_or(fg_img, bg_img)

    if (visual_debug is True):
        cv2.imwrite(os.path.join('debug', 'd004_01_foreground_image_mask.png'), mask)
        cv2.imwrite(os.path.join('debug', 'd004_02_foreground_image.png'), fg_img)
        cv2.imwrite(os.path.join('debug', 'd004_03_background_image_mask.png'), mask_inv)
        cv2.imwrite(os.path.join('debug', 'd004_04_background_image.png'), bg_img)

    return overlaid_img


def overlay_img_with_bg(base_img: Any, bg_img: Any, stroke_color_img: Any, base_mask: Any, bg_inv_mask: Any,
                        stroke_mask: Any) -> Any:
    """
    It merges the background and the forground based on the orignal, backgound, colored and mask images.

    :param base_img: This image that holds the human in it.
    :type base_img: Any
    :param bg_img: It is the image that holds the scenic background.
    :type bg_img: Any
    :param stroke_color_img: This is the colored image based on stroke color.
    :type stroke_color_img: Any
    :param base_mask: This is the mask image which is the segmented version of human without scaling
    :type base_mask: Any
    :param bg_inv_mask: This is the mask image which is the segmented version of human with scaling
    :type bg_inv_mask: Any
    :param stroke_mask: it is the mask of the stroke area
    :type stroke_mask: Any
    :return: It returns the final image that has both stroked human with background
    :rtype: Any
    """
    global visual_debug

    stroke_img = cv2.bitwise_or(stroke_color_img, stroke_color_img, mask=stroke_mask)
    human_img = cv2.bitwise_or(base_img, base_img, mask=base_mask)
    stroke_human_img = cv2.bitwise_or(human_img, stroke_img)

    bg_mask = cv2.bitwise_not(bg_inv_mask)
    bg_img_filtered = cv2.bitwise_or(bg_img, bg_img, mask=bg_mask)

    overlaid_img = cv2.bitwise_or(stroke_human_img, bg_img_filtered)

    if (visual_debug is True):
        cv2.imwrite(os.path.join('debug', 'd004_01_foreground_stroke_image.png'), stroke_img)
        cv2.imwrite(os.path.join('debug', 'd004_02_foreground_human_image.png'), human_img)
        cv2.imwrite(os.path.join('debug', 'd004_03_background_stroke_human_image.png'), stroke_human_img)
        cv2.imwrite(os.path.join('debug', 'd004_04_background_image.png'), bg_img)
        cv2.imwrite(os.path.join('debug', 'd004_04_background_image_mask.png'), bg_mask)
        cv2.imwrite(os.path.join('debug', 'd004_04_background_filtered_image.png'), bg_img_filtered)

    return overlaid_img


def add_img_stroke(model_session: Any, in_file_path: str, out_file_path: str,
                   color: Union[List[int], Tuple[int, int, int]],
                   zooming_factor: float) -> None:
    """
    This utility function implements the outline stroking feature for any human in the given
    image.

    :param model_session: The session that holds what unet2 familiy of the model to be used
    :type model_session: Any
    :param in_file_path: It is the input path of the file to be processed
    :type in_file_path: str
    :param out_file_path: It is the ouput path where the merged image has to be placed
    :type out_file_path: str
    :param color: This color indicated the color of the stroke area
    :type color: Union[List[int], Tuple[int, int, int]]
    :param zooming_factor: It is the scaling factor to determing the outline stroke thickness.
    Always use the value between 1.01 to 1.09
    :type zooming_factor: float
    """
    global visual_debug

    RChannel, GChannel, BChannel = color

    img_org = cv2.imread(in_file_path)
    img_org_mask = remove(img_org, session=model_session, alpha_matting=False, only_mask=True,
                          post_process_mask=True)

    img_scale_mask = zoom_mask(img_org_mask, zooming_factor)
    Img_overlay_mask = cv2.bitwise_xor(img_org_mask, img_scale_mask)

    img_blend_color = np.zeros([img_org.shape[0], img_org.shape[1], 3], dtype=np.uint8)
    img_blend_color[:, :] = [BChannel, GChannel, RChannel]

    img_blended = overlay_img(img_org, img_blend_color, Img_overlay_mask)

    if (visual_debug is True):
        cv2.imwrite(os.path.join('debug', 'd001_overlay_image.png'), img_blend_color)
        cv2.imwrite(os.path.join('debug', 'd002_unet2_mask_image.png'), img_org_mask)
        cv2.imwrite(os.path.join('debug', 'd003_unet2_mask_scaled_image.png'), img_scale_mask)
        cv2.imwrite(os.path.join('debug', 'd004_overlay_mask_image.png'), Img_overlay_mask)
        cv2.imwrite(os.path.join('debug', 'd005_overlay_image.png'), img_blended)

    cv2.imwrite(out_file_path, img_blended)


def add_img_stroke_with_bg(model_session: Any, in_file_path: str, bg_file_path: str,
                           out_file_path: str,
                           color: Union[List[int], Tuple[int, int, int]],
                           zooming_factor: float) -> None:
    """
    This utility function implements the outline stroking feature for any human and superimpose the stroked
    human with scenic (sort of) background image.

    :param model_session: The session that holds what unet2 familiy of the model to be used
    :type model_session: Any
    :param in_file_path: It is the input path of the file with human image to be processed
    :type in_file_path: str
    :param bg_file_path: This image path that holds the scenic (or some sort of) backgorund information
    :type bg_file_path: str
    :param out_file_path: It is the ouput path where the merged image has to be placed
    :type out_file_path: str
    :param color: This color indicated the color of the stroke area
    :type color: Union[List[int], Tuple[int, int, int]]
    :param zooming_factor: It is the scaling factor to determing the outline stroke thickness.
    Always use the value between 1.01 to 1.09
    :type zooming_factor: float
    """
    global visual_debug

    RChannel, GChannel, BChannel = color

    img_org = cv2.imread(in_file_path)
    Img_org_mask = remove(img_org, session=model_session, alpha_matting=False, only_mask=True,
                          post_process_mask=True)

    img_scale_mask = zoom_mask(Img_org_mask, zooming_factor)
    img_overlay_mask = cv2.bitwise_xor(Img_org_mask, img_scale_mask)

    img_blend_color = np.zeros([img_org.shape[0], img_org.shape[1], 3], dtype=np.uint8)
    img_blend_color[:, :] = [BChannel, GChannel, RChannel]

    img_bg = cv2.resize(cv2.imread(bg_file_path), (img_org.shape[1], img_org.shape[0]),
                        interpolation=cv2.INTER_LINEAR)

    img_blended = overlay_img_with_bg(img_org, img_bg, img_blend_color, Img_org_mask, img_scale_mask, img_overlay_mask)

    if (visual_debug is True):
        cv2.imwrite(os.path.join('debug', 'd001_overlay_image.png'), img_blend_color)
        cv2.imwrite(os.path.join('debug', 'd002_unet2_mask_image.png'), Img_org_mask)
        cv2.imwrite(os.path.join('debug', 'd003_unet2_mask_scaled_image.png'), img_scale_mask)
        cv2.imwrite(os.path.join('debug', 'd004_stroke_mask_image.png'), img_overlay_mask)
        cv2.imwrite(os.path.join('debug', 'd005_overlay_image.png'), img_blended)

    cv2.imwrite(out_file_path, img_blended)
