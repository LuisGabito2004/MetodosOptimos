import sys
from typing import List, Tuple, Optional

class DIMO:
    def __init__(self, cost_matrix: List[List[float]], initial_allocation: List[List[float]], num_allocated: int):
        """
        Initialize the MODI Transportation Problem Solver
        
        Args:
            cost_matrix: Matrix of transportation costs
            initial_allocation: Initial basic feasible solution
            num_allocated: Number of allocated cells
        """
        self.cost_matrix = cost_matrix
        self.allocation_matrix = [row[:] for row in initial_allocation]
        self.num_allocated = num_allocated
        self.num_rows = len(cost_matrix)
        self.num_cols = len(cost_matrix[0])
        self.u_values: List[Optional[float]] = []  # Potencial asociado a las filas de la matriz de costos
        self.v_values: List[Optional[float]] = []  # Potencial asociado a las columnas de la matriz de costos
        self.deltas: List[List[Optional[float]]] = []  # Cálcula que indica cuánto cambiaría el costo si se moviera una unidad
        self.iteration = 0
        self.resultString = ""

    def print_tableau(self) -> None:
        """Print the current tableau showing costs, allocations, u/v values, and deltas""" 
        col_width = 12  # Increased width to accommodate larger numbers
        
        # Print column headers with v values
        header = "".ljust(col_width)
        for j in range(self.num_cols):
            v_val = f"{self.v_values[j]:.0f}" if self.v_values and self.v_values[j] is not None else "N/A"
            header += f"v={v_val}".ljust(col_width)
        self.resultString += header + "\n"
        print(header)
        
        # Print costs, allocations and u values
        for i in range(self.num_rows):
            u_val = f"{self.u_values[i]:.0f}" if self.u_values and self.u_values[i] is not None else "N/A"
            row = f"u={u_val}".ljust(col_width)
            for j in range(self.num_cols):
                cost = self.cost_matrix[i][j]
                alloc = self.allocation_matrix[i][j]
                if alloc == 0.000001:  # Special case for degeneracy handling
                    alloc_str = "ε"
                else:
                    alloc_str = f"{alloc:.0f}" if alloc > 0 else "0"
                cell = f"{alloc_str}({cost})".ljust(col_width)
                row += cell
            self.resultString += row + "\n"
            print(row)

        # Print deltas for unallocated cells
        if self.deltas:
            self.resultString += "\nDelta Values (unallocated cells only):\n"
            print("\nDelta Values (unallocated cells only):")
            
            # Header row for deltas
            delta_header = "index".ljust(col_width)
            for j in range(self.num_cols):
                delta_header += str(j).ljust(col_width)
            self.resultString += delta_header + "\n"
            print(delta_header)

            # Delta values
            for i in range(self.num_rows):
                delta_row = str(i).ljust(col_width)
                for j in range(self.num_cols):
                    if self.deltas[i][j] is not None:
                        delta_val = f"{self.deltas[i][j]}".ljust(col_width)
                    else:
                        delta_val = "0".ljust(col_width)
                    delta_row += delta_val
                self.resultString += delta_row + "\n"
                print(delta_row)
            print()

        # Print current total cost
        self.calculate_total_cost()
        
        if self.is_degenerate():
            status = "Status: Solution is degenerate"
            self.resultString += status + "\n"
            print(status)
        
        separator = "=" * 40
        self.resultString += separator + "\n"
        print(separator)

    def is_degenerate(self) -> bool:
        """Check if the current solution is degenerate"""
        return self.num_allocated != (self.num_rows + self.num_cols - 1)

    def check_independent_allocation(self) -> Tuple[bool, List[int], List[int]]:
        """
        Check if allocation positions are independent
        Returns: (is_independent, eliminated_rows, eliminated_cols)
        """
        elim_rows = [0] * self.num_rows
        elim_cols = [0] * self.num_cols
        
        while True:
            flag = 0
            # Eliminate rows
            for i in range(self.num_rows):
                if elim_rows[i] == 0:
                    allocated_cells = [
                        self.allocation_matrix[i][j] 
                        for j in range(self.num_cols) 
                        if elim_cols[j] == 0 and self.allocation_matrix[i][j] != 0 
                        and self.allocation_matrix[i][j] != -1
                    ]
                    if len(allocated_cells) < 2:
                        elim_rows[i] = 1
                        flag = 1

            # Eliminate columns
            for j in range(self.num_cols):
                if elim_cols[j] == 0:
                    allocated_cells = [
                        self.allocation_matrix[i][j] 
                        for i in range(self.num_rows) 
                        if elim_rows[i] == 0 and self.allocation_matrix[i][j] != 0 
                        and self.allocation_matrix[i][j] != -1
                    ]
                    if len(allocated_cells) < 2:
                        elim_cols[j] = 1
                        flag = 1
                    
            if flag == 0:
                is_independent = 0 not in elim_rows and 0 not in elim_cols
                return is_independent, elim_rows, elim_cols

    def calculate_uv_values(self) -> None:
        """Calculate u and v values for the current allocation"""
        self.u_values = [None] * self.num_rows
        self.v_values = [None] * self.num_cols
        
        # Find row/column with maximum allocations
        max_row = (-1, 0)  # (index, count)
        max_col = (-1, 0)  # (index, count)
        
        for i in range(self.num_rows):
            allocs = sum(1 for j in range(self.num_cols) if self.allocation_matrix[i][j] != 0)
            if allocs > max_row[1]:
                max_row = (i, allocs)

        for j in range(self.num_cols):
            allocs = sum(1 for i in range(self.num_rows) if self.allocation_matrix[i][j] != 0)
            if allocs > max_col[1]:
                max_col = (j, allocs)

        # Initialize based on maximum allocations
        if max_row[1] > max_col[1]:
            self._initialize_from_row(max_row[0])
        else:
            self._initialize_from_column(max_col[0])

        # Fill remaining values
        while None in self.u_values or None in self.v_values:
            self._fill_remaining_uv_values()

    def _initialize_from_row(self, row_idx: int) -> None:
        """Initialize u and v values starting from a specific row"""
        self.u_values[row_idx] = 0
        for j in range(self.num_cols):
            if self.allocation_matrix[row_idx][j] != 0 and self.v_values[j] is None:
                self.v_values[j] = self.cost_matrix[row_idx][j] - self.u_values[row_idx]

    def _initialize_from_column(self, col_idx: int) -> None:
        """Initialize u and v values starting from a specific column"""
        self.v_values[col_idx] = 0
        for i in range(self.num_rows):
            if self.allocation_matrix[i][col_idx] != 0 and self.u_values[i] is None:
                self.u_values[i] = self.cost_matrix[i][col_idx] - self.v_values[col_idx]

    def _fill_remaining_uv_values(self) -> None:
        """Fill remaining u and v values using known values"""
        if None in self.u_values:
            i = self.u_values.index(None)
            for j in range(self.num_cols):
                if self.allocation_matrix[i][j] != 0 and self.v_values[j] is not None:
                    self.u_values[i] = self.cost_matrix[i][j] - self.v_values[j]
                    break
                    
        if None in self.v_values:
            j = self.v_values.index(None)
            for i in range(self.num_rows):
                if self.allocation_matrix[i][j] != 0 and self.u_values[i] is not None:
                    self.v_values[j] = self.cost_matrix[i][j] - self.u_values[i]
                    break

    def calculate_deltas(self) -> None:
        """Calculate delta values for unallocated cells"""
        self.deltas = [[None] * self.num_cols for _ in range(self.num_rows)]
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.allocation_matrix[i][j] == 0:
                    self.deltas[i][j] = self.cost_matrix[i][j] - self.u_values[i] - self.v_values[j]

    def is_optimal(self) -> bool:
        """Check if current solution is optimal"""
        return all(delta is None or delta >= 0 
                  for row in self.deltas 
                  for delta in row)

    def update_allocation(self) -> None:
        """Create new allocation based on negative deltas"""
        # Find most negative delta
        min_delta = float('inf')
        min_pos = (-1, -1)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.deltas[i][j] is not None and self.deltas[i][j] < min_delta:
                    min_delta = self.deltas[i][j]
                    min_pos = (i, j)

        # Find loop
        i, j = min_pos
        temp_alloc = self.allocation_matrix[i][j]
        self.allocation_matrix[i][j] = sys.maxsize
        _, elim_rows, elim_cols = self.check_independent_allocation()
        self.allocation_matrix[i][j] = temp_alloc  # Restore original value
        
        row_indices = [i for i, val in enumerate(elim_rows) if val == 0]
        col_indices = [j for j, val in enumerate(elim_cols) if val == 0]
        
        # Start building the path
        path = [min_pos]
        current_pos = min_pos
        is_horizontal = True
        
        while len(path) < 4:  # We need exactly 4 points to form a closed loop
            if is_horizontal:
                # Look for vertical connection
                for i in row_indices:
                    if i != current_pos[0] and self.allocation_matrix[i][current_pos[1]] > 0:
                        path.append((i, current_pos[1]))
                        current_pos = (i, current_pos[1])
                        break
            else:
                # Look for horizontal connection
                for j in col_indices:
                    if j != current_pos[1] and self.allocation_matrix[current_pos[0]][j] > 0:
                        path.append((current_pos[0], j))
                        current_pos = (current_pos[0], j)
                        break
            is_horizontal = not is_horizontal

        # Update allocations along the path
        min_value = float('inf')
        for idx, (x, y) in enumerate(path[1::2]):  # Check only negative positions
            if self.allocation_matrix[x][y] != 0.000001:
                min_value = min(min_value, self.allocation_matrix[x][y])
        
        for idx, (i, j) in enumerate(path):
            if idx % 2 == 0:  # Add to even positions (including 0)
                self.allocation_matrix[i][j] += min_value
            else:  # Subtract from odd positions
                self.allocation_matrix[i][j] -= min_value

        # Clean up any tiny residuals
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if abs(self.allocation_matrix[i][j]) < 1e-10:
                    self.allocation_matrix[i][j] = 0

        # Update number of allocations
        self.num_allocated = sum(1 for i in range(self.num_rows) 
                               for j in range(self.num_cols) 
                               if self.allocation_matrix[i][j] > 0)

    def remove_degeneracy(self) -> None:
        """Remove degeneracy by adding small values"""
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.allocation_matrix[i][j] == 0:
                    self.allocation_matrix[i][j] = 0.000001
                    is_independent = self.check_independent_allocation()[0]
                    if is_independent:
                        self.num_allocated += 1
                        return
                    self.allocation_matrix[i][j] = 0

    def calculate_total_cost(self) -> float:
        """Calculate total cost for current allocation"""
        cost = 0
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cost += self.cost_matrix[i][j] * self.allocation_matrix[i][j]
        return cost
    
    def print_total_cost(self):
        cost = 0
        formula=""
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.allocation_matrix[i][j] != 0:
                    cost += self.cost_matrix[i][j] * self.allocation_matrix[i][j]
                    formula += f"{self.cost_matrix[i][j]}*{self.allocation_matrix[i][j]} + "
        formula = "\nCost: " + formula[:-3] + " = " + f"{cost}"

        self.resultString += formula
        print(formula)

    def solve(self) -> Tuple[Optional[List[List[float]]], Optional[float]]:
        """
        Solve the transportation problem using MODI method
        Returns: (optimal_allocation, optimal_cost) or (None, None) if no solution exists
        """
        max_iterations = 100
        self.iteration = 0
        
        
        self.resultString += f"Iteration {self.iteration+1}" + "\n"
        print(f"Iteration {self.iteration+1}")
        # Print initial tableau
        self.print_tableau()
        
        while self.iteration < max_iterations:
            self.iteration += 1
            
            # Handle degeneracy
            if self.is_degenerate():
                self.remove_degeneracy()
                self.print_tableau()
                continue

            # Check independence
            if not self.check_independent_allocation()[0]:
                self.resultString += "\nNo solution exists - allocations are not independent" + "\n"
                print("\nNo solution exists - allocations are not independent")
                return None, None

            # Calculate u and v values
            self.calculate_uv_values()
            
            # Calculate deltas
            self.calculate_deltas()
            
            # Print current tableau
            self.print_tableau()
            
            # Check if optimal
            if self.is_optimal():
                self.resultString += "\nOptimal solution found!" + "\n"
                print("\nOptimal solution found!")
                return self.allocation_matrix, self.calculate_total_cost()
            
            # Update allocation
            self.update_allocation()

        self.resultString += "\nMax iterations reached without finding optimal solution" + "\n"
        print("\nMax iterations reached without finding optimal solution")
        return None, None

    # [Rest of the class methods remain unchanged]

if __name__ == "__main__":
    # Example usage with the same test case
    cost_matrix = [
        [12, 13, 4, 6],
        [6, 4, 10, 11],
        [10, 9, 12, 4]
    ]
    
    initial_allocation = [
        [400, 0, 100, 0],
        [0, 700, 0, 0],
        [0, 200, 100, 500]
    ]
    
    num_allocated = 6
    
    dimo = DIMO(cost_matrix, initial_allocation, num_allocated)

    dimo.resultString = "Initial Tableau" + "\n"
    print("Initial Tableau")
    dimo.print_tableau()
    dimo.resultString += ("=" * 40) + "\n"
    print("=" * 40)
    optimal_allocation, optimal_cost = dimo.solve()
    
    if optimal_allocation is not None:
        dimo.resultString += "\nFinal Optimal Allocation:" + "\n"
        print("\nFinal Optimal Allocation:")
        dimo.print_tableau()
        dimo.print_total_cost()
    else:
        dimo.resultString += "No solution exists" + "\n"
        print("No solution exists")

