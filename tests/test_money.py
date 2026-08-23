from ledger.money import format_cents


def test_format_positive():
    assert format_cents(1250) == "$12.50"


def test_format_negative():
    assert format_cents(-815) == "-$8.15"


def test_format_zero():
    assert format_cents(0) == "$0.00"


def test_format_thousands_separator():
    assert format_cents(123456789) == "$1,234,567.89"
