import numpy as np

class SimplexResult:
    def __init__(self, status, x=None, z=None, message=""):
        self.status = status          # "optimal", "unbounded", "infeasible", "error"
        self.x = x                    # primal solution (original variable space)
        self.z = z                    # objective value 
        self.message = message

    def __repr__(self):
        return f"SimplexResult(status={self.status!r}, x={self.x}, z={self.z}, message={self.message!r})"

class SimplexSolver:

    def __init__(self, tol=1e-9, max_iter=10_000):
        self.tol = tol
        self.max_iter = max_iter

    def _pivot(self, T, row, col):
        pivot = T[row, col] #pivot element
        T[row, :] /= pivot  #Normalize the pivot row
        m, n = T.shape
        for r in range(m): #Gaussian elemination to update the table
            if r != row:
                T[r, :] -= T[r, col] * T[row, :]

    def _choose_entering(self, row):

        candidates = np.where(row < -self.tol)[0]
        if candidates.size == 0:
            return None
        return candidates[np.argmin(row[candidates])]

    def _choose_leaving(self, T, col):
        rhs = T[:-1, -1]
        col_vals = T[:-1, col]
        mask = col_vals > self.tol

        if not np.any(mask):
            return None  # Unbounded
        ratios = rhs[mask] / col_vals[mask]
        idx = np.argmin(ratios)

        leaving_rows = np.where(mask)[0]
        return leaving_rows[idx]

    def _build_tableau(self, A, b, c):

        m, n = A.shape     
        # Add slack variables
        slack_matrix = np.eye(m)
        full_A = np.hstack([A, slack_matrix])     
        # Initial basis consists of slack variables
        basis = list(range(n, n + m))     
        # Objective row (maximization)
        c_full = np.zeros(n + m)
        c_full[:n] = -c  
        c_full[n:] = 0       
        # Build tableau
        T = np.zeros((m + 1, n + m + 1))
        T[:-1, :n + m] = full_A
        T[:-1, -1] = b
        T[-1, :n + m] = c_full
        
        return T, basis

    def _optimize_tableau(self, T, basis):

        iters = 0
        while iters < self.max_iter:
            iters += 1
            obj_row = T[-1, :-1]
            col = self._choose_entering(obj_row)
            if col is None:
                return "optimal", basis  

            row = self._choose_leaving(T, col)
            if row is None:
                return "unbounded", basis

            self._pivot(T, row, col)
            basis[row] = col

        return "iteration_limit", basis

    def solve(self, c, A, b, maximize=True):

        c = np.array(c, dtype=float).flatten()
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float).flatten()

        if A.shape[0] != b.shape[0]:
            return SimplexResult("error", message="Number of constraints in A and b don't match.")
        if A.shape[1] != c.shape[0]:
            return SimplexResult("error", message="Objective length must equal number of variables.")

        # Convert minimization to maximization
        c_eff = c.copy()
        if not maximize:
            c_eff = -c_eff

        # Ensure b >= 0 
        for i in range(len(b)):
            if b[i] < 0:
                return SimplexResult("error", message="All b values must be non-negative for <= constraints.")

        # Build and solve tableau
        T, basis = self._build_tableau(A, b, c_eff)
        status, basis = self._optimize_tableau(T, basis)

        if status == "unbounded":
            return SimplexResult("unbounded", message="Objective is unbounded.")
        if status != "optimal":
            return SimplexResult("error", message=f"Simplex did not converge: {status}")

        # Extract solution
        m, n = A.shape[0], A.shape[1]
        x = np.zeros(n)
        
        # Find values of basic variables
        for i in range(m):
            bj = basis[i]
            if bj < n:  
                x[bj] = T[i, -1]

        z = T[-1, -1]
        if not maximize:
            z = -z

        return SimplexResult("optimal", x=x, z=z)