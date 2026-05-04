import numpy as np
import matplotlib.pyplot as plt

class SimplexSolver:
    def __init__(self, c, A, b):
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.num_vars = len(c)
        self.num_constraints = len(b)
        
        # Initial basis: x4, x5, x6 as per Example 3.5
        self.basis = [3, 4, 5] 
        self.path = []
        
        # Construct Tableau
        # Row 0: [Value | Reduced Costs]
        # Rows 1-3: [RHS | Constraints]
        self.tableau = np.zeros((self.num_constraints + 1, self.num_vars + 1))
        self.tableau[0, 1:] = self.c
        self.tableau[1:, 0] = self.b
        self.tableau[1:, 1:] = self.A

    def print_tableau(self, iteration, p_row=None, p_col=None):
        print(f"\n--- TABLEAU {iteration} ---")
        header = "      | " + " | ".join([f"x{i+1}".center(7) for i in range(self.num_vars)])
        print(header)
        print("-" * len(header))
        
        for i in range(self.tableau.shape[0]):
            label = f"x{self.basis[i-1]+1} =" if i > 0 else "      "
            row_str = f"{label:5} | "
            for j in range(self.tableau.shape[1]):
                val = self.tableau[i, j]
                # Highlight pivot element as seen in image_62c342.png
                cell = f"*{val:6.1f}" if i == p_row and j == p_col else f"{val:7.1f}"
                row_str += cell + " | "
            print(row_str)

    def solve(self):
        iteration = 0
        while True:
            # Track current BFS coordinates (x1, x2, x3) for plotting
            current_x = np.zeros(self.num_vars)
            for i, b_idx in enumerate(self.basis):
                current_x[b_idx] = self.tableau[i+1, 0]
            self.path.append(current_x[:3].copy())

            # Check reduced costs for optimality
            red_costs = self.tableau[0, 1:]
            if np.all(red_costs >= -1e-9):
                self.print_tableau(iteration)
                print("\nOptimal solution found.")
                break
            
            # Pivot Selection to match path A-D-B-E
            if iteration == 0: 
                p_col, p_row = 1, 2  # x1 enters, x5 exits
            elif iteration == 1:
                p_col, p_row = 3, 1  # x3 enters, x4 exits
            elif iteration == 2:
                p_col, p_row = 2, 3  # x2 enters, x6 exits
            else:
                p_col = np.where(red_costs < -1e-9)[0][0] + 1
                p_row = np.argmin([self.tableau[i,0]/self.tableau[i,p_col] 
                                  if self.tableau[i,p_col] > 0 else np.inf 
                                  for i in range(1, 4)]) + 1

            self.print_tableau(iteration, p_row, p_col)
            
            # Print Variable Changes
            entering = f"x{p_col}"
            exiting = f"x{self.basis[p_row-1]+1}"
            print(f"\n>>> Variable Entering: {entering}")
            print(f">>> Variable Exiting:  {exiting}")
            
            # Pivot Operation
            self.tableau[p_row, :] /= self.tableau[p_row, p_col]
            for i in range(self.tableau.shape[0]):
                if i != p_row:
                    self.tableau[i, :] -= self.tableau[i, p_col] * self.tableau[p_row, :]
            
            self.basis[p_row-1] = p_col - 1
            iteration += 1

    def plot_path(self):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        pts = np.array(self.path)
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], 'ro-', linewidth=2, label='Simplex Path')
        
        # Vertex Labels matching Example 3.5
        labels = ['A', 'D', 'B', 'E']
        for i, txt in enumerate(labels):
            if i < len(pts):
                ax.text(pts[i,0], pts[i,1], pts[i,2], f'  {txt}', size=12, weight='bold')

        ax.set_xlabel('x1'); ax.set_ylabel('x2'); ax.set_zlabel('x3')
        ax.set_title('Path A -> D -> B -> E')
        plt.legend()
        plt.show()

# Run the Problem
c = [-10, -12, -12, 0, 0, 0]
A = [[1, 2, 2, 1, 0, 0], [2, 1, 2, 0, 1, 0], [2, 2, 1, 0, 0, 1]]
b = [20, 20, 20]

solver = SimplexSolver(c, A, b)
solver.solve()
solver.plot_path()