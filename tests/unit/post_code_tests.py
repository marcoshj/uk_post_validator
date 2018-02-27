import pytest

from uk_post_validator import exceptions
from uk_post_validator.inward_code import InwardCode
from uk_post_validator.outward_code import OutwardCode
from uk_post_validator.parsers import post_code_parser
from uk_post_validator.post_code import PostCode
from uk_post_validator.validators import post_code_validators


class TestPostCodeValidators:
    @pytest.mark.parametrize('post_code', [
        'GIR 0AA',
        'EC1A 1BB',
        'W1A 0AX',
        'M1 1AE',
        'B33 8TH',
        'CR2 6XH',
        'DN55 1PT',
        'BS98 1TL',
    ])
    def test_valid_post_codes_format_is_valid(self, post_code):
        assert post_code_validators.validate_post_code_format(post_code) is True

    @pytest.mark.parametrize('post_code', [
        'EC1A 1B',
        'W1A0AX',
        'M 1AE',
        '33 8TH',
        'CR222 6XH',
        'DNA5 1PT',
        '1S98 1TL',
    ])
    def test_wrong_formatted_post_codes_are_raising_exceptions(
            self,
            post_code
    ):
        with pytest.raises(exceptions.InvalidPostCodeFormatError):
            post_code_validators.validate_post_code_format(post_code)

    @pytest.mark.parametrize('area, district, sector, unit', [
        ('BR', '1A', 9, 'AA'),
        ('br', '1a', 9, 'aa'),
        ('BR', '1', 9, 'AA'),
        ('br', '1', 9, 'aa'),
        ('AB', '11', 9, 'AA'),
        ('ab', '11', 9, 'aa'),
        ('BL', '0', 9, 'AA'),
        ('A', '9A', 9, 'AA'),
        ('AA', '9A', 9, 'AA'),
        ('PR', '0', 9, 'AA'),
        ('aa', '9a', 9, 'aa'),
        ('pr', '0', 9, 'aa'),
    ])
    def test_post_code_components_validation_is_validated_for_correct_values(
            self,
            area,
            district,
            sector,
            unit,
    ):
        post_code_validation = post_code_validators.validate_post_code_by_components(
            area,
            district,
            sector,
            unit
        )

        assert post_code_validation is True

    @pytest.mark.parametrize('area, district, sector, unit, expected_exception', [
        ('BR', '11', 9, 'AA', exceptions.SingleDigitDistrictAreaFormatError),
        ('br', '11', 9, 'aa', exceptions.SingleDigitDistrictAreaFormatError),
        ('AB', '1', 9, 'AA', exceptions.DoubleDigitDistrictAreaFormatError),
        ('AB', '1A', 9, 'AA', exceptions.DoubleDigitDistrictAreaFormatError),
        ('AB', '1a', 9, 'AA', exceptions.DoubleDigitDistrictAreaFormatError),
        ('Q', '11', 9, 'AA', exceptions.AreaCharacterNotAllowedError),
        ('q', '1A', 9, 'AA', exceptions.AreaCharacterNotAllowedError),
        ('AI', '1A', 9, 'AA', exceptions.AreaCharacterNotAllowedError),
        ('A', '1Z', 9, 'AA', exceptions.DistrictCharacterNotAllowedError),
        ('AA', '1C', 9, 'AA', exceptions.DistrictCharacterNotAllowedError),
        ('AB', '11', 9, 'CM', exceptions.UnitCharactersNotAllowedError),
        ('AB', '11', 9, 'Ak', exceptions.UnitCharactersNotAllowedError),
    ])
    def test_wrong_post_code_components_validation_are_raising_exceptions(
            self,
            area,
            district,
            sector,
            unit,
            expected_exception
    ):
        with pytest.raises(expected_exception):
            post_code_validators.validate_post_code_by_components(
                area,
                district,
                sector,
                unit
            )

    @pytest.mark.parametrize('area, district', [
        ('BR', '1'),
        ('BR', '1A'),
        ('br', '1a'),
        ('LL', '11'),
        ('PR', '0'),
        ('PR', '0A'),
        ('pr', '0'),
    ])
    def test_district_digits_for_area_are_correctly_validated(self, area, district):
        district_is_valid = post_code_validators._validate_district_digits_for_area(
            area=area,
            district=district
        )
        assert district_is_valid is True

    @pytest.mark.parametrize('area, district, expected_exception', [
        ('BR', 'AA', exceptions.SingleDigitDistrictAreaFormatError),
        ('br', 'AA', exceptions.SingleDigitDistrictAreaFormatError),
        ('BR', '11', exceptions.SingleDigitDistrictAreaFormatError),
        ('LL', '1', exceptions.DoubleDigitDistrictAreaFormatError),
        ('LL', '1A', exceptions.DoubleDigitDistrictAreaFormatError),
        ('LL', '1a', exceptions.DoubleDigitDistrictAreaFormatError),
        ('LS', '0', exceptions.NonZeroDistrictAreaFormatError),
        ('LS', '0', exceptions.NonZeroDistrictAreaFormatError),
    ])
    def test_district_digits_for_area_validation_raises_exceptions_when_invalid(
            self,
            area,
            district,
            expected_exception
    ):
        with pytest.raises(expected_exception):
            post_code_validators._validate_district_digits_for_area(
                area=area,
                district=district
            )

    @pytest.mark.parametrize('area, district', [
        ('A', '9A'),
        ('B', '9K'),
        ('BA', '9A'),
        ('BA', '9Y'),
        ('a', '9a'),
        ('b', '9k'),
        ('ba', '9a'),
        ('ba', '9y'),
    ])
    def test_district_letters_for_area_are_correctly_validated(self, area, district):
        district_is_valid = post_code_validators._validate_district_letters_for_area(
            area=area,
            district=district
        )
        assert district_is_valid is True

    @pytest.mark.parametrize('area, district, expected_exception', [
        ('C', '1Z', exceptions.DistrictCharacterNotAllowedError),
        ('C', '1Z', exceptions.DistrictCharacterNotAllowedError),
        ('CA', '1C', exceptions.DistrictCharacterNotAllowedError),
        ('BA', '1Z', exceptions.DistrictCharacterNotAllowedError),
        ('c', '1z', exceptions.DistrictCharacterNotAllowedError),
        ('c', '1z', exceptions.DistrictCharacterNotAllowedError),
        ('ca', '1c', exceptions.DistrictCharacterNotAllowedError),
        ('ba', '1z', exceptions.DistrictCharacterNotAllowedError),
    ])
    def test_district_letters_for_area_validation_raises_exceptions_when_invalid(
            self,
            area,
            district,
            expected_exception
    ):
        with pytest.raises(expected_exception):
            post_code_validators._validate_district_letters_for_area(
                area=area,
                district=district
            )

    @pytest.mark.parametrize('area', [
        'IA',
        'JA',
        'ZA',
        'AQ',
        'AV',
        'AX',
        'ia',
        'ja',
        'za',
        'aq',
        'av',
        'ax',
    ])
    def test_area_is_correctly_validated(self, area):
        area_is_valid = post_code_validators._validate_area(area)
        assert area_is_valid is True

    @pytest.mark.parametrize('area, expected_exception', [
        ('QA', exceptions.AreaCharacterNotAllowedError),
        ('VV', exceptions.AreaCharacterNotAllowedError),
        ('XX', exceptions.AreaCharacterNotAllowedError),
        ('AI', exceptions.AreaCharacterNotAllowedError),
        ('AJ', exceptions.AreaCharacterNotAllowedError),
        ('AZ', exceptions.AreaCharacterNotAllowedError),
        ('qa', exceptions.AreaCharacterNotAllowedError),
        ('vv', exceptions.AreaCharacterNotAllowedError),
        ('xx', exceptions.AreaCharacterNotAllowedError),
        ('ai', exceptions.AreaCharacterNotAllowedError),
        ('aj', exceptions.AreaCharacterNotAllowedError),
        ('az', exceptions.AreaCharacterNotAllowedError),
    ])
    def test_area_validation_raises_exceptions_when_invalid(
            self,
            area,
            expected_exception
    ):
        with pytest.raises(expected_exception):
            post_code_validators._validate_area(area)

    @pytest.mark.parametrize('unit', [
        'AA',
        'AB',
        'ZS',
    ])
    def test_unit_is_correctly_validated(self, unit):
        unit_is_valid = post_code_validators._validate_unit(unit)
        assert unit_is_valid is True

    @pytest.mark.parametrize('unit, expected_exception', [
        ('CA', exceptions.UnitCharactersNotAllowedError),
        ('ca', exceptions.UnitCharactersNotAllowedError),
        ('AC', exceptions.UnitCharactersNotAllowedError),
        ('Ai', exceptions.UnitCharactersNotAllowedError),
        ('kA', exceptions.UnitCharactersNotAllowedError),
        ('AM', exceptions.UnitCharactersNotAllowedError),
        ('sO', exceptions.UnitCharactersNotAllowedError),
        ('VA', exceptions.UnitCharactersNotAllowedError),
    ])
    def test_area_validation_raises_exceptions_when_invalid(
            self,
            unit,
            expected_exception
    ):
        with pytest.raises(expected_exception):
            post_code_validators._validate_unit(unit)

    @pytest.mark.parametrize('area, district, sector, unit, full_code_expected', [
        ('A', '9', '9', 'AA', 'A9 9AA'),
        ('a', '9', '9', 'Aa', 'A9 9AA'),
        ('aA', '9', 9, 'Aa', 'AA9 9AA'),
    ])
    def test_full_post_code_composition_in_validation(
            self,
            area,
            district,
            sector,
            unit,
            full_code_expected
    ):
        full_code = post_code_validators._compose_full_post_code(
            area,
            district,
            sector,
            unit
        )

        assert full_code == full_code_expected


