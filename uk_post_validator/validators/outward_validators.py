import re

from uk_post_validator import exceptions

AREA_REGEX = '[A-Za-z]{1,2}'
DISTRICT_REGEX = '([1-9][0-9]|[0-9][A-Za-z]{0,1})'
OUTWARD_REGEX = ''.join([AREA_REGEX, DISTRICT_REGEX])


def validate_area(area: str) -> bool:
    """Validates that area has a correct format"""
    area_pattern_is_correct = re.fullmatch(
        '^{}$'.format(AREA_REGEX),
        str(area)
    )

    if area_pattern_is_correct:
        return True

    raise exceptions.InvalidAreaValueError(
        'Area should be 1 or 2 alphabetic characters'
    )


def validate_district(district: str) -> bool:
    """Validates that district has a correct format"""
    district_pattern_is_correct = re.fullmatch(
        '^{}$'.format(DISTRICT_REGEX),
        str(district)
    )

    if district_pattern_is_correct:
        return True

    raise exceptions.InvalidDistrictValueError(
        'District should be 2 numeric characters,'
        ' or 1 numeric and none or 1 alphabetic characters'
    )


def validate_outward_code(outward_code: str) -> bool:
    """Validates that full outward code has correct format."""
    outward_pattern_is_correct = re.fullmatch(
        '^{}$'.format(OUTWARD_REGEX),
        outward_code
    )

    if outward_pattern_is_correct:
        return True

    raise exceptions.InvalidOutwardCodeFormatError(
        'Outward code is not correctly formatted'
    )
