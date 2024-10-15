"""
    @DEPRECATED

    This class has become useless so I need to remove in a
    near future as we have the VideoEffect that identifies
    subclasses as effects.
"""

from moviepy.editor import vfx
from abc import ABC, abstractmethod


class MoviepyEffect(ABC):
    """
    Abstract class to be inherited by all my custom moviepy effects
    so I can control they belong to this family.

    A moviepy effect (or what I call like that) is an effect that is
    applied directly to the video by using only the moviepy editor
    and/or moviepy vfx module. It could be a simple moviepy effect
    made an object to simplify the work with it, or a more complex
    effect that is build with some different small effects.
    """
    @abstractmethod
    def apply(self):
        pass

    @classmethod
    def get_moviepy_vfx_effect(self, moviepy_effect_name: str):
        """
        Returns the moviepy vfx effect name corresponding to the provided
        'moviepy_effect_name'.
        """
        return getattr(vfx, moviepy_effect_name, None)