class TestPostCodeParsers:
    @pytest.mark.parametrize(
        'post_code, expected_area, expected_district, expected_sector, expected_unit', [
            ('AA9A 9AA', 'AA', '9A', 9, 'AA'),
            ('A9A 9AA', 'A', '9A', 9, 'AA'),
            ('A9 9AA', 'A', '9', 9, 'AA'),
            ('A99 9AA', 'A', '99', 9, 'AA'),
            ('AA9 9AA', 'AA', '9', 9, 'AA'),
            ('AA99 9AA', 'AA', '99', 9, 'AA'),
            ('AA9A9AA', 'AA', '9A', 9, 'AA'),
            ('A9A9AA', 'A', '9A', 9, 'AA'),
            ('A99AA', 'A', '9', 9, 'AA'),
            ('A999AA', 'A', '99', 9, 'AA'),
            ('AA99AA', 'AA', '9', 9, 'AA'),
            ('AA999AA', 'AA', '99', 9, 'AA'),
            ('aa9a9aa', 'aa', '9a', 9, 'aa'),
            ('a9a9aa', 'a', '9a', 9, 'aa'),
            ('a99aa', 'a', '9', 9, 'aa'),
            ('a000aa', 'a', '00', 0, 'aa'),
            ('aa00aa', 'aa', '0', 0, 'aa'),
            ('aa000aa', 'aa', '00', 0, 'aa'),
        ]
    )
    def test_post_code_is_parsed_correctly(
            self,
            post_code,
            expected_area,
            expected_district,
            expected_sector,
            expected_unit
    ):
        area, district, sector, unit = post_code_parser.divide_post_code_in_components(
            post_code
        )

        assert expected_area == area
        assert expected_district == district
        assert expected_sector == sector
        assert expected_unit == unit

    @pytest.mark.parametrize('post_code, expected_exceptions', [
        (7, exceptions.PostCodeParsingError),
        ('A', (exceptions.OutwardCodeParsingError, exceptions.InwardCodeParsingError)),
        ('AAA AAA', (exceptions.OutwardCodeParsingError, exceptions.InwardCodeParsingError)),
    ])
    def test_post_code_parser_raises_exception_when_invalid_values(
            self,
            post_code,
            expected_exceptions
    ):
        with pytest.raises(expected_exceptions):
            post_code_parser.divide_post_code_in_components(post_code)


