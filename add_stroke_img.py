from socialmediautils import stroke


model_session = stroke.get_stroke_session("u2net_human_seg")
stroke.enable_visual_debug(True)
stroke_color = (255, 255, 0)
stroke.add_img_stroke(model_session, "sample/me.png", stroke_color, 1.07)
