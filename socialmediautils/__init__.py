""" This package implements the various utilities for making social media content
"""
from .version import __version__
from .stroke import get_stroke_session
from .stroke.stroke_img import add_img_stroke
from .stroke.stroke_img import add_img_stroke_with_bg
from .stroke.stroke_img import enable_visual_debug


__all__ = ['__version__', 'get_stroke_session', 'add_img_stroke', 'add_img_stroke_with_bg', 'enable_visual_debug']
