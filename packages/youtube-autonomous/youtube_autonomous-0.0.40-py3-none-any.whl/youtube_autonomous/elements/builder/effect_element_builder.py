from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import EnhancementField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from yta_multimedia.video.edition.effect.moviepy.black_and_white_moviepy_effect import BlackAndWhiteMoviepyEffect
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip
from typing import Union


class EffectElementBuilder(ElementBuilder):
    """
    This builders allows you to generate 'EFFECT' content.
    """
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        effect_name = enhancement.keywords
        extra_parameters = {}   # TODO: Get these

        effect = cls.effect_name_to_class(effect_name)

        return effect

        # TODO: I need to send the segment, because the effect will
        # be aplied into the segment but with the enhancement
        # parameters
        return cls.build_custom_from_effect_name(effect_name, segment.video_clip, **extra_parameters)
    
    @classmethod
    def effect_name_to_class(cls, effect_name: str):
        """
        Returns the effect class according to the provided 'effect_name'
        parameter. It will return None if no effect found for that
        'effect_name' parameter.
        """
        effect = None
        
        if effect_name == 'black_and_white':
            effect = BlackAndWhiteMoviepyEffect

        return effect

    @classmethod
    def build_custom_from_effect_name(cls, effect_name: str, video_or_audio: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip], **parameters):
        # TODO: Apply VideoFileClip, AudioFileClip and the others
        ElementParameterValidator.validate_string_mandatory_parameter(effect_name, effect_name)
        # TODO: Validate keywords is a valid effect key name

        # TODO: Apply the effect in the provided 'video_or_audio'
        effect = cls.effect_name_to_class(effect_name)
        if not effect:
            raise Exception(f'No effect found for the "effect_name" parameter "{effect_name}" provided.')

        return effect(video_or_audio).apply(**parameters)

    @classmethod
    def build_custom(cls, effect, video_or_audio: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip], **parameters):
        # TODO: Make the effects implement an abstract class named
        # 'Effect' to be able to detect them as subclasses
        return effect(video_or_audio).apply(**parameters)

    @classmethod
    def build(cls, video_or_audio: Union[VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip]):
        """
        Basic example to test that the building process and
        the class are working correctly.

        TODO: Remove this in the future when 'custom' is 
        working perfectly.
        """
        return BlackAndWhiteMoviepyEffect

        return BlackAndWhiteMoviepyEffect(video_or_audio).apply()