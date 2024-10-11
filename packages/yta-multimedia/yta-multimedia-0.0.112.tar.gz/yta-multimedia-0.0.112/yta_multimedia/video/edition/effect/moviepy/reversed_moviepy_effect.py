from yta_multimedia.video.edition.effect.moviepy.moviepy_effect import MoviepyEffect
from yta_general_utils.temp import create_temp_filename, create_custom_temp_filename
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, AudioFileClip, ImageSequenceClip
from typing import Union
from pydub import AudioSegment


class ReversedMoviepyEffect(MoviepyEffect):
    """
    This method creates a new one but in reversa, also with the sound reversed.

    It doesn't use the 'mirror_time' effect because it fails. Instead, it saves
    each frame of the video and builds a new video using them in reverse order.
    It also uses the original audio an reverses it in the new generated video.
    """
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip]):
        self.__clip = clip

    def process_parameters(self):
        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        if not self.__clip:
            return None
        
        self.process_parameters()
        
        # TODO: Try to do this in memory, not writing files
        AUDIO_FILE = create_temp_filename('tmp_audio.mp3')
        REVERSED_AUDIO_FILE = create_temp_filename('tmp_reversed_audio.mp3')
        frames_array = []
        for frame in self.__clip.iter_frames():
            frame_name = create_custom_temp_filename('frame_' + str(len(frames_array)) + '.png')
            frames_array.append(frame_name)
        self.__clip.write_images_sequence(create_custom_temp_filename('') + 'frame_%01d.png', logger = 'bar')

        # Reverse audio (I set it manually to fps because others
        # values are failing)
        self.__clip.audio.write_audiofile(AUDIO_FILE, fps = 44100)
        original = AudioSegment.from_mp3(AUDIO_FILE)
        original.reverse().export(REVERSED_AUDIO_FILE)
        reversed_audio = AudioFileClip(REVERSED_AUDIO_FILE)

        # [ 2 ]   Rebuild the video, but in reverse, from last frame to first one
        frames_array = frames_array[::-1]
        self.__clip = ImageSequenceClip(frames_array, fps = self.__clip.fps).set_audio(reversed_audio)

        return self.__clip