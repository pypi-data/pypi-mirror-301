from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.move import MoveLinearPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.static import StayAtPositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.enums import ScreenPosition
from yta_general_utils.file.checker import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, concatenate_videoclips
from typing import Union
from random import randrange


class SlideRandomPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of appearing from TOP, TOP_LEFT, BOTTOM, RIGHT, etc. 
    staying at the center, and dissapearing from the opposite 
    edge. This animation will spend 1/6 of the time in the 
    entrance, 4/6 of the time staying at the center, and 1/6 of 
    the time in the exit.
    """
    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
        This effect will make the 'self.video' appear from outside
        of the screen (from the 'in_screen_edge'), will stay in
        the middle of the screen for 4/6 times of its duration, and
        will go away through the 'out_screen_edge' edge of the 
        screen. All over the provided 'background_video'.

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

        background_video = super().process_background_video(background_video)

        random_position = ScreenPosition.in_and_out_positions_as_list()

        movement_time = background_video.duration / 6
        stay_time = background_video.duration / 6 * 4

        effect = concatenate_videoclips([
            MoveLinearPositionMoviepyEffect(self.video.subclip(0, movement_time)).apply_over_video(background_video.subclip(0, movement_time), random_position[0], ScreenPosition.CENTER),
            StayAtPositionMoviepyEffect(self.video.subclip(movement_time, movement_time + stay_time)).apply_over_video(background_video.subclip(movement_time, movement_time + stay_time), ScreenPosition.CENTER),
            MoveLinearPositionMoviepyEffect(self.video.subclip(movement_time + stay_time, self.video.duration)).apply_over_video(background_video.subclip(movement_time + stay_time, self.video.duration), ScreenPosition.CENTER, random_position[1])
        ])

        return effect