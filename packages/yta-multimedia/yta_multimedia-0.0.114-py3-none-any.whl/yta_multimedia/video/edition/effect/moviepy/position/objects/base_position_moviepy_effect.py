from yta_multimedia.video.edition.duration import set_video_duration
from yta_general_utils.file.checker import file_is_video_file
from moviepy.editor import ColorClip, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class BasePositionMoviepyEffect:
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

    # TODO: Apply the effect within a black background clip of 1920x1080
    def apply(self):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        background_video = ColorClip((1920, 1080), [0, 0, 0], duration = self.video.duration)

        return self.apply_over_video(background_video)

    def process_background_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
        This method will process the provided 'background_video' to check that it is
        valid and also to change its duration to fit the 'self.video' given when
        initializing this effect object. It will shorten the video if its duration is
        greater than the 'self.video', or will loop it to reach the 'self.video'
        duration.

        This method returns, if everything is ok, the new 'background_video' with its
        new duration.
        """
        if not background_video:
            raise Exception('No "background_video" provided.')
    
        if isinstance(background_video, str):
            if not file_is_video_file:
                raise Exception('Provided "background_video" is not a valid video file.')
            
            background_video = VideoFileClip(background_video)

        background_video = set_video_duration(background_video, self.video.duration)

        return background_video
    
    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
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
        pass