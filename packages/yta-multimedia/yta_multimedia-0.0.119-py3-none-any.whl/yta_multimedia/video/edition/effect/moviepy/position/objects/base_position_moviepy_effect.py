from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_center import CoordinateCenter
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_corner import CoordinateCorner
from yta_multimedia.video.edition.effect.moviepy.position.enums import ScreenPosition
from yta_multimedia.video.edition.duration import set_video_duration
from yta_general_utils.file.checker import file_is_video_file
from moviepy.editor import ColorClip, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class BasePositionMoviepyEffect(VideoEffect):
    """
    Class created to test position effects and building objects
    to simplify their use in our system.
    """
    video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip] = None

    def __init__(self, video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        # TODO: This could be an Image that we want to make clip
        if not video:
            raise Exception('No "video" provided.')
    
        if isinstance(video, str):
            if not file_is_video_file:
                raise Exception('Provided "video" is not a valid video file.')
            
            video = VideoFileClip(video)

        self.video = video

    @staticmethod
    def validate_position(position: Union[ScreenPosition, CoordinateCorner, CoordinateCenter]):
        """
        Validates that the provided 'position' is an ScreenPosition, a
        CoordinateCenter or a CoordinateCorner, or raises an Exception
        if not.
        """
        if not isinstance(position, ScreenPosition) and not isinstance(position, CoordinateCenter) and not isinstance(position, CoordinateCorner):
            raise Exception('Provided "position" is not a valid ScreenPosition, CoordinateCenter or CoordinateCorner.')

    @staticmethod
    def get_black_background_clip(duration: float):
        return ColorClip((1920, 1080), [0, 0, 0], duration = duration)

    @staticmethod
    def apply(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        return BasePositionMoviepyEffect.apply_over_video(clip, BasePositionMoviepyEffect.get_black_background_clip(clip.duration))
    
    @staticmethod
    def apply_over_video(clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], background_clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        """
        This method parses the provided 'clip' and 'background_clip' to
        ensure they are valid moviepy clips and also sets the 
        'background_clip' duration to fit the provided 'clip' duration.
        """
        super().parse_moviepy_video(clip)
        super().parse_moviepy_video(background_clip)

        background_clip = set_video_duration(background_clip, clip.duration)

        return background_clip