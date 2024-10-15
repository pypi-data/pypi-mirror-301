from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.enums import EffectPremade
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip, AudioClip, CompositeAudioClip
from typing import Union


class EffectElementBuilder(ElementBuilder):
    """
    This builders allows you to generate 'EFFECT' content.
    """
    @classmethod
    def effect_name_to_class(cls, effect_name: str):
        """
        Returns the effect class according to the provided 'effect_name'
        parameter. It will return None if no effect found for that
        'effect_name' parameter.
        """
        valid_name = EffectPremade.get_valid_name(effect_name, ignore_case = True)

        if not valid_name:
            raise Exception(f'The provided effect premade name "{effect_name}" is not valid. The valid ones are: {EffectPremade.get_all_names_as_str()}')
        
        return EffectPremade[valid_name]
    
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        effect_name = enhancement.keywords
        effect = cls.effect_name_to_class(effect_name)

        return effect

        # TODO: I need to send the segment, because the effect will
        # be aplied into the segment but with the enhancement
        # parameters
        return cls.build_custom_from_effect_name(effect_name, segment.video_clip, **extra_parameters)

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