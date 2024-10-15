from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.enums import Premade
from yta_general_utils.programming.parameter_obtainer import ParameterObtainer


class PremadeElementBuilder(ElementBuilder):
    @classmethod
    def premade_name_to_class(cls, premade_name: str):
        """
        Returns the corresponding premade class according to the
        provided 'premade_name'. If no premade class found, the
        return will be None.
        """
        valid_name = Premade.get_valid_name(premade_name, ignore_case = True)

        if not valid_name:
            raise Exception(f'The provided premade name "{premade_name}" is not valid. The valid ones are: {Premade.get_all_names_as_str()}')
        
        return Premade[valid_name]

    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        premade_name = enhancement.keywords

        ElementParameterValidator.validate_premade_name(premade_name)

        premade_class = cls.premade_name_to_class(premade_name)
        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'duration']
        parameters = super().extract_extra_params(enhancement, premade_class.generate, parameters_to_ignore)

        # For this specific case, we use the 'duration' field as the
        # duration extra_param if needed, because it could be using
        # a narration so the actual 'duration' must be that
        parameters['duration'] = enhancement.duration

        actual_parameters = ParameterObtainer.get_parameters_from_method(premade_class.generate)

        # I need to ensure that parameters has only 'mandatory' or 'optional'
        # actual parameters of the method
        parameters = {key: value for key, value in parameters.items() if key in actual_parameters['mandatory'] or key in actual_parameters['optional']}

        return cls.build_custom_from_premade_name(premade_name, **parameters)

    @classmethod
    def build_from_segment(cls, segment: dict):
        premade_name = segment.keywords

        ElementParameterValidator.validate_premade_name(premade_name)

        premade_class = cls.premade_name_to_class(premade_name)
        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'duration']
        parameters = super().extract_extra_params(segment, premade_class.generate, parameters_to_ignore)

        # For this specific case, we use the 'duration' field as the
        # duration extra_param if needed, because it could be using
        # a narration so the actual 'duration' must be that
        parameters['duration'] = segment.duration

        actual_parameters = ParameterObtainer.get_parameters_from_method(premade_class.generate)

        # I need to ensure that parameters has only 'mandatory' or 'optional'
        # actual parameters of the method
        parameters = {key: value for key, value in parameters.items() if key in actual_parameters['mandatory'] or key in actual_parameters['optional']}

        return cls.build_custom_from_premade_name(premade_name, **parameters)

    @classmethod
    def build_custom_from_premade_name(cls, premade_name: str, **parameters):
        ElementParameterValidator.validate_premade_name(premade_name)

        premade_class = cls.premade_name_to_class(premade_name)

        return cls.build(premade_class, **parameters)

    @classmethod
    def build(cls, premade, **parameters):
        # TODO: Make the premades implement an abstract class named
        # 'Premade' to be able to detect them as subclasses
        return premade.generate(**parameters)