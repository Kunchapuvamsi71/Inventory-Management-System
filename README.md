# Inventory Management System

A command-line Python inventory tracker using SQLite.

## Features
- Add products with unique IDs
- List and search products
- Increase or decrease stock
- Prevent negative price and stock values
- Show products at or below a low-stock threshold

## Run
```bash
python inventory.py
```

The SQLite database (`inventory.db`) is created automatically.

## Run automated tests
```bash
python -m pip install pytest
python -m pytest -v
```

The tests use a temporary database so they do not change your real inventory file.

## Notes
This is an educational prototype. A commercial version should add authentication, role permissions, backups, audit history, and stronger operational monitoring.
