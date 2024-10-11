from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_center import CoordinateCenter
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_corner import CoordinateCorner
from yta_multimedia.video.edition.effect.moviepy.position.enums import ScreenPosition
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video.edition.effect.moviepy.position.utils.move import linear_movement
from yta_multimedia.audio.channels import synchronize_audio_pan_with_video_by_position
from yta_general_utils.file.checker import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class MoveLinearPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of moving the element from one place in the screen (or outside
    of bounds) to another, linearly.
    """
    def apply(self, initial_position: Union[ScreenPosition, tuple] = ScreenPosition.OUT_LEFT, final_position: Union[ScreenPosition, CoordinateCorner, CoordinateCenter] = ScreenPosition.CENTER):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        background_video = ColorClip((1920, 1080), [0, 0, 0], duration = self.video.duration)

        return self.apply_over_video(background_video, initial_position, final_position)

    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], initial_position: Union[ScreenPosition, CoordinateCorner, CoordinateCenter] = ScreenPosition.OUT_LEFT, final_position: Union[ScreenPosition, CoordinateCorner, CoordinateCenter] = ScreenPosition.CENTER):
        """
        TODO: Write well

        Applies the effect on the video used when instantiating the
        effect, but applies the effect by placing it over the 
        'background_video' provided in this method (the 
        'background_video' will act as a background video for the 
        effect applied on the initial video).

        This method will set the video used when instantiating the
        effect as the most important, and its duration will be 
        considered as that. If the 'background_video' provided 
        has a duration lower than the original video, we will
        loop it to reach that duration. If the video is shorter
        than the 'background_video', we will crop the last one
        to fit the original video duration.
        """
        if not background_video:
            raise Exception('No "background_video" provided.')
        
        if isinstance(background_video, str):
            if not file_is_video_file:
                raise Exception('Provided "background_video" is not a valid video file.')
            
            background_video = VideoFileClip(background_video)

        if not isinstance(initial_position, ScreenPosition) and not isinstance(initial_position, CoordinateCenter) and not isinstance(initial_position, CoordinateCorner):
            raise Exception('Provided "initial_position" is not a valid ScreenPosition, CoordinateCenter or CoordinateCorner.')

        if not isinstance(final_position, ScreenPosition) and not isinstance(final_position, CoordinateCenter) and not isinstance(final_position, CoordinateCorner):
            raise Exception('Provided "final_position" is not a valid ScreenPosition, CoordinateCenter or CoordinateCorner.')

        background_video = super().process_background_video(background_video)

        initial_position = get_moviepy_position(self.video, background_video, initial_position)
        final_position = get_moviepy_position(self.video, background_video, final_position)

        effect = self.video.set_position(lambda t: linear_movement(t, initial_position, final_position, self.video.duration, self.video.fps)).set_start(0).set_duration(self.video.duration)

        # We pan the video audio by position
        effect = synchronize_audio_pan_with_video_by_position(effect.audio, effect)

        return CompositeVideoClip([
            background_video,
            effect
        ])