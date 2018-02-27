from uk_post_validator.parsers import outward_parser
from uk_post_validator.validators import outward_validators


class OutwardCode:
    """
    The outward code is the part of the postcode before the single
    space in the middle.

    It is between two and four characters long.

    It's components are:
      -Area: one or two characters long and is all letters.
      -District: between two and four characters long.
       One or two digits (and sometimes a final letter).
    """
    def __init__(self, area: str, district: str):
        outward_validators.validate_area(area)
        outward_validators.validate_district(district)
        self._area = str(area).upper()
        self._district = str(district).upper()

    @property
    def area(self) -> str:
        """Returns string value of area for outward code instance."""
        return self._area

    @property
    def district(self) -> str:
        """
        Returns string value of district for outward code instance.
        """
        return self._district

    @property
    def code(self) -> str:
        """Returns the full outward code in a string"""
        return f'{self.area}{self.district}'

    def __repr__(self) -> str:
        return self.code

    @classmethod
    def create_from_complete_outward_code(cls, outward_code: str):
        """
        Creates an instance of the class, validating the full code
        and parsing its components.
        """
        outward_validators.validate_outward_code(outward_code)
        area, district = outward_parser.divide_outward_code_in_components(
            outward_code
        )

        return cls(area=area, district=district)
