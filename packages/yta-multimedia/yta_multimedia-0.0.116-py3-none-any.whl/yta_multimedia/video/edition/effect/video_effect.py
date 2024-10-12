from yta_general_utils.checker.type import variable_is_type
from yta_general_utils.file.checker import file_is_video_file
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from typing import Union
from abc import ABC, abstractmethod


class VideoEffect(ABC):
    """
    Abstract class to be inherited by all my custom effects so I can 
    control they belong to this family.

    A video effect is an effect that is customly made by using 
    personal modifications, calculations, involving maybe some
    image manipulation, etc.
    """
    def __init__(self, video: Union[VideoFileClip, ImageClip, CompositeVideoClip, str]):
        if not video:
            raise Exception('No "video" provided.')
        
        if variable_is_type(video, str):
            if not file_is_video_file(video):
                raise Exception('Provided "video" is not a valid video file.')
            
            video = VideoFileClip(video)

        self.video = video

    @abstractmethod
    def apply(self):
        pass