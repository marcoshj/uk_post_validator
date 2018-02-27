import re

from uk_post_validator import exceptions

POST_CODE_REGEX = ('([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|'
                   '(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|'
                   '(([A-Za-z][0-9][A-Za-z])|'
                   '([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))'
                   ' [0-9][A-Za-z]{2})')

SINGLE_DIGIT_AREAS = ['BR', 'FY', 'HA', 'HD', 'HG', 'HR', 'HS', 'HX',
                      'JE', 'LD', 'SM', 'SR', 'WC', 'WN', 'ZE']

DOUBLE_DIGIT_AREAS = ['AB', 'LL', 'SO']

ZERO_DISTRICT_AREAS = ['BL', 'BS', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS']

FORBIDDEN_AREA_FIRST_LETTER = 'QVX'

FORBIDDEN_AREA_SECOND_LETTER = 'IJZ'

ALLOWED_THIRD_POSITION_FOR_A9A_FORMAT = 'ABCDEFGHJKPSTUW'

ALLOWED_FOURTH_POSITION_FOR_AA9A_FORMAT = 'ABEHMNPRVWXY'

FORBIDDEN_UNIT_LETTERS = 'CIKMOV'


def validate_post_code_format(full_code: str) -> bool:
    """Validates that full post code has correct format."""
    code_to_validate = full_code.strip().upper()
    post_code_is_correct = re.fullmatch(f'^{POST_CODE_REGEX}$', code_to_validate)

    if not post_code_is_correct:
        raise exceptions.InvalidPostCodeFormatError('Post code has not a correct format')

    return True


def validate_post_code_by_components(
        area: str,
        district: str,
        sector: int,
        unit: str
) -> bool:
    """
    Given the whole post code, validates each component independently and
    against the rest of the code.
    """
    area = area.upper()
    district = district.upper()
    unit = unit.upper()

    _validate_district_digits_for_area(area, district)

    _validate_district_letters_for_area(area, district)

    _validate_area(area)

    _validate_unit(unit)

    return validate_post_code_format(_compose_full_post_code(
        area,
        district,
        sector,
        unit
    ))


def _validate_district_digits_for_area(area: str, district: str) -> bool:
    """
    Validates that district digits are valid (if applicable) depending area.
    """
    area = area.strip().upper()
    district = district.strip().upper()
    if area in SINGLE_DIGIT_AREAS and not re.fullmatch('^[0-9][A-Za-z]?$', district):
        raise exceptions.SingleDigitDistrictAreaFormatError(
            'Postcode area cannot have double digit district'
        )
    if area in DOUBLE_DIGIT_AREAS and not re.fullmatch('^[0-9]{2}$', district):
        raise exceptions.DoubleDigitDistrictAreaFormatError(
            'Postcode area must have a double digit district'
        )
    if area not in ZERO_DISTRICT_AREAS and re.fullmatch('^0[A-Za-z]?$', district):
        raise exceptions.NonZeroDistrictAreaFormatError(
            'Postcode area cannot have a district with value zero'
        )

    return True


def _validate_district_letters_for_area(area: str, district: str) -> bool:
    """
    Validates district letters are valid (if applicable) depending area.
    """
    area = area.strip().upper()
    district = district.strip().upper()
    if re.fullmatch('^[A-Za-z]$', area) \
            and re.fullmatch('^[0-9][A-Za-z]$', district) \
            and district[1] not in ALLOWED_THIRD_POSITION_FOR_A9A_FORMAT:
        raise exceptions.DistrictCharacterNotAllowedError(
            'District letter not allowed for postcode format'
        )
    if re.fullmatch('^[A-Za-z]{2}$', area) \
            and re.fullmatch('^[0-9][A-Za-z]$', district) \
            and district[1] not in ALLOWED_FOURTH_POSITION_FOR_AA9A_FORMAT:
        raise exceptions.DistrictCharacterNotAllowedError(
            'District letter not allowed for postcode format'
        )

    return True


def _validate_area(area: str) -> bool:
    """
    Validates first and second letters of are valid (if applicable).
    """
    area = area.strip().upper()
    if area[0] in FORBIDDEN_AREA_FIRST_LETTER:
        raise exceptions.AreaCharacterNotAllowedError(
            'First area letter cannot be Q, V nor X'
        )
    if len(area) == 2 and area[1] in FORBIDDEN_AREA_SECOND_LETTER:
        raise exceptions.AreaCharacterNotAllowedError(
            'Second area letter cannot be I, J nor Z'
        )

    return True


def _validate_unit(unit: str) -> bool:
    """
    Validates unit letters are valid values
    (to avoid confusing digits or each other when hand-written).
    """
    unit = unit.strip().upper()
    if any(letter in unit for letter in FORBIDDEN_UNIT_LETTERS):
        raise exceptions.UnitCharactersNotAllowedError(
            f'Unit doesn\'t allow the following characters:'
            f' {", ".join(FORBIDDEN_UNIT_LETTERS)}.'
        )

    return True


def _compose_full_post_code(
        area: str,
        district: str,
        sector: int,
        unit: str
) -> str:
    """
    Composes a full post code string with all its components with and
    a space in the middle. All strings are uppercase
    """
    return (f'{area.strip().upper()}{district.strip().upper()}'
            f' {sector}{unit.strip().upper()}')
