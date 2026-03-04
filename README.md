# Simple Retail Inventory Management System

A simple, user-friendly inventory management application built with Python and Tkinter, featuring a modern Bootstrap-inspired interface. This application allows users to manage product stock, track sales, and monitor inventory value.

## Features

-   **Product Management**: Add, update, and delete products easily.
-   **Inventory Tracking**: View current stock levels, prices, and categories.
-   **Search Functionality**: Search for products by name or category.
-   **Sales Recording**: "Sell" items to deduct from inventory automatically.
-   **Low Stock Alerts**: Visual alerts when product quantity falls below a threshold (default: 5).
-   **Valuation**: Real-time calculation of total inventory value.
-   **Data Persistence**: Uses SQLite database (`inventory.db`) to save data.

## Python Compatibility

This application is compatible with modern versions of Python.

- **Supported Python Versions**: Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12 and later.
- **Incompatible Python Versions**: Python 2.x and Python versions earlier than 3.6 are **not supported**.

## Technologies Used

-   **Python**: Core programming language.
-   **Tkinter**: Standard GUI framework for Python.
-   **ttkbootstrap**: Modern themed widget extension for Tkinter (provides the Bootstrap aesthetic).
-   **SQLite**: Lightweight disk-based database.

## Installation and Usage

1.  **Prerequisites**: Ensure you have Python (version 3.6 or later) installed on your system.
2.  **Clone/Download**: Download the source code to your local machine.
3.  **Install Dependencies**:
    Open a terminal or command prompt in the project directory and run:
    ```bash
    pip install ttkbootstrap
    ```
4.  **Run the Application**:
    In the same terminal, run:
    ```bash
    python main.py
    ```
5.  **Database**: The `inventory.db` file will be created automatically upon the first run.

6.  **STATUS**: 98%

