from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.enums import TextPremade
from yta_multimedia.video.generation.manim.classes.text.text_word_by_word_manim_animation import TextWordByWordManimAnimation
from yta_general_utils.programming.parameter_obtainer import ParameterObtainer
from moviepy.editor import VideoFileClip


class TextElementBuilder(ElementBuilder):
    @classmethod
    def text_premade_name_to_class(cls, text_premade_name: str):
        """
        Returns the corresponding text premade class according to
        the provided 'text_premade_name'. If no text premade class
        found, the return will be None.
        """
        valid_name = TextPremade.get_valid_name(text_premade_name, ignore_case = True)

        if not valid_name:
            raise Exception(f'The provided text premade name "{text_premade_name}" is not valid. The valid ones are: {TextPremade.get_all_names_as_str()}')
        
        return TextPremade[valid_name]

    @classmethod
    def build_custom_from_text_class_name(cls, text_class_name: str, **parameters):
        ElementParameterValidator.validate_text_class_name(text_class_name)

        text_class = None
        if text_class == 'text_word_by_word':
            text_class = TextWordByWordManimAnimation
        else:
            raise Exception(f'The provided "text_class" parameter {text_class} is not a valid text class name.')
        
        return cls.build_custom(text_class, **parameters)

    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        text_premade_name = enhancement.keywords

        ElementParameterValidator.validate_premade_name(text_premade_name)

        text_premade_class = cls.text_premade_name_to_class(text_premade_name)
        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'output_filename', 'duration']
        parameters = super().extract_extra_params(enhancement, text_premade_class.generate, parameters_to_ignore)

        # For this specific case, we use the 'duration' field as the
        # duration extra_param if needed, because it could be using
        # a narration so the actual 'duration' must be that one
        parameters['duration'] = enhancement.duration

        actual_parameters = ParameterObtainer.get_parameters_from_method(text_premade_class.generate)

        # I need to ensure that parameters has only 'mandatory' or 'optional'
        # actual parameters of the method
        parameters = {key: value for key, value in parameters.items() if key in actual_parameters['mandatory'] or key in actual_parameters['optional']}

        return cls.build_custom_from_text_premade_name(text_premade_name, **parameters)

    @classmethod
    def build_from_segment(cls, segment: dict):
        text_premade_name = segment.keywords

        ElementParameterValidator.validate_premade_name(text_premade_name)

        text_premade_class = cls.text_premade_name_to_class(text_premade_name)
        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'output_filename', 'duration']
        parameters = super().extract_extra_params(segment, text_premade_class.generate, parameters_to_ignore)

        # For this specific case, we use the 'duration' field as the
        # duration extra_param if needed, because it could be using
        # a narration so the actual 'duration' must be that
        parameters['duration'] = segment.duration

        actual_parameters = ParameterObtainer.get_parameters_from_method(text_premade_class.generate)

        # I need to ensure that parameters has only 'mandatory' or 'optional'
        # actual parameters of the method
        parameters = {key: value for key, value in parameters.items() if key in actual_parameters['mandatory'] or key in actual_parameters['optional']}

        return cls.build_custom_from_text_premade_name(text_premade_name, **parameters)
    
    @classmethod
    def build_custom_from_text_premade_name(cls, text_premade_name, **parameters):
        """
        This method instantiates the 'text_animation_class' Manim
        text animation class and uses the provided 'parameters' to
        build the text animation. The provided 'parameters' must 
        fit the ones requested by the provided class 'generate'
        method.
        """
        ElementParameterValidator.validate_premade_name(text_premade_name)

        text_premade_class = cls.text_premade_name_to_class(text_premade_name)

        # We generate the animation to return it
        filename = text_premade_class().generate(**parameters)

        return VideoFileClip(filename)