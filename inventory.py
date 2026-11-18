import sqlite3

DB_NAME = "inventory.db"


def connect():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                quantity INTEGER NOT NULL CHECK(quantity >= 0)
            )
        """)


def add_product(product_id, name, price, quantity):
    product_id = product_id.strip()
    name = name.strip()
    if not product_id or not name:
        raise ValueError("Product ID and name are required.")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        raise ValueError("Price must be a non-negative number.")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
        raise ValueError("Quantity must be a non-negative integer.")

    try:
        with connect() as connection:
            connection.execute(
                "INSERT INTO products (product_id, name, price, quantity) VALUES (?, ?, ?, ?)",
                (product_id, name, float(price), quantity)
            )
    except sqlite3.IntegrityError as error:
        raise ValueError("Product ID already exists or product data is invalid.") from error


def list_products():
    with connect() as connection:
        return connection.execute(
            "SELECT product_id, name, price, quantity FROM products ORDER BY name"
        ).fetchall()


def find_product(search_term):
    term = f"%{search_term.strip()}%"
    with connect() as connection:
        return connection.execute(
            """SELECT product_id, name, price, quantity
               FROM products WHERE product_id LIKE ? OR name LIKE ?
               ORDER BY name""",
            (term, term)
        ).fetchall()


def update_stock(product_id, change):
    if isinstance(change, bool) or not isinstance(change, int) or change == 0:
        raise ValueError("Stock change must be a non-zero integer.")

    with connect() as connection:
        cursor = connection.execute(
            """UPDATE products SET quantity = quantity + ?
               WHERE product_id = ? AND quantity + ? >= 0""",
            (change, product_id, change)
        )
        if cursor.rowcount == 0:
            exists = connection.execute(
                "SELECT 1 FROM products WHERE product_id = ?", (product_id,)
            ).fetchone()
            if exists:
                raise ValueError("Stock cannot become negative.")
            raise ValueError("Product ID was not found.")


def low_stock(threshold=5):
    if threshold < 0:
        raise ValueError("Threshold cannot be negative.")
    with connect() as connection:
        return connection.execute(
            """SELECT product_id, name, price, quantity
               FROM products WHERE quantity <= ? ORDER BY quantity""",
            (threshold,)
        ).fetchall()


def main():
    initialize_database()
    while True:
        print("\\n=== INVENTORY MANAGEMENT ===")
        print("1. Add product")
        print("2. View all products")
        print("3. Search product")
        print("4. Update stock")
        print("5. Show low-stock products")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                product_id = input("Product ID: ")
                name = input("Product name: ")
                price = float(input("Price: "))
                quantity = int(input("Opening quantity: "))
                add_product(product_id, name, price, quantity)
                print("Product added.")
            elif choice == "2":
                for product in list_products():
                    print(product)
            elif choice == "3":
                for product in find_product(input("Enter ID or name: ")):
                    print(product)
            elif choice == "4":
                product_id = input("Product ID: ")
                change = int(input("Quantity change (+ to add, - to remove): "))
                update_stock(product_id, change)
                print("Stock updated.")
            elif choice == "5":
                threshold = int(input("Low-stock threshold (default 5): ") or "5")
                for product in low_stock(threshold):
                    print(product)
            elif choice == "6":
                print("Goodbye.")
                break
            else:
                print("Please choose a number from 1 to 6.")
        except (ValueError, sqlite3.Error) as error:
            print(f"Could not complete operation: {error}")


if __name__ == "__main__":
    main()
