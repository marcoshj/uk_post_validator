from uk_post_validator.parsers import inward_parser
from uk_post_validator.validators import inward_validators


class InwardCode:
    """
    The inward code is the part of the postcode after the single space
    in the middle.

    It is three characters long.

    It's components are:
      - Sector: a digit
      - Unit: 2 letters
    """
    def __init__(self, sector: int, unit: str):
        inward_validators.validate_sector(sector)
        inward_validators.validate_unit(unit)
        self._sector = int(sector)
        self._unit = unit.upper()

    @property
    def sector(self) -> int:
        """Returns numeric value of sector for inward code instance."""
        return self._sector

    @property
    def unit(self) -> str:
        """Returns string value of unit for inward code instance."""
        return self._unit

    @property
    def code(self) -> str:
        """Returns the full inward code in a string"""
        return f'{self.sector}{self.unit}'

    def __repr__(self) -> str:
        return self.code

    @classmethod
    def create_from_complete_inward_code(cls, inward_code: str):
        """
        Creates an instance of the class, validating the full code
        and parsing its components.
        """
        inward_validators.validate_inward_code(inward_code)
        sector, unit = inward_parser.divide_inward_code_in_components(
            inward_code
        )
        return cls(sector=sector, unit=unit)
