import pytest

from uk_post_validator.exceptions import InwardCodeParsingError
from uk_post_validator.parsers import inward_parser
from uk_post_validator.validators import inward_validators
from uk_post_validator import exceptions
from uk_post_validator.inward_code import InwardCode


class TestInwardCodeParsers:
    @pytest.mark.parametrize('inward_code, expected_sector, expected_unit', [
        ('9AA', 9, 'AA'),
        ('0AA', 0, 'AA'),
        ('0zz', 0, 'zz'),
    ])
    def test_inward_code_is_divided_correctly_by_parser(
            self,
            inward_code,
            expected_sector,
            expected_unit
    ):
        sector, unit = inward_parser.divide_inward_code_in_components(
            inward_code
        )

        assert expected_sector == sector
        assert expected_unit == unit

    @pytest.mark.parametrize('inward_code', [
        1,
        '1',
        'A',
        'AA',
        'AAA',
        None,
        object,
        [1, 'A', 'A']
    ])
    def test_inward_code_parser_is_raising_exceptions_for_invalid_values(
            self,
            inward_code,
    ):
        with pytest.raises(InwardCodeParsingError):
            inward_parser.divide_inward_code_in_components(inward_code)


class TestInwardValidators:
    @pytest.mark.parametrize("sector", [
        0, '0', 5, '5', 9, '9'
    ])
    def test_sector_validator_for_correct_values(
            self,
            sector
    ):
        assert inward_validators.validate_sector(sector) is True

    @pytest.mark.parametrize("sector", [
        -1,
        10,
        '-1',
        '10',
        object,
        'a',
        'z',
        'A',
        'Z',
        []
    ])
    def test_sector_validator_for_incorrect_values(self, sector):
        with pytest.raises(exceptions.InvalidSectorValueError):
            inward_validators.validate_sector(sector)

    @pytest.mark.parametrize("unit", [
        'az', 'AZ', 'aZ', 'Az'
    ])
    def test_unit_validator_for_correct_values(self, unit):
        assert inward_validators.validate_unit(unit) is True

    @pytest.mark.parametrize("unit", [
        -11,
        '-11',
        -1,
        '-1',
        0,
        '00',
        1,
        '1',
        11,
        '11',
        'a',
        'aaa',
        'z',
        'zzz',
        object,
        '++',
        '**'
    ])
    def test_unit_validator_for_incorrect_values(self, unit):
        with pytest.raises(exceptions.InvalidUnitValueError):
            inward_validators.validate_unit(unit)

    @pytest.mark.parametrize("inward_code", [
        '0AA', '5BB', '9CC'
    ])
    def test_validation_inward_code(self, inward_code):
        assert inward_validators.validate_inward_code(inward_code) is True

    @pytest.mark.parametrize("inward_code", [
        'A', '1', 'AA', '1A', 'A1', 'AAA', '10A', '9AAA',
    ])
    def test_validation_inward_code_with_wrong_data(self, inward_code):
        with pytest.raises(exceptions.InvalidInwardCodeFormatError):
            inward_validators.validate_inward_code(inward_code)


class TestInwardCodeObject:
    @pytest.mark.parametrize(
        "sector, unit, expected_sector, expected_unit, expected_code",
        [
            ('0', 'AZ', 0, 'AZ', '0AZ'),
            (0, 'AZ', 0, 'AZ', '0AZ'),
            ('0', 'az', 0, 'AZ', '0AZ'),
            (0, 'az', 0, 'AZ', '0AZ'),
            ('9', 'ZA', 9, 'ZA', '9ZA'),
            (9, 'ZA', 9, 'ZA', '9ZA'),
            ('9', 'za', 9, 'ZA', '9ZA'),
            (9, 'za', 9, 'ZA', '9ZA')
        ]
    )
    def test_inward_code_is_created_with_correct_data(
            self,
            sector,
            unit,
            expected_sector,
            expected_unit,
            expected_code
    ):
        inward_code = InwardCode(sector=sector, unit=unit)

        assert expected_sector == inward_code.sector
        assert expected_unit == inward_code.unit
        assert expected_code == inward_code.code

    @pytest.mark.parametrize("sector, unit, expected_exception", [
        (10, 'AZ', exceptions.InvalidSectorValueError),
        (-1, 'AZ', exceptions.InvalidSectorValueError),
        (5, 'A', exceptions.InvalidUnitValueError),
        (5, 'ABC', exceptions.InvalidUnitValueError),

    ])
    def test_inward_code_is_not_created_when_data_is_not_correct(
            self,
            sector,
            unit,
            expected_exception
    ):
        with pytest.raises(expected_exception):
            InwardCode(sector=sector, unit=unit)

    @pytest.mark.parametrize(
        "sector, unit, expected_string",
        [
            (0, 'AZ', '0AZ'),
            (9, 'ZA', '9ZA'),
        ]
    )
    def test_string_representation_inward_code(self, sector, unit, expected_string):
        assert expected_string == str(InwardCode(sector=sector, unit=unit))

    @pytest.mark.parametrize(
        "expected_sector, expected_unit, complete_inward_code", [
            (1, 'BB', '1BB'),
            (0, 'AX', '0AX'),
            (1, 'AE', '1AE'),
            (8, 'TH', '8TH'),
            (6, 'XH', '6XH'),
            (1, 'PT', '1PT'),
        ]
    )
    def test_inward_class_object_creation_by_complete_code(
            self,
            expected_sector,
            expected_unit,
            complete_inward_code
    ):
        inward_code = InwardCode.create_from_complete_inward_code(complete_inward_code)
        assert expected_unit == inward_code.unit
        assert expected_sector == inward_code.sector
        assert complete_inward_code == inward_code.code
