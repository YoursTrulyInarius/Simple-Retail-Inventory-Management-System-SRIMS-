import tkinter as tk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database

class InventoryApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Simple Retail Inventory Management System")
        self.root.geometry("1000x600")

        # Variables
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()
        self.description_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.setup_ui()
        self.populate_list()

    def setup_ui(self):
        # Style Constants
        TITLE_FONT = ("Segoe UI", 24, "bold")
        HEADER_FONT = ("Segoe UI", 12, "bold")
        LABEL_FONT = ("Segoe UI", 10)
        ENTRY_FONT = ("Segoe UI", 10)
        BTN_FONT = ("Segoe UI", 10, "bold")
        
        BG_COLOR = "#f4f6f7"
        HEADER_BG = "#2c3e50"
        SIDEBAR_BG = "#ffffff"
        
        self.root.configure(bg=BG_COLOR)

        # Top Frame - Title
        top_frame = tk.Frame(self.root, bg=HEADER_BG, height=80)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = tk.Label(top_frame, text="Retail Inventory Management", font=TITLE_FONT, bg=HEADER_BG, fg="white")
        title_label.pack(pady=15)

        # Main Container
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left Frame - Inputs (Sidebar)
        left_frame = tk.Frame(main_frame, bg=SIDEBAR_BG, relief=tk.RIDGE, borderwidth=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), ipadx=10, ipady=10)
        
        tk.Label(left_frame, text="Product Details", font=HEADER_FONT, bg=SIDEBAR_BG, fg="#34495e").pack(pady=(10, 20))

        input_container = tk.Frame(left_frame, bg=SIDEBAR_BG)
        input_container.pack(fill=tk.X, padx=10)

        # Input Fields using Grid
        
        # Name
        tk.Label(input_container, text="Name:", font=LABEL_FONT, bg=SIDEBAR_BG, anchor="w").grid(row=0, column=0, sticky="w", pady=(5, 0))
        tk.Entry(input_container, textvariable=self.name_var, font=ENTRY_FONT, relief=tk.SOLID, borderwidth=1).grid(row=0, column=1, sticky="ew", pady=(5, 10), padx=(5, 0), ipady=3)

        # Category (Combobox)
        tk.Label(input_container, text="Category:", font=LABEL_FONT, bg=SIDEBAR_BG, anchor="w").grid(row=1, column=0, sticky="w", pady=(5, 0))
        category_combo = ttk.Combobox(input_container, textvariable=self.category_var, font=ENTRY_FONT, values=["Electronics", "Clothing", "Groceries", "Home & Garden", "Toys", "Beauty", "Automotive", "Sports", "Books", "Others"])
        category_combo.grid(row=1, column=1, sticky="ew", pady=(5, 10), padx=(5, 0), ipady=3)

        # Quantity
        tk.Label(input_container, text="Quantity:", font=LABEL_FONT, bg=SIDEBAR_BG, anchor="w").grid(row=2, column=0, sticky="w", pady=(5, 0))
        tk.Entry(input_container, textvariable=self.quantity_var, font=ENTRY_FONT, relief=tk.SOLID, borderwidth=1).grid(row=2, column=1, sticky="ew", pady=(5, 10), padx=(5, 0), ipady=3)

        # Price
        tk.Label(input_container, text="Price:", font=LABEL_FONT, bg=SIDEBAR_BG, anchor="w").grid(row=3, column=0, sticky="w", pady=(5, 0))
        tk.Entry(input_container, textvariable=self.price_var, font=ENTRY_FONT, relief=tk.SOLID, borderwidth=1).grid(row=3, column=1, sticky="ew", pady=(5, 10), padx=(5, 0), ipady=3)

        # Description
        tk.Label(input_container, text="Description:", font=LABEL_FONT, bg=SIDEBAR_BG, anchor="w").grid(row=4, column=0, sticky="w", pady=(5, 0))
        tk.Entry(input_container, textvariable=self.description_var, font=ENTRY_FONT, relief=tk.SOLID, borderwidth=1).grid(row=4, column=1, sticky="ew", pady=(5, 10), padx=(5, 0), ipady=3)

        input_container.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = tk.Frame(left_frame, bg=SIDEBAR_BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=20)
        
        btn_style = {"font": BTN_FONT, "relief": tk.FLAT, "cursor": "hand2", "width": 10}
        
        tk.Button(btn_frame, text="Add", command=self.add_item, bg="#27ae60", fg="white", **btn_style).grid(row=0, column=0, padx=2, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Update", command=self.update_item, bg="#f39c12", fg="white", **btn_style).grid(row=0, column=1, padx=2, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Delete", command=self.delete_item, bg="#c0392b", fg="white", **btn_style).grid(row=1, column=0, padx=2, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Clear", command=self.clear_inputs, bg="#95a5a6", fg="white", **btn_style).grid(row=1, column=1, padx=2, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Sell", command=self.sell_item, bg="#8e44ad", fg="white", **btn_style).grid(row=2, column=0, columnspan=2, padx=2, pady=5, sticky="ew")
        
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # Right Frame - List and Search
        right_frame = tk.Frame(main_frame, bg=BG_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Search Bar
        search_frame = tk.Frame(right_frame, bg=BG_COLOR)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", font=LABEL_FONT, bg=BG_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        tk.Entry(search_frame, textvariable=self.search_var, font=ENTRY_FONT, relief=tk.SOLID, borderwidth=1).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        tk.Button(search_frame, text="Search", command=self.search_inventory, bg="#3498db", fg="white", font=BTN_FONT, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.populate_list, bg="#34495e", fg="white", font=BTN_FONT, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT)

        # Style for Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=LABEL_FONT, rowheight=30, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=HEADER_FONT, background="#ecf0f1", foreground="#2c3e50", relief="raised")
        style.map("Treeview", background=[('selected', '#3498db')])

        # Treeview
        columns = ("ID", "Name", "Category", "Quantity", "Price", "Description")
        display_cols = ("Name", "Category", "Quantity", "Price", "Description")
        
        tree_frame = tk.Frame(right_frame, bg="white", relief=tk.SOLID, borderwidth=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, displaycolumns=display_cols, show="headings", selectmode="browse")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.heading("Name", text="Name", anchor="w")
        self.tree.heading("Category", text="Category", anchor="w")
        self.tree.heading("Quantity", text="Qty", anchor="center")
        self.tree.heading("Price", text="Price", anchor="e")
        self.tree.heading("Description", text="Description", anchor="w")
        
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Category", width=100, anchor="w")
        self.tree.column("Quantity", width=60, anchor="center")
        self.tree.column("Price", width=80, anchor="e")
        self.tree.column("Description", width=200, anchor="w")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        # Status Bar
        self.status_frame = tk.Frame(right_frame, bg="#dfe6e9", height=40, relief=tk.FLAT)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.valuation_label = tk.Label(self.status_frame, text="Total Value: ₱0.00", font=("Segoe UI", 11, "bold"), bg="#dfe6e9", fg="#2c3e50")
        self.valuation_label.pack(side=tk.RIGHT, padx=15, pady=5)
        
        self.alert_label = tk.Label(self.status_frame, text="", font=("Segoe UI", 11, "bold"), fg="#e74c3c", bg="#dfe6e9", cursor="hand2")
        self.alert_label.pack(side=tk.LEFT, padx=15, pady=5)
        self.alert_label.bind("<Button-1>", self.show_low_stock_popup)

    def populate_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        self.tree.tag_configure('odd', background='#f9f9f9')
        self.tree.tag_configure('even', background='white')

        for i, row in enumerate(self.db.fetch_all_products()):
            tag = 'even' if i % 2 == 0 else 'odd'
            qty_formatted = f"{row.quantity:,}"
            price_formatted = f"₱{row.price:,.2f}   " # Added padding
            self.tree.insert("", tk.END, values=(row.id, row.name, row.category, qty_formatted, price_formatted, row.description), tags=(tag,))
        self.update_status()

    def select_item(self, event):
        try:
            selected_item = self.tree.selection()[0]
            row = self.tree.item(selected_item)['values']
            self.selected_id = row[0]
            self.name_var.set(row[1])
            self.category_var.set(row[2])
            
            # Remove commas, currency symbols, and padding for editing
            qty_str = str(row[3]).replace(',', '')
            price_str = str(row[4]).replace(',', '').replace('₱', '').strip()
            
            self.quantity_var.set(int(qty_str))
            self.price_var.set(float(price_str))
            self.description_var.set(row[5])
        except (IndexError, ValueError):
            pass

    def add_item(self):
        if not self.validate_inputs():
            return
        try:
            self.db.insert_product(self.name_var.get(), self.category_var.get(), self.quantity_var.get(), self.price_var.get(), self.description_var.get())
            self.clear_inputs()
            self.populate_list()
            messagebox.showinfo("Success", "Product added successfully")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def update_item(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showerror("Error", "No item selected")
            return
        if not self.validate_inputs():
            return
        try:
            self.db.update_product(self.selected_id, self.name_var.get(), self.category_var.get(), self.quantity_var.get(), self.price_var.get(), self.description_var.get())
            self.clear_inputs()
            self.populate_list()
            messagebox.showinfo("Success", "Product updated successfully")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def delete_item(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showerror("Error", "No item selected")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            try:
                self.db.delete_product(self.selected_id)
                self.clear_inputs()
                self.populate_list()
                messagebox.showinfo("Success", "Product deleted successfully")
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def sell_item(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showerror("Error", "No item selected")
            return
        
        try:
            current_qty = self.quantity_var.get()
            
            # Ask for quantity
            qty_to_sell = simpledialog.askinteger("Sell Item", f"Enter quantity to sell (Current: {current_qty}):", minvalue=1)
            
            if qty_to_sell:
                if qty_to_sell > current_qty:
                    messagebox.showerror("Error", f"Insufficient stock! You only have {current_qty} items.")
                    return

                new_qty = current_qty - qty_to_sell
                self.quantity_var.set(new_qty)
                
                # Update in DB
                self.db.update_product(self.selected_id, self.name_var.get(), self.category_var.get(), new_qty, self.price_var.get(), self.description_var.get())
                
                self.populate_list()
                messagebox.showinfo("Success", f"Sold {qty_to_sell} items successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def validate_inputs(self):
        if self.name_var.get().strip() == "":
            messagebox.showerror("Validation Error", "Name is required")
            return False
        try:
            qty = self.quantity_var.get()
            if qty < 0:
                raise ValueError
        except (tk.TclError, ValueError):
            messagebox.showerror("Validation Error", "Quantity must be a valid non-negative integer")
            return False
        
        try:
            price = self.price_var.get()
            if price < 0:
                raise ValueError
        except (tk.TclError, ValueError):
            messagebox.showerror("Validation Error", "Price must be a valid non-negative number")
            return False
            
        return True

    def search_inventory(self):
        query = self.search_var.get()
        if query:
            for i in self.tree.get_children():
                self.tree.delete(i)
            for i, row in enumerate(self.db.search_products(query)):
                tag = 'even' if i % 2 == 0 else 'odd'
                qty_formatted = f"{row.quantity:,}"
                price_formatted = f"₱{row.price:,.2f}   " # Added padding
                self.tree.insert("", tk.END, values=(row.id, row.name, row.category, qty_formatted, price_formatted, row.description), tags=(tag,))
        else:
            self.populate_list()

    def clear_inputs(self):
        self.name_var.set("")
        self.category_var.set("")
        self.quantity_var.set(0)
        self.price_var.set(0.0)
        self.description_var.set("")
        if hasattr(self, 'selected_id'):
            del self.selected_id

    def update_status(self):
        total_value = self.db.get_total_valuation()
        self.valuation_label.config(text=f"Total Value: ₱{total_value:,.2f}")
        
        low_stock = self.db.get_low_stock_products()
        if low_stock:
            self.alert_label.config(text=f"Low Stock Alert: {len(low_stock)} items")
        else:
            self.alert_label.config(text="")

    def show_low_stock_popup(self, event):
        low_stock = self.db.get_low_stock_products()
        if not low_stock:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Low Stock Items")
        popup.geometry("600x400")
        popup.configure(bg="#f4f6f7")

        tk.Label(popup, text="Low Stock Alert", font=("Segoe UI", 16, "bold"), bg="#f4f6f7", fg="#e74c3c").pack(pady=10)

        # Treeview for popup
        columns = ("Name", "Category", "Quantity", "Price")
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        
        tree.heading("Name", text="Name")
        tree.heading("Category", text="Category")
        tree.heading("Quantity", text="Qty")
        tree.heading("Price", text="Price")
        
        tree.column("Name", width=200)
        tree.column("Category", width=100)
        tree.column("Quantity", width=50, anchor="center")
        tree.column("Price", width=80, anchor="e")

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for row in low_stock:
            qty_formatted = f"{row.quantity:,}"
            price_formatted = f"₱{row.price:,.2f}   "
            tree.insert("", tk.END, values=(row.name, row.category, qty_formatted, price_formatted))
        
        tk.Button(popup, text="Close", command=popup.destroy, bg="#95a5a6", fg="white", font=("Segoe UI", 10)).pack(pady=10)
