from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.utils.resize_t_functions import linear_zoom_transition_t_func
from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageClip
from typing import Union


class LinearZoomVideoEffect(VideoEffect):
    """
    Creates a linear Zoom effect in the provided video.
    """

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], zoom_start: float, zoom_end: float):
        """
        Applies the effect on the provided 'clip'.
        """
        clip = super().parse_moviepy_video(clip)

        if not zoom_start or not zoom_end:
            raise Exception('No "zoom_start" or "zoom_end" provided.')

        fps = clip.fps
        duration = clip.duration
        screensize = clip.size

        effected_video = (
            clip
            .resize(screensize)
            .resize(lambda t: linear_zoom_transition_t_func(t, duration, zoom_start, zoom_end))
            .set_position(('center', 'center'))
            .set_duration(duration)
            .set_fps(fps)
        )

        return CompositeVideoClip([effected_video], size = screensize)


    