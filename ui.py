import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
from database import Database

class InventoryApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Simple Retail Inventory Management System")
        self.root.geometry("1100x700")
        try:
            self.root.state('zoomed')
        except:
            pass # Linux/Mac might not support 'zoomed'

        # Variables
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()
        self.description_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.setup_ui()
        self.populate_list()

    def validate_numeric(self, p):
        if p == "" or p.isdigit():
            return True
        return False

    def validate_float(self, p):
        if p == "":
            return True
        try:
            float(p)
            return True
        except ValueError:
            return False

    def setup_ui(self):
        # Top Header
        header_frame = tb.Frame(self.root, bootstyle=PRIMARY)
        header_frame.pack(fill=X, side=TOP)
        
        tb.Label(header_frame, text="Simple Retail Inventory Management System", 
                 font=("Helvetica", 26, "bold"), bootstyle=INVERSE).pack(pady=25)

        # Footer Status Bar (Packed BEFORE container to ensure visibility)
        footer = tb.Frame(self.root, bootstyle=LIGHT, padding=15)
        footer.pack(fill=X, side=BOTTOM)

        self.valuation_label = tb.Label(footer, text="Total Inventory Value: ₱0.00", font=("Helvetica", 14, "bold"), bootstyle=DARK)
        self.valuation_label.pack(side=RIGHT, padx=25)

        self.alert_label = tb.Label(footer, text="", font=("Helvetica", 14, "bold"), bootstyle=DANGER)
        self.alert_label.pack(side=LEFT, padx=25)
        self.alert_label.bind("<Button-1>", self.show_low_stock_popup)

        # Main Container
        container = tb.Frame(self.root, padding=25)
        container.pack(fill=BOTH, expand=YES)

        # Left Column - Control Panel
        left_panel = tb.Frame(container, padding=10)
        left_panel.pack(side=LEFT, fill=Y)

        # Product Details Labelframe
        input_frame = tb.Labelframe(left_panel, text="Product Details", bootstyle=PRIMARY)
        input_frame.pack(fill=X, pady=(0, 20), padx=5)
        
        # Sub-frame for padding inside Labelframe
        input_inner = tb.Frame(input_frame, padding=15)
        input_inner.pack(fill=BOTH, expand=YES)

        # Input Grid
        LABEL_FONT = ("Helvetica", 13)
        ENTRY_FONT = ("Helvetica", 13)
        BTN_FONT = ("Helvetica", 12, "bold")
        
        # Configure fonts using Style system for compatibility
        style = tb.Style()
        style.configure('TEntry', font=ENTRY_FONT)
        style.configure('TCombobox', font=ENTRY_FONT)
        style.configure('TLabelframe.Label', font=("Helvetica", 14, "bold"))
        style.configure('TButton', font=BTN_FONT)
        
        grid_config = {"padx": 10, "pady": 15, "sticky": W}

        # Register validation commands
        vcmd_num = (self.root.register(self.validate_numeric), '%P')
        vcmd_float = (self.root.register(self.validate_float), '%P')
        
        tb.Label(input_inner, text="Product Name:", font=LABEL_FONT).grid(row=0, column=0, **grid_config)
        tb.Entry(input_inner, textvariable=self.name_var, width=35).grid(row=0, column=1, sticky=EW, padx=5)

        tb.Label(input_inner, text="Category:", font=LABEL_FONT).grid(row=1, column=0, **grid_config)
        categories = ["Electronics", "Clothing", "Groceries", "Home & Garden", "Toys", "Beauty", "Automotive", "Sports", "Books", "Others"]
        tb.Combobox(input_inner, textvariable=self.category_var, values=categories, width=33).grid(row=1, column=1, sticky=EW, padx=5)

        tb.Label(input_inner, text="Quantity:", font=LABEL_FONT).grid(row=2, column=0, **grid_config)
        tb.Entry(input_inner, textvariable=self.quantity_var, width=35, validate="key", validatecommand=vcmd_num).grid(row=2, column=1, sticky=EW, padx=5)

        tb.Label(input_inner, text="Price:", font=LABEL_FONT).grid(row=3, column=0, **grid_config)
        tb.Entry(input_inner, textvariable=self.price_var, width=35, validate="key", validatecommand=vcmd_float).grid(row=3, column=1, sticky=EW, padx=5)

        tb.Label(input_inner, text="Description:", font=LABEL_FONT).grid(row=4, column=0, **grid_config)
        tb.Entry(input_inner, textvariable=self.description_var, width=35).grid(row=4, column=1, sticky=EW, padx=5)

        input_inner.columnconfigure(1, weight=1)

        # Buttons Frame
        btn_frame = tb.Frame(left_panel)
        btn_frame.pack(fill=X, pady=10, side=TOP)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # CRUD Buttons - Larger and Even Width (Fonts set via Style)
        btn_padding = {"padx": 5, "pady": 10, "sticky": EW}
        
        tb.Button(btn_frame, text="Add Item", command=self.add_item, bootstyle=SUCCESS).grid(row=0, column=0, **btn_padding)
        tb.Button(btn_frame, text="Update Item", command=self.update_item, bootstyle=WARNING).grid(row=0, column=1, **btn_padding)
        tb.Button(btn_frame, text="Delete Item", command=self.delete_item, bootstyle=DANGER).grid(row=1, column=0, **btn_padding)
        tb.Button(btn_frame, text="Clear Fields", command=self.clear_inputs, bootstyle=SECONDARY).grid(row=1, column=1, **btn_padding)
        tb.Button(btn_frame, text="Sell Selected Item", command=self.sell_item, bootstyle=INFO).grid(row=2, column=0, columnspan=2, padx=5, pady=20, sticky=EW)

        # Right Column - Data View
        right_panel = tb.Frame(container, padding=10)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Search Bar
        search_frame = tb.Frame(right_panel)
        search_frame.pack(fill=X, pady=(0, 20))
        
        tb.Entry(search_frame, textvariable=self.search_var).pack(side=LEFT, fill=X, expand=YES, padx=(0, 15))
        tb.Button(search_frame, text="Search", command=self.search_inventory, bootstyle=PRIMARY).pack(side=LEFT, padx=5)
        tb.Button(search_frame, text="Show All", command=self.populate_list, bootstyle=SECONDARY).pack(side=LEFT)

        # Table Section
        self.table_coldata = [
            {"text": "Product Name", "stretch": True, "width": 220},
            {"text": "Category", "stretch": True, "width": 160},
            {"text": "Quantity", "stretch": False, "width": 110},
            {"text": "Price", "stretch": False, "width": 140},
            {"text": "Description", "stretch": True, "width": 300}
        ]
        
        self.dt = Tableview(
            master=right_panel,
            coldata=self.table_coldata,
            rowdata=[],
            paginated=True,
            searchable=False,
            bootstyle=PRIMARY,
        )
        self.dt.pack(fill=BOTH, expand=YES)
        
        self.tree = self.dt.view
        # Smooth Treeview Styling
        style.configure('Treeview', font=("Helvetica", 12), rowheight=45, borderwidth=0)
        style.configure('Treeview.Heading', font=("Helvetica", 13, "bold"), borderwidth=1)
        
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

    def populate_list(self):
        # We need to bypass Tableview's automatic mapping to keep ID as iid
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for row in self.db.fetch_all_products():
            qty_formatted = f"{row.quantity:,}"
            price_formatted = f"₱{row.price:,.2f}"
            self.tree.insert("", tk.END, iid=row.id, values=(row.name, row.category, qty_formatted, price_formatted, row.description))
        self.update_status()

    def select_item(self, event):
        try:
            selection = self.tree.selection()
            if not selection:
                return
            selected_item = selection[0]
            # Use iid for the ID, and ensure it's an integer
            self.selected_id = int(selected_item)
            row = self.tree.item(selected_item)['values']
            self.name_var.set(row[0])
            self.category_var.set(row[1])
            
            qty_str = str(row[2]).replace(',', '')
            price_str = str(row[3]).replace(',', '').replace('₱', '').strip()
            
            self.quantity_var.set(int(qty_str))
            self.price_var.set(float(price_str))
            self.description_var.set(row[4])
        except (IndexError, ValueError):
            pass

    def add_item(self):
        if not self.validate_inputs():
            return
        
        # If an item was selected, deselect it before adding as a new item
        if hasattr(self, 'selected_id'):
            del self.selected_id
            self.tree.selection_remove(self.tree.selection())

        try:
            self.db.insert_product(self.name_var.get().strip(), self.category_var.get(), self.quantity_var.get(), self.price_var.get(), self.description_var.get().strip())
            self.clear_inputs()
            self.populate_list()
            messagebox.showinfo("Success", "Product added successfully")
        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Could not add product: {str(e)}")

    def update_item(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Warning", "Please select a product to update")
            return
        if not self.validate_inputs():
            return
        try:
            self.db.update_product(self.selected_id, self.name_var.get().strip(), self.category_var.get(), self.quantity_var.get(), self.price_var.get(), self.description_var.get().strip())
            self.clear_inputs()
            self.populate_list()
            messagebox.showinfo("Success", "Product updated successfully")
        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Could not update product: {str(e)}")

    def delete_item(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        if messagebox.askyesno("Confirm", "Delete this product permanently?"):
            try:
                self.db.delete_product(self.selected_id)
                self.clear_inputs()
                self.populate_list()
                messagebox.showinfo("Success", "Product deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete product: {str(e)}")

    def sell_item(self):
        if not hasattr(self, 'selected_id'):
            messagebox.showwarning("Warning", "Please select a product to sell")
            return
        
        try:
            current_qty = self.quantity_var.get()
            qty_to_sell = simpledialog.askinteger("Sell Item", f"Quantity to sell (In Stock: {current_qty}):", minvalue=1)
            
            if qty_to_sell:
                if qty_to_sell > current_qty:
                    messagebox.showerror("Error", "Insufficient stock!")
                    return

                new_qty = current_qty - qty_to_sell
                self.db.update_product(self.selected_id, self.name_var.get(), self.category_var.get(), new_qty, self.price_var.get(), self.description_var.get())
                self.populate_list()
                messagebox.showinfo("Success", f"Sold {qty_to_sell} units")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def validate_inputs(self):
        # Enforce all fields must be filled
        if not self.name_var.get().strip():
            messagebox.showwarning("Validation Error", "Product Name is required!")
            return False
        
        if not self.category_var.get().strip():
            messagebox.showwarning("Validation Error", "Please select or enter a Category!")
            return False
            
        if not self.description_var.get().strip():
            messagebox.showwarning("Validation Error", "Description is required!")
            return False

        try:
            qty = self.quantity_var.get()
            price = self.price_var.get()
            
            if qty < 0:
                messagebox.showwarning("Validation Error", "Quantity cannot be negative!")
                return False
            if price <= 0:
                messagebox.showwarning("Validation Error", "Price must be greater than zero!")
                return False
        except (tk.TclError, ValueError):
            messagebox.showwarning("Validation Error", "Quantity and Price must be valid numbers!")
            return False
            
        return True

    def search_inventory(self):
        query = self.search_var.get()
        if not query:
            self.populate_list()
            return

        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for row in self.db.search_products(query):
            qty_formatted = f"{row.quantity:,}"
            price_formatted = f"₱{row.price:,.2f}"
            self.tree.insert("", tk.END, iid=row.id, values=(row.name, row.category, qty_formatted, price_formatted, row.description))

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
        self.valuation_label.config(text=f"Total Inventory Value: ₱{total_value:,.2f}")
        
        low_stock = self.db.get_low_stock_products()
        if low_stock:
            self.alert_label.config(text=f"⚠️ Low Stock Alert: {len(low_stock)} items")
        else:
            self.alert_label.config(text="")

    def show_low_stock_popup(self, event):
        low_stock = self.db.get_low_stock_products()
        if not low_stock: return

        popup = tb.Toplevel(self.root)
        popup.title("Low Stock Items")
        popup.geometry("600x400")
        
        tb.Label(popup, text="Low Stock Alert", font=("Helvetica", 16, "bold"), bootstyle=DANGER).pack(pady=10)

        tree = tb.Treeview(popup, columns=("Name", "Category", "Quantity"), show="headings", bootstyle=DANGER)
        tree.heading("Name", text="Name")
        tree.heading("Category", text="Category")
        tree.heading("Quantity", text="Qty")
        tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        for row in low_stock:
            tree.insert("", tk.END, values=(row.name, row.category, row.quantity))
        
        tb.Button(popup, text="Close", command=popup.destroy, bootstyle=SECONDARY).pack(pady=10)
