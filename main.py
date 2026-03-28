import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.app import InventoryApp

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
