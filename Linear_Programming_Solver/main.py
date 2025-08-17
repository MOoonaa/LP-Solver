from ui import LPSolverApp
import tkinter as tk

def main():
    root = tk.Tk()   
    app = LPSolverApp(root)  
    root.mainloop()

if __name__ == "__main__":
    main()