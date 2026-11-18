import pytest
import inventory


@pytest.fixture(autouse=True)
def use_test_database(tmp_path, monkeypatch):
    test_db = tmp_path / "test_inventory.db"
    monkeypatch.setattr(inventory, "DB_NAME", str(test_db))
    inventory.initialize_database()


def test_add_and_list_product():
    inventory.add_product("P101", "Notebook", 45.5, 10)
    products = inventory.list_products()
    assert len(products) == 1
    assert products[0][0] == "P101"
    assert products[0][3] == 10


def test_duplicate_product_id():
    inventory.add_product("P101", "Notebook", 45, 10)
    with pytest.raises(ValueError):
        inventory.add_product("P101", "Pen", 10, 20)


def test_search_by_name():
    inventory.add_product("P101", "Notebook", 45, 10)
    assert len(inventory.find_product("Note")) == 1


def test_reject_negative_price():
    with pytest.raises(ValueError):
        inventory.add_product("P102", "Pen", -2, 5)


def test_reject_negative_quantity():
    with pytest.raises(ValueError):
        inventory.add_product("P103", "Pencil", 5, -1)


def test_update_stock():
    inventory.add_product("P101", "Notebook", 45, 10)
    inventory.update_stock("P101", -3)
    assert inventory.list_products()[0][3] == 7


def test_stock_cannot_be_negative():
    inventory.add_product("P101", "Notebook", 45, 2)
    with pytest.raises(ValueError):
        inventory.update_stock("P101", -3)


def test_low_stock():
    inventory.add_product("P101", "Notebook", 45, 3)
    assert len(inventory.low_stock(5)) == 1
