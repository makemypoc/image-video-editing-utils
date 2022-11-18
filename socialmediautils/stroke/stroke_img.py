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
    global visual_debug
    visual_debug = enable
    if (visual_debug is True):
        if not os.path.exists('debug'):
            os.makedirs('debug')


def zoom_mask(mask_img: Any, zoom_factor: float = 1.05, angle: int = 0, zoom_option: int = 1) -> Any:

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


def add_img_stroke(model_session: Any, in_file_path: str, out_file_path: str,
                   color: Union[List[int], Tuple[int, int, int]],
                   zooming_factor: float) -> None:
    global visual_debug

    RChannel, GChannel, BChannel = color

    img_org = cv2.imread(in_file_path)
    Img_org_mask = remove(img_org, session=model_session, alpha_matting=False, only_mask=True,
                          post_process_mask=True)

    img_scale_mask = zoom_mask(Img_org_mask, zooming_factor)
    Img_overlay_mask = cv2.bitwise_xor(Img_org_mask, img_scale_mask)

    img_blend_color = np.zeros([img_org.shape[0], img_org.shape[1], 3], dtype=np.uint8)
    img_blend_color[:, :] = [BChannel, GChannel, RChannel]

    img_blended = overlay_img(img_org, img_blend_color, Img_overlay_mask)

    if (visual_debug is True):
        cv2.imwrite(os.path.join('debug', 'd001_overlay_image.png'), img_blend_color)
        cv2.imwrite(os.path.join('debug', 'd002_unet2_mask_image.png'), Img_org_mask)
        cv2.imwrite(os.path.join('debug', 'd003_unet2_mask_scaled_image.png'), img_scale_mask)
        cv2.imwrite(os.path.join('debug', 'd004_overlay_mask_image.png'), Img_overlay_mask)
        cv2.imwrite(os.path.join('debug', 'd005_overlay_image.png'), img_blended)

    cv2.imwrite(out_file_path, img_blended)
