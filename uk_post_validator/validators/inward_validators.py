import re

from uk_post_validator import exceptions

SECTOR_REGEX = '[0-9]'
UNIT_REGEX = '[A-Za-z]{2}'


def validate_sector(sector: int) -> bool:
    """Validates that sector has correct format."""
    sector_pattern_is_correct = re.fullmatch('^{}$'.format(SECTOR_REGEX), str(sector))

    if sector_pattern_is_correct:
        return True

    raise exceptions.InvalidSectorValueError(
        'Sector should be an integer in range 0-9'
    )


def validate_unit(unit: str) -> bool:
    """Validates that unit has correct format."""
    unit_pattern_is_correct = re.fullmatch('^{}$'.format(UNIT_REGEX), str(unit))

    if unit_pattern_is_correct:
        return True

    raise exceptions.InvalidUnitValueError(
        'Unit should be a string with two characters'
    )


def validate_inward_code(inward_code: str) -> bool:
    """Validates that full inward code has correct format."""
    inward_pattern_is_correct = re.fullmatch(
        '^{sector}{unit}$'.format(sector=SECTOR_REGEX, unit=UNIT_REGEX),
        inward_code
    )

    if inward_pattern_is_correct:
        return True

    raise exceptions.InvalidInwardCodeFormatError(
        'Inward code should be 1 numeric and 2 alphabetic characters'
    )

