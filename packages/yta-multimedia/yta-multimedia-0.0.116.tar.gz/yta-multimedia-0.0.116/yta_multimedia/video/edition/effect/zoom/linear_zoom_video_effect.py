from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.utils.resize_t_functions import linear_zoom_transition_t_func
from moviepy.editor import CompositeVideoClip


class LinearZoomVideoEffect(VideoEffect):
    """
    Creates a linear Zoom effect in the provided video.
    """
    def apply(self, zoom_start: float, zoom_end: float):
        """
        A zoom = 1 means no zoom. Zoom = 1.2 means zoomed in. Zoom = 0.8
        means zoomed out.

        TODO: Explain this, please.
        """
        fps = self.video.fps
        duration = self.video.duration
        screensize = self.video.size

        # TODO: Check that 'zoom_start' and 'zoom_end' are valid
        if not zoom_start or not zoom_end:
            raise Exception('No "zoom_start" or "zoom_end" provided.')

        effected_video = (
            self.video
            .resize(screensize)
            .resize(lambda t: linear_zoom_transition_t_func(t, duration, zoom_start, zoom_end))
            .set_position(('center', 'center'))
            .set_duration(duration)
            .set_fps(fps)
        )

        return CompositeVideoClip([effected_video], size = screensize)


    