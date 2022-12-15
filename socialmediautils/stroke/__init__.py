""" This module implements the outline stroke feature for human in the given images
"""
from typing import Any
from .stroke_img import add_img_stroke
from .stroke_img import add_img_stroke_with_bg
from .stroke_img import enable_visual_debug


def get_stroke_session(model_type: str) -> Any:
    from rembg.session_factory import new_session
    return new_session(model_type)
