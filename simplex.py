import matplotlib.pyplot as plt

class SimplexSolverLists:
    def __init__(self, c, A, b):
        self.numVars = len(c)
        self.numConstr = len(b)
        
        #initial basis like example 3.5
        self.basis = [3, 4, 5] 
        self.path = []
        
        #tableau with 2d lists [m+1 rows] x [n+1 columns]
        #row 0
        self.tableau = [[0.0] + [float(val) for val in c]]
        
        #rows 1-3
        for i in range(self.numConstr):
            row = [float(b[i])] + [float(val) for val in A[i]]
            self.tableau.append(row)

    def printTableau(self, iteration, prow=None, pcol=None):
        print(f"\ntableau {iteration}")
        headers = ["                "] + [f"x{i+1}" for i in range(self.numVars)]
        print(" | ".join(f"{h:^7}" for h in headers))
        print("-" * 80)
        
        for i, row in enumerate(self.tableau):
            label = f"  x{self.basis[i-1]+1} =" if i > 0 else "      "
            printRow = []
            for j, val in enumerate(row):
                #highlight pivot elemebt with astrisk
                cell = f"*{val:6.1f}" if i == prow and j == pcol else f"{val:7.1f}"
                printRow.append(cell)
            print(f"{label:5} | " + " | ".join(printRow))

    def solve(self):
        iteration = 0 
        while True:
            #x1, x2, x3 are columns 1, 2, 3
            currSln = [0.0, 0.0, 0.0]
            for i, b in enumerate(self.basis):
                if b < 3: #track x1, x2, x3
                    currSln[b] = self.tableau[i+1][0]
            self.path.append(currSln)

            #checking row 0 for most negative value
            negCosts = self.tableau[0][1:]
            minVal = min(negCosts)
            
            if minVal >= -1e-9: #optimality
                self.printTableau(iteration)
                print("\noptimal solution")
                break
            
            #follow A to D to B to E like textbook
            if iteration == 0: 
                pcol, prow = 1, 2 #x1 enters x5 exits
            elif iteration == 1: 
                pcol, prow = 3, 1 #x3 enters x4 exits
            elif iteration == 2: 
                pcol, prow = 2, 3 #x2 enters, x6 exits
            else:
                pcol = negCosts.index(minVal) + 1

                #ratio Test
                ratios = []
                for i in range(1, 4):
                    entry = self.tableau[i][pcol]
                    ratios.append(self.tableau[i][0] / entry if entry > 1e-9 else float('inf'))
                prow = ratios.index(min(ratios)) + 1

            self.printTableau(iteration, prow, pcol)
            print(f"\n x{pcol} enters")
            print(f"\n x{self.basis[prow-1]+1} exits.")

            #pivot and do row operations
            pivot = self.tableau[prow][pcol]
            #normalize pivot row
            self.tableau[prow] = [x / pivot for x in self.tableau[prow]]
            
            #get rid of other values in the pivot column
            for i in range(len(self.tableau)):
                if i != prow:
                    factor = self.tableau[i][pcol]
                    self.tableau[i] = [self.tableau[i][j] - factor * self.tableau[prow][j] 
                                      for j in range(len(self.tableau[0]))]
            
            self.basis[prow-1] = pcol - 1
            iteration += 1

    def plotPath(self):
        #use matplotlib for visuals
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = [p[0] for p in self.path]; y = [p[1] for p in self.path]; z = [p[2] for p in self.path]
        ax.plot(x, y, z, 'ro-', linewidth=2)
        ax.set_title("A -> D -> B -> E"); plt.show()

#execution
c = [-10, -12, -12, 0, 0, 0]
A = [[1, 2, 2, 1, 0, 0], [2, 1, 2, 0, 1, 0], [2, 2, 1, 0, 0, 1]]
b = [20, 20, 20]

solver = SimplexSolverLists(c, A, b)
solver.solve()
solver.plotPath()