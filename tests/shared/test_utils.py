from app.shared.utils import (
    MaxSlopePercent,
    SlopeClass,
    classify_slope,
    slugify,
)


def test_slugify_basic():
    assert slugify('Fazenda Teste') == 'fazenda-teste'


def test_slugify_accents():
    assert slugify('Fazenda São João') == 'fazenda-sao-joao'


def test_slugify_special_chars():
    assert slugify('Fazenda & Cia') == 'fazenda-cia'


def test_slugify_multiple_spaces():
    assert slugify('Fazenda  Teste') == 'fazenda-teste'


def test_slugify_already_lowercase():
    assert slugify('fazenda-teste') == 'fazenda-teste'


def test_slugify_numbers():
    assert slugify('Fazenda 01') == 'fazenda-01'


def test_slugify_leading_trailing_spaces():
    assert slugify('  Fazenda Teste  ') == 'fazenda-teste'


def test_slugify_leading_trailing_hiphens():
    assert slugify('-Fazenda Teste-') == 'fazenda-teste'


def test_classify_flat_slope():
    assert classify_slope(MaxSlopePercent.FLAT - 1) == SlopeClass.FLAT


def test_classify_gentle_slope():
    assert classify_slope(MaxSlopePercent.GENTLE - 1) == SlopeClass.GENTLE


def test_classify_moderate_slope():
    assert classify_slope(MaxSlopePercent.MODERATE - 1) == SlopeClass.MODERATE


def test_classify_strong_slope():
    assert classify_slope(MaxSlopePercent.STRONG - 1) == SlopeClass.STRONG


def test_classify_steep_slope():
    assert classify_slope(MaxSlopePercent.STEEP - 1) == SlopeClass.STEEP


def test_classify_very_steep_slope():
    assert (
        classify_slope(MaxSlopePercent.VERY_STEEP - 1) == SlopeClass.VERY_STEEP
    )
