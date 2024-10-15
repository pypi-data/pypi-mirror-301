from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.utils.resize_t_functions import linear_zoom_out_t_func
from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageClip
from typing import Union


class LinearZoomOutVideoEffect(VideoEffect):
    """
    Creates a linear Zoom out effect in the provided video.
    """
    
    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], zoom_ratio = None):
        """
        Applies the effect on the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        if zoom_ratio is None:
            zoom_ratio = 0.2

        fps = clip.fps
        duration = clip.duration
        screensize = clip.size

        effected_video = (
            clip
            .resize(screensize)
            .resize(lambda t: linear_zoom_out_t_func(t, duration, zoom_ratio))
            .set_position(('center', 'center'))
            .set_duration(duration)
            .set_fps(fps)
        )

        return CompositeVideoClip([effected_video], size = screensize)


    