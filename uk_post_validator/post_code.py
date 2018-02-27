from uk_post_validator import exceptions
from uk_post_validator.inward_code import InwardCode
from uk_post_validator.outward_code import OutwardCode
from uk_post_validator.parsers import post_code_parser
from uk_post_validator.validators import post_code_validators


class PostCode:
    """
    It is between six and eight characters long.

    It's components are, concatenated, the ones of the outward and
    inward codes (respectively).

    To create a postcode object, its components (outward and inward
    codes) must pass its own validation.
    """
    def __init__(self, outward_code: OutwardCode, inward_code: InwardCode):
        self._outward_code = outward_code
        self._inward_code = inward_code

    @property
    def area_code(self) -> str:
        """
        Returns string value of area for postcode instance
        (only specific identifier).
        """
        return self._outward_code.area

    @property
    def district_code(self) -> str:
        """
        Returns string value of district for postcode instance
        (only specific identifier).
        """
        return self._outward_code.district

    @property
    def sector_code(self) -> int:
        """
        Returns digit value of sector for postcode instance
        (only specific identifier).
        """
        return self._inward_code.sector

    @property
    def unit_code(self) -> str:
        """
        Returns string value of unit for postcode instance
        (only specific identifier).
        """
        return self._inward_code.unit

    @property
    def area(self) -> str:
        """
        Returns string value of area for postcode instance
        (full code).
        """
        return self.area_code

    @property
    def district(self) -> str:
        """
        Returns string value of district for postcode instance
        (full code, which is outward code).
        """
        return '{area}{district_code}'.format(
            area=self.area,
            district_code=self.district_code
        )

    @property
    def sector(self) -> str:
        """
        Returns string value of sector for postcode instance
        (full code).
        """
        return '{district} {sector_code}'.format(
            district=self.district,
            sector_code=self.sector_code
        )

    @property
    def unit(self) -> str:
        """
        Returns string value of unit for postcode instance
        (full code, outward + inward code).
        """
        return '{sector}{unit_code}'.format(
            sector=self.sector,
            unit_code=self.unit_code
        )

    @property
    def full_code(self) -> str:
        """
        Returns a string composed by outward + inward code,
        separated by a space.
        """
        return self.unit

    def is_valid(self) -> bool:
        """
        Checks if postcode is valid, not only its components format,
        but the whole postcode.
        """
        try:
            return post_code_validators.validate_post_code_by_components(
                area=self.area_code,
                district=self.district_code,
                sector=self.sector_code,
                unit=self.unit_code
            )
        except exceptions.PostCodeError:
            return False

    def __repr__(self) -> str:
        return self.full_code

    @classmethod
    def create_from_complete_post_code(cls, post_code: str):
        """
        Creates an instance of the class, validating the full code
        and parsing its components.
        """
        post_code_validators.validate_post_code_format(post_code)
        area, district, sector, unit = post_code_parser.divide_post_code_in_components(
            post_code
        )

        return cls(
            outward_code=OutwardCode(area=area, district=district),
            inward_code=InwardCode(sector=sector, unit=unit)
        )
