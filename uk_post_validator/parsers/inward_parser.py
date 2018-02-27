from typing import Tuple

from uk_post_validator.exceptions import InwardCodeParsingError


def divide_inward_code_in_components(inward_code: str) -> Tuple[int, str]:
    """
    Divides a string containing the full inward code into sector and unit.
    """
    try:
        sector, unit = int(inward_code[:1]), inward_code[1:]
    except (ValueError, TypeError):
        raise InwardCodeParsingError(
            'Cannot find sector and unit for specified inward code'
        )

    if '' in [sector, unit]:
        raise InwardCodeParsingError('Nor sector nor unit can be empty')

    return sector, unit
