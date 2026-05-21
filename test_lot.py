# test_lot.py
import pytest

from orderedmeta import Lot


# -------------------------
# Valid initialization
# -------------------------


def test_lot_initializes_correctly():
    lot = Lot("metal", 7, "ACME")

    assert lot.kind == "metal"
    assert lot.quantity == 7
    assert lot.name == "ACME"


def test_lot_as_csv():
    lot = Lot("wood", 5, "BOARD")

    assert lot.as_csv() == "kind=wood, quantity=5, name=BOARD"


# -------------------------
# kind validation
# -------------------------


@pytest.mark.parametrize(
    "kind",
    [
        "glass",
        "stone",
        "",
        None,
    ],
)
def test_invalid_kind(kind):
    with pytest.raises(ValueError):
        Lot(kind, 5, "ACME")


# -------------------------
# quantity validation
# -------------------------


@pytest.mark.parametrize(
    "quantity",
    [
        -1,
        0.2,
        10.2,
        100,
    ],
)
def test_quantity_out_of_range(quantity):
    with pytest.raises(ValueError):
        Lot("metal", quantity, "ACME")


@pytest.mark.parametrize(
    "quantity",
    [
        "7",
        None,
        [],
        {},
    ],
)
def test_quantity_wrong_type(quantity):
    with pytest.raises(TypeError):
        Lot("metal", quantity, "ACME")


# -------------------------
# name validation
# -------------------------


@pytest.mark.parametrize(
    "name",
    [
        "",
        "A",
        "ABCDEFGHIJKLM",  # 13 chars
    ],
)
def test_name_wrong_size(name):
    with pytest.raises(ValueError):
        Lot("metal", 5, name)


@pytest.mark.parametrize(
    "name",
    [
        "acme",
        "Wood",
        "abc123",
    ],
)
def test_name_not_uppercase(name):
    with pytest.raises(ValueError):
        Lot("metal", 5, name)


@pytest.mark.parametrize(
    "name",
    [
        123,
        None,
        [],
    ],
)
def test_name_wrong_type(name):
    with pytest.raises(TypeError):
        Lot("metal", 5, name)
