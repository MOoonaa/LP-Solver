import numpy as np
import matplotlib.pyplot as plt

def format_constraint(a, b, c, sense):
    """Formats constraint equation as a string"""
    parts = []
    if a != 0:
        parts.append(f"{a:.2f}x" if abs(a) != 1 else ("x" if a > 0 else "-x"))
    if b != 0:
        sign = "+" if (b > 0 and parts) else ("-" if b < 0 else "")
        coeff = abs(b) if abs(b) != 1 else ""
        parts.append(f" {sign} {coeff}y" if coeff else f" {sign} y")
    return f"{''.join(parts)} {sense} {c:.2f}"

def graphical_solver(opt_type, obj_coeffs, constraints):
   
    def satisfies(x, y, a, b, c, sense):
        if sense == "<=":
            return a * x + b * y <= c + 1e-9
        elif sense == ">=":
            return a * x + b * y >= c - 1e-9
        elif sense == "=":
            return np.isclose(a * x + b * y, c, atol=1e-9)
        return False

    cons_funcs = [lambda X, Y, a=a, b=b, c=c, s=sense: satisfies(X, Y, a, b, c, s) for a, b, c, sense in constraints]

    # Find intersection points
    points = []
    for i in range(len(constraints)):
        for j in range(i+1, len(constraints)):
            a1, b1, c1, _ = constraints[i]
            a2, b2, c2, _ = constraints[j]
            A = np.array([[a1, b1], [a2, b2]])
            B = np.array([c1, c2])
            if np.linalg.det(A) != 0:
                x, y = np.linalg.solve(A, B)
                if x >= -1e-9 and y >= -1e-9:
                    if all(cf(x, y) for cf in cons_funcs):
                        points.append((x, y))

    # Axis intercepts
    for a, b, c, sense in constraints:
        if a != 0:
            x = c / a
            if x >= -1e-9 and all(cf(x, 0) for cf in cons_funcs):
                points.append((x, 0))
        if b != 0:
            y = c / b
            if y >= -1e-9 and all(cf(0, y) for cf in cons_funcs):
                points.append((0, y))

    # Unique points
    unique_points = []
    for p in points:
        if not any(np.isclose(p[0], q[0]) and np.isclose(p[1], q[1]) for q in unique_points):
            unique_points.append(p)

    # Status defaults
    status = "optimal"
    opt_val = None
    opt_pts = []

    # Check Infeasiblity 
    if not unique_points:
        print ("No feasible area solution")
        status = "infeasible"

    # Check Unbounded solution 
    elif status != "infeasible":
        obj_dir = np.array(obj_coeffs, dtype=float)
        if opt_type == 'min':
            obj_dir = -obj_dir
        limiting_constraints = 0
        for (a, b, c, sense) in constraints:
            n = np.array([a, b], dtype=float)
            proj = np.dot(n, obj_dir)
            if sense == "<=" and proj > 1e-9:
                limiting_constraints += 1
            elif sense == ">=" and proj < -1e-9:
                limiting_constraints += 1
            elif sense == "=":
                limiting_constraints += 1
        if limiting_constraints == 0:
            status = "unbounded"

    # If optimal, compute optimum
    if status == "optimal":
        values = [(p, obj_coeffs[0] * p[0] + obj_coeffs[1] * p[1]) for p in unique_points]
        if opt_type == 'max':
            opt_val = max(v for _, v in values)
        else:
            opt_val = min(v for _, v in values)
        opt_pts = [p for p, v in values if np.isclose(v, opt_val)]
                # Multiple optimal solutions detection
        if len(opt_pts) > 1:
            p1, p2 = opt_pts[0], opt_pts[-1]
            print(f"Multiple optimal solutions between {p1} and {p2}")
            print(f"All optimal points: P(λ) = λ*{p1} + (1 - λ)*{p2}, 0 ≤ λ ≤ 1")

    # ==== Plotting ====
    if unique_points:
        max_x = max(p[0] for p in unique_points) + 2
        max_y = max(p[1] for p in unique_points) + 2
    else:
        max_x, max_y = 10, 10  # default range when no feasible points

    x_vals = np.linspace(0, max_x, 400)
    y_vals = np.linspace(0, max_y, 400)
    X, Y = np.meshgrid(x_vals, y_vals)

    feasible_region = np.ones_like(X, dtype=bool)
    for cf in cons_funcs:
        feasible_region &= cf(X, Y)

    plt.figure(figsize=(8, 8))
    plt.contourf(X, Y, feasible_region, levels=[0.5,1], colors=["#87CEFA"], alpha=0.3)

    # Constraint lines
    constraint_colors = plt.cm.tab10(np.linspace(0, 1, len(constraints)))  # Creates a color spectrum

    legend_handles = []

    # Plot each constraint with unique color and label
    for i, (a, b, c, sense) in enumerate(constraints):
        color = constraint_colors[i]  # Assign unique color to each constraint
        label = f"C{i+1}: {format_constraint(a, b, c, sense)}"
        
        if b != 0:  # Non-vertical line
            plt.plot(x_vals, (c - a * x_vals) / b, 
                    linestyle='--', 
                    color=color,
                    label=f"Constraint {i+1}: {a:.1f}x + {b:.1f}y {sense} {c:.1f}")
        else:  # Vertical line
            plt.axvline(c / a, 
                    linestyle='--', 
                    color=color,
                    label=f"Constraint {i+1}: {a:.1f}x {sense} {c:.1f}")
        
        # Create a custom legend entry
        legend_handles.append(plt.Line2D([], [], color=color, linestyle='--', linewidth=2,label=label))
    
    # Add objective function to legend
    obj_label = f"Obj: z = {obj_coeffs[0]:.2f}x + {obj_coeffs[1]:.2f}y ({opt_type})"
    legend_handles.append(
        plt.Line2D([], [], color='black', linestyle='-', linewidth=2,label=obj_label))
    
    # Add optimal point to legend
    opt_color = 'green' if opt_type == 'max' else 'gold'
    opt_label = f"Optimal ({opt_type})"
    legend_handles.append(plt.Line2D([], [], color=opt_color, marker='o', linestyle='None',markersize=10, label=opt_label))

    # All intersection points
    for p in unique_points:
        plt.plot(p[0], p[1], 'ro')
        plt.text(p[0] + 0.1, p[1] + 0.1, f"({p[0]:.2f},{p[1]:.2f})", fontsize=8) 

    # Optimal points
    for p in opt_pts:
        plt.plot(p[0], p[1], 'go' if opt_type == 'max' else 'gold', markersize=10) 

    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(left=0)  # Start x-axis at 0
    plt.ylim(bottom=0)  # Start y-axis at 0
    plt.title(f"LP Graphical Solution - {status.capitalize()}")
    plt.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.tight_layout()
    plt.grid(True)
    plt.show()
    
    return {'status': status, 'opt_value': opt_val, 'opt_points': opt_pts}
