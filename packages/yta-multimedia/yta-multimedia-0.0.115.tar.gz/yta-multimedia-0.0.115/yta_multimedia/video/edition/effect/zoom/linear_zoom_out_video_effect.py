from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.utils.resize_t_functions import linear_zoom_out_t_func
from moviepy.editor import CompositeVideoClip


class LinearZoomOutVideoEffect(VideoEffect):
    """
    Creates a linear Zoom out effect in the provided video.
    """
    def apply(self, zoom_ratio: float = None):
        fps = self.video.fps
        duration = self.video.duration
        screensize = self.video.size

        # TODO: Check that 'zoom_ratio' is valid
        if zoom_ratio is None:
            zoom_ratio = 0.2

        effected_video = (
            self.video
            .resize(screensize)
            .resize(lambda t: linear_zoom_out_t_func(t, duration, zoom_ratio))
            .set_position(('center', 'center'))
            .set_duration(duration)
            .set_fps(fps)
        )

        return CompositeVideoClip([effected_video], size = screensize)


    