from app.shared.utils import slugify


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
