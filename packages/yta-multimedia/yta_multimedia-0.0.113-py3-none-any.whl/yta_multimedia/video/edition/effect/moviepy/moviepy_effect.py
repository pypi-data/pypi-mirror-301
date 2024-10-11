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
    def process_parameters(self):
        pass
    
    @abstractmethod
    def apply(self):
        pass
