import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import numpy as np
from PIL import Image, ImageTk   
from graphical import graphical_solver
from simplex import SimplexSolver

class LPSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Programming Solver")
        self.root.geometry("900x900")
        image=Image.open('loading.jpg')
        self.icon=ImageTk.PhotoImage(image)
        self.root.iconphoto(True,self.icon)
       
        # Create notebook for different solvers
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both' ,expand=True)
        
        # Graphical Solver Tab
        self.create_graphical_tab()
        
        # Simplex Solver Tab
        self.create_simplex_tab()
        
    
    def create_graphical_tab(self):

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Graphical Solver")
        
        # Problem Type
        ttk.Label(tab, text="Problem Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.graphical_opt_type = tk.StringVar(value="max")
        ttk.Radiobutton(tab, text="Maximize", variable=self.graphical_opt_type, value="max").grid(row=0, column=1,sticky=tk.W)
        ttk.Radiobutton(tab, text="Minimize", variable=self.graphical_opt_type, value="min").grid(row=0, column=2,sticky=tk.W)
        
        # Objective Function
        ttk.Label(tab, text="Objective Coefficients:").grid(row=1, column=0,padx=5, pady=5,sticky=tk.W)
        ttk.Label(tab, text="x").grid(row=1, column=2 ,sticky=tk.W)
        ttk.Label(tab, text="y").grid(row=1, column=4,sticky=tk.W)
        
        self.obj_x = tk.DoubleVar(value=1)
        self.obj_y = tk.DoubleVar(value=1)
        ttk.Entry(tab, textvariable=self.obj_x, width=5).grid(row=1, column=1,sticky=tk.W)
        ttk.Entry(tab, textvariable=self.obj_y, width=5).grid(row=1, column=3,sticky=tk.W)
        
        # Constraints Frame
        constraints_frame = ttk.LabelFrame(tab, text="Constraints")
        constraints_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky=tk.W+tk.E)
        
        # Constraints header
        ttk.Label(constraints_frame, text="x  ").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(constraints_frame, text="y").grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(constraints_frame, text="RHS").grid(row=0, column=6, padx=5, pady=5)
        
        self.constraint_entries = []
        for i in range(3):
            self.add_constraint_row(constraints_frame, i+1)
        
        # Add/Remove constraint buttons
        button_frame = ttk.Frame(constraints_frame)
        button_frame.grid(row=10, column=0, columnspan=7, pady=5)
        ttk.Button(button_frame, text="Add Constraint", command=lambda: self.add_constraint_row(constraints_frame, len(self.constraint_entries)+1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Constraint", command=self.remove_constraint_row).pack(side=tk.LEFT, padx=5)
        
        # Solve Button
        ttk.Button(tab, text="Solve Graphically", command=self.solve_graphical).grid(row=3, column=0, columnspan=5, pady=10)
        
        # Results
        self.graphical_results = Text(tab, height=10, width=80)
        self.graphical_results.grid(row=4, column=0, columnspan=5, padx=10, pady=10)
    
    def add_constraint_row(self, frame, row):
      
        coeff_x = tk.DoubleVar(value=1)
        coeff_y = tk.DoubleVar(value=1)
        rhs = tk.DoubleVar(value=1)
        sense = tk.StringVar(value="<=")
        
        # Create all widgets
        x_entry = ttk.Entry(frame, textvariable=coeff_x, width=5)
        plus_label = ttk.Label(frame, text="x +")
        y_entry = ttk.Entry(frame, textvariable=coeff_y, width=5)
        y_label = ttk.Label(frame, text="y")
        sense_combo = ttk.Combobox(frame, textvariable=sense, 
                                values=["<=", ">=", "="], 
                                width=3, state="readonly")
        rhs_entry = ttk.Entry(frame, textvariable=rhs, width=5)
        
        # Grid all widgets
        x_entry.grid(row=row, column=1, padx=2, pady=2)
        plus_label.grid(row=row, column=2, padx=0, pady=2)
        y_entry.grid(row=row, column=3, padx=2, pady=2)
        y_label.grid(row=row, column=4, padx=0, pady=2)
        sense_combo.grid(row=row, column=5, padx=2, pady=2)
        rhs_entry.grid(row=row, column=6, padx=2, pady=2)
        
        # Store all widgets and variables
        self.constraint_entries.append({
            'coeff_x': coeff_x,
            'coeff_y': coeff_y,
            'sense': sense,
            'rhs': rhs,
            'widgets': [x_entry, plus_label, y_entry, y_label, sense_combo, rhs_entry]
        })
    
    def remove_constraint_row(self):
        if len(self.constraint_entries) > 1:  
            # Get the last constraint entry
            last_entry = self.constraint_entries[-1]
            
            # Destroy all widgets in the row
            for widget in last_entry['widgets']:
                widget.destroy()
                
            # Remove from our tracking list
            self.constraint_entries.pop()
    
    def solve_graphical(self):
        try:
            # Get objective coefficients
            obj_coeffs = (self.obj_x.get(), self.obj_y.get())
            
            # Get constraints
            constraints = []
            for entry in self.constraint_entries:
                a = entry['coeff_x'].get()
                b = entry['coeff_y'].get()
                c = entry['rhs'].get()
                sense = entry['sense'].get()
                constraints.append((a, b, c, sense))
            
            # Solve
            result = graphical_solver(
                opt_type=self.graphical_opt_type.get(),
                obj_coeffs=obj_coeffs,
                constraints=constraints
            )
            
            # Display results
            self.graphical_results.delete(1.0, tk.END)
            self.graphical_results.insert(tk.END, "=== LP Solution ===\n")
            self.graphical_results.insert(tk.END, f"Status: {result['status']}\n")
            
            if result['status'] == 'optimal':
                self.graphical_results.insert(tk.END, f"Optimal Value: {result['opt_value']:.4f}\n")
                self.graphical_results.insert(tk.END, "Optimal Points:\n")
                for point in result['opt_points']:
                    self.graphical_results.insert(tk.END, f"  ({point[0]:.4f}, {point[1]:.4f})\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def create_simplex_tab(self):

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Simplex Solver")
        
        # Problem Type
        ttk.Label(tab, text="Problem Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.simplex_opt_type = tk.StringVar(value="max")
        ttk.Radiobutton(tab, text="Maximize", variable=self.simplex_opt_type, value="max").grid(row=0, column=1,  sticky=tk.W)
        ttk.Radiobutton(tab, text="Minimize", variable=self.simplex_opt_type, value="min").grid(row=0, column=2, sticky=tk.W)
        
        # Variables Frame
        vars_frame = ttk.LabelFrame(tab, text="Variables")
        vars_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)
        
        ttk.Label(vars_frame, text="Number of Variables:").grid(row=0, column=0, padx=5, pady=5)
        self.num_vars = tk.IntVar(value=2)
        ttk.Spinbox(vars_frame, from_=1, to=10, textvariable=self.num_vars, width=5, command=self.update_variable_count).grid(row=0, column=1, padx=5, pady=5)
        
        # Objective Function
        self.objective_entries = []
        self.objective_frame = ttk.LabelFrame(vars_frame, text="Objective Coefficients")
        self.objective_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        self.update_objective_entries()
        
        # Constraints
        constraints_frame = ttk.LabelFrame(tab, text="Constraints")
        constraints_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)
        
        # Constraints header
        ttk.Label(constraints_frame, text="Coefficients").grid(row=0, column=0, columnspan=10, padx=5, pady=5)
        
        # Constraint entries (start with 2 empty constraints)
        self.simplex_constraint_entries = []
        for i in range(2):
            self.add_simplex_constraint_row(constraints_frame, i+1)
        
        # Add/Remove constraint buttons
        button_frame = ttk.Frame(constraints_frame)
        button_frame.grid(row=10, column=0, columnspan=10, pady=5)
        ttk.Button(button_frame, text="Add Constraint", command=lambda: self.add_simplex_constraint_row(constraints_frame, len(self.simplex_constraint_entries)+1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Constraint", command=self.remove_simplex_constraint_row).pack(side=tk.LEFT, padx=5)
        
        # Solve Button
        ttk.Button(tab, text="Solve with Simplex", command=self.solve_simplex).grid(row=3, column=0, columnspan=3, pady=10)
        
        # Results
        self.simplex_results =Text(tab, height=10, width=80)
        self.simplex_results.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
    
    def update_variable_count(self):

        self.update_objective_entries()
        self.update_constraints()
    
    def update_objective_entries(self):

        # Clear existing entries
        for widget in self.objective_frame.winfo_children():
            widget.destroy()
        
        self.objective_entries = []
        num_vars = self.num_vars.get()
        
        for i in range(num_vars):
            ttk.Label(self.objective_frame, text=f"x{i+1}:").grid(row=0, column=i*2, padx=5, pady=5)
            var = tk.DoubleVar(value=1)
            ttk.Entry(self.objective_frame, textvariable=var, width=5).grid(row=0, column=i*2+1, padx=5, pady=5)
            self.objective_entries.append(var)
    def update_constraints(self):

        # Store current constraints data
        current_constraints = []
        for entry in self.simplex_constraint_entries:
            current_constraints.append({
                'coeffs': [var.get() for var in entry['coeffs']],
                'sense': entry['sense'].get(),
                'rhs': entry['rhs'].get()
            })
        
        # Clear all existing constraint widgets
        for entry in self.simplex_constraint_entries:
            for widget in entry['widgets']:
                widget.destroy()
        self.simplex_constraint_entries = []
        
        # Recreate constraints with new variable count
        for i, constraint in enumerate(current_constraints):
            row = i + 1
            self.add_simplex_constraint_row(self.simplex_constraint_entries[0]['widgets'][0].master, row)
            
            # Set values from stored data (truncate or pad as needed)
            num_vars = self.num_vars.get()
            for j in range(min(num_vars, len(constraint['coeffs']))):
                self.simplex_constraint_entries[-1]['coeffs'][j].set(constraint['coeffs'][j])
            
            # Set sense and rhs
            self.simplex_constraint_entries[-1]['sense'].set(constraint['sense'])
            self.simplex_constraint_entries[-1]['rhs'].set(constraint['rhs'])

    def add_simplex_constraint_row(self, frame, row):

        num_vars = self.num_vars.get()
        coeff_vars = []
        widgets = [] 
        sense = tk.StringVar(value="<=")
        rhs = tk.DoubleVar(value=1)
        
        
        for i in range(num_vars):
            var = tk.DoubleVar(value=1)
            entry = ttk.Entry(frame, textvariable=var, width=5)
            entry.grid(row=row, column=i*2, padx=5, pady=5)
            coeff_vars.append(var)
            widgets.append(entry)
            
            if i < num_vars - 1:
                lbl = ttk.Label(frame, text="+")
                lbl.grid(row=row, column=i*2+1, padx=2)
                widgets.append(lbl)
        
        col = num_vars * 2
        sense_label = ttk.Label(frame, text="<=", width=3)
        sense_label.grid(row=row, column=col, padx=5, pady=5)
        rhs_entry = ttk.Entry(frame, textvariable=rhs, width=5)
        rhs_entry.grid(row=row, column=col+1, padx=5, pady=5)

        widgets.extend([sense_label, rhs_entry])

        self.simplex_constraint_entries.append({
            'coeffs': coeff_vars,
            'sense': sense,  
            'rhs': rhs,
            'widgets': widgets   # save widgets for removal
        })
        
    def remove_simplex_constraint_row(self):
 
        if len(self.simplex_constraint_entries) > 1:  
            # Get the last constraint entry
            last_entry = self.simplex_constraint_entries[-1]
            
            # Destroy all widgets in the row
            for widget in last_entry['widgets']:
                widget.destroy()
                
            # Remove from our tracking list
            self.simplex_constraint_entries.pop()
    
    def solve_simplex(self):
  
        try:
            # Get objective coefficients
            c = [var.get() for var in self.objective_entries]
            
            # Get constraints
            A = []
            b = []
            for entry in self.simplex_constraint_entries:
                A.append([var.get() for var in entry['coeffs']])
                b.append(entry['rhs'].get())
            
            # Solve
            solver = SimplexSolver()
            result = solver.solve(
                c=c,
                A=A,
                b=b,
                maximize=(self.simplex_opt_type.get() == "max")
            )
            
            # Display results
            self.simplex_results.delete(1.0, tk.END)
            self.simplex_results.insert(tk.END, "=== Simplex Solution ===\n")
            self.simplex_results.insert(tk.END, f"Status: {result.status}\n")
            
            if result.status == 'optimal':
                self.simplex_results.insert(tk.END, f"Optimal Value: {result.z:.4f}\n")
                self.simplex_results.insert(tk.END, "Solution:\n")
                for i, val in enumerate(result.x):
                    self.simplex_results.insert(tk.END, f"  x{i+1} = {val:.4f}\n")
            
            if result.message:
                self.simplex_results.insert(tk.END, f"\nMessage: {result.message}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    

if __name__ == "__main__":
    root = tk.Tk()
    app = LPSolverApp(root)
    root.mainloop()