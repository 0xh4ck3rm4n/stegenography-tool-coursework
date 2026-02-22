import sys
def display_available():
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception:
        return False

def main():
    if "--cli" in sys.argv or not display_available():
        sys.argv = [a for a in sys.argv if a != "--cli"] 
        import cli
        cli.run()
    else:
        import gui
        root = gui.create_gui()
        root.mainloop()

if __name__ == "__main__":
    main()