class TestPostCodeObject:
    @pytest.fixture
    def valid_post_code(self):
        return PostCode.create_from_complete_post_code('EC1A 1BB')

    @pytest.fixture
    def non_valid_post_code(self):
        return PostCode.create_from_complete_post_code('AB0A 1BB')

    @pytest.mark.parametrize('outward_code, inward_code', [
        (OutwardCode('A', '9'), InwardCode(9, 'AA')),
        (OutwardCode('AA', '9A'), InwardCode(0, 'BB')),
    ])
    def test_post_code_is_created_correctly_when_values_are_valid(
            self,
            outward_code: OutwardCode,
            inward_code: InwardCode
    ):
        post_code = PostCode(
            outward_code=outward_code,
            inward_code=inward_code
        )

        assert post_code.area_code == outward_code.area
        assert post_code.district_code == outward_code.district
        assert post_code.sector_code == inward_code.sector
        assert post_code.unit_code == inward_code.unit

    @pytest.mark.parametrize(
        'post_code, area_expected, district_expected, sector_expected, unit_expected', [
            (
                    PostCode(
                        OutwardCode('A', '9'),
                        InwardCode(9, 'AA')
                    ),
                    'A', 'A9', 'A9 9', 'A9 9AA'
            ),
            (
                    PostCode(
                        OutwardCode('AA', '99'),
                        InwardCode(0, 'AA')
                    ),
                    'AA', 'AA99', 'AA99 0', 'AA99 0AA'
            ),

        ])
    def test_post_code_properties_are_valid(
            self,
            post_code: PostCode,
            area_expected,
            district_expected,
            sector_expected,
            unit_expected
    ):
        assert post_code.area == area_expected
        assert post_code.district == district_expected
        assert post_code.sector == sector_expected
        assert post_code.unit == unit_expected
        assert post_code.full_code == unit_expected
        assert post_code.full_code == str(post_code)

    @pytest.mark.parametrize('post_code', [
        'EC1A 1BB',
        'W1A 0AX',
        'M1 1AE',
        'B33 8TH',
        'CR2 6XH',
        'DN55 1PT',
    ])
    def test_create_post_code_object_from_full_code_string(self, post_code):
        post_code_created = PostCode.create_from_complete_post_code(post_code)

        assert isinstance(post_code_created, PostCode)

    def test_post_code_is_valid(self, valid_post_code):
        assert valid_post_code.is_valid() is True

    def test_post_code_is_not_valid(self, non_valid_post_code):
        assert non_valid_post_code.is_valid() is False
