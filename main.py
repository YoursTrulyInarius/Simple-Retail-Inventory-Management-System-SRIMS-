import ttkbootstrap as tb
from ui import InventoryApp

if __name__ == "__main__":
    # Use ttkbootstrap Window instead of tk.Tk
    # Themes: flatly, darkly, superhero, cosmo, lumen, yeti, etc.
    root = tb.Window(themename="flatly")
    app = InventoryApp(root)
    root.mainloop()
