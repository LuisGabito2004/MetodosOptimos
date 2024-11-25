from typing import List, Tuple
import numpy as np

class MAV:
    def __init__(
        self,
        origin: int,
        destination: int,
        matrix: List[List[int]],
        offer: List,
        demand: List,
    ):
        self.origin = origin
        self.destination = destination
        self.matrix = [[(0, matrix[i][j]) for j in range(self.destination)] for i in range(self.origin)]
        self.offer = offer
        self.demand = demand
        self.penaltiesRow = [0] * self.origin
        self.penaltiesColumn = [0] * self.destination
        self.columnsIgnored = []
        self.rowsIgnored = []
        self.penaltiesRow, self.penaltiesColumn = self.calc_penalties()
        self.resultString = ""
        self.totalCost = 0.0

    def calc_penalties(self) -> Tuple[List[int], List[int]]:
        penaltiesRow = [0] * self.origin
        penaltiesColumn = [0] * self.destination
        
        # Calculate row penalties
        for i in range(self.origin):
            if i in self.rowsIgnored or self.offer[i] == 0:
                penaltiesRow[i] = -1
                continue
                
            # Get costs for unignored columns with remaining demand
            valid_costs = [self.matrix[i][j][1] for j in range(self.destination) 
                         if j not in self.columnsIgnored and self.demand[j] > 0]
            
            if len(valid_costs) >= 2:  # Need at least 2 values to calculate penalty
                min_cost = min(valid_costs)
                valid_costs.remove(min_cost)
                second_min = min(valid_costs)
                penaltiesRow[i] = second_min - min_cost
            else:
                penaltiesRow[i] = -1
        
        # Calculate column penalties
        for j in range(self.destination):
            if j in self.columnsIgnored or self.demand[j] == 0:
                penaltiesColumn[j] = -1
                continue
                
            # Get costs for unignored rows with remaining offer
            valid_costs = [self.matrix[i][j][1] for i in range(self.origin) 
                         if i not in self.rowsIgnored and self.offer[i] > 0]
            
            if len(valid_costs) >= 2:  # Need at least 2 values to calculate penalty
                min_cost = min(valid_costs)
                valid_costs.remove(min_cost)
                second_min = min(valid_costs)
                penaltiesColumn[j] = second_min - min_cost
            else:
                penaltiesColumn[j] = -1
                
        return penaltiesRow, penaltiesColumn

    def find_last_allocation(self):
        # Find the remaining supply and demand
        remaining_row = next((i for i in range(self.origin) if self.offer[i] > 0), None)
        remaining_col = next((j for j in range(self.destination) if self.demand[j] > 0), None)
        
        if remaining_row is not None and remaining_col is not None:
            allocation = min(self.offer[remaining_row], self.demand[remaining_col])
            self.matrix[remaining_row][remaining_col] = (
                allocation, self.matrix[remaining_row][remaining_col][1]
            )
            self.offer[remaining_row] -= allocation
            self.demand[remaining_col] -= allocation
            return True
        return False

    def calc_cost(self):
        cost = 0
        formula=""
        for row in self.matrix:
            for col in row:
                if col[0] != 0:
                    cost += col[0]*col[1]
                    formula += f"{col[0]}*{col[1]} + "

        formula = "\nCost: " + formula[:-3] + " = " + f"{cost}"
        self.resultString += formula
        self.totalCost = cost
        print(formula)


    def is_feasible(self) -> Tuple[bool, str]:
        # Check if dimensions match
        if len(self.offer) != self.origin:
            return False, f"Supply vector length ({len(self.offer)}) doesn't match number of origins ({self.origin})"
        if len(self.demand) != self.destination:
            return False, f"Demand vector length ({len(self.demand)}) doesn't match number of destinations ({self.destination})"
            
        # Check for non-negative values
        if any(s < 0 for s in self.offer):
            return False, "Supply contains negative values"
        if any(d < 0 for d in self.demand):
            return False, "Demand contains negative values"
            
        # Check if problem is balanced
        total_supply = sum(self.offer)
        total_demand = sum(self.demand)
        if total_supply != total_demand:
            return False, f"Problem is not balanced: Supply ({total_supply}) ≠ Demand ({total_demand})"
            
        # Check m+n-1 rule
        required_allocations = self.origin + self.destination - 1
        max_possible_allocations = min(
            # Maximum allocations can't exceed supply points
            sum(1 for s in self.offer if s > 0),
            # Maximum allocations can't exceed demand points
            sum(1 for d in self.demand if d > 0)
        ) * min(self.origin, self.destination)
        
        if max_possible_allocations < required_allocations:
            return False, f"Problem cannot have enough basic variables: Needs {required_allocations} but can only have {max_possible_allocations}"
            
        return True, "Problem is feasible"

    def print_tableau(self):
        # Define a consistent column width
        col_width = 10
        
        # Print the table header with consistent spacing
        header = "\nDestinations".center((self.destination * col_width) + 10)
        self.resultString += header + "\n"
        print(header)
        
        # Print column headers with fixed width
        header_row = "Origin".ljust(col_width)
        for i in range(1, self.destination + 1):
            header_row += str(i).ljust(col_width)
        header_row += "Offer".ljust(col_width) + "Pen"
        self.resultString += header_row + "\n"
        print(header_row)

        # Print the table rows with consistent spacing
        for i in range(self.origin):
            row = str(i + 1).ljust(col_width)
            for j in range(self.destination):
                cell = f"{self.matrix[i][j][0]}({self.matrix[i][j][1]})".ljust(col_width)
                row += cell
            row += str(self.offer[i]).ljust(col_width) + str(self.penaltiesRow[i])
            self.resultString += row + "\n"
            print(row)

        # Print the demand row with consistent spacing
        demand_row = "Demand".ljust(col_width)
        for d in self.demand:
            demand_row += str(d).ljust(col_width)
        self.resultString += demand_row + "\n"
        print(demand_row)

        # Print the penalties row with consistent spacing
        pen_row = "Pen".ljust(col_width)
        for p in self.penaltiesColumn:
            pen_row += str(p).ljust(col_width)
        self.resultString += pen_row + "\n"
        print(pen_row)
        print()  # Add blank line for readability

    def solve_vogel(self):
        iteration = 0
        # Continue allocation until all supply and demand are satisfied
        while sum(self.offer) > 0 and sum(self.demand) > 0:
            iteration += 1
            # Find maximum penalty among active rows and columns
            active_row_penalties = [p for i, p in enumerate(self.penaltiesRow) 
                                  if i not in self.rowsIgnored and p != -1]
            active_col_penalties = [p for i, p in enumerate(self.penaltiesColumn) 
                                  if i not in self.columnsIgnored and p != -1]
            
            if not active_row_penalties and not active_col_penalties:
                # Try to make one final allocation if needed
                if sum(self.offer) > 0 and sum(self.demand) > 0:
                    if self.find_last_allocation():
                        self.penaltiesRow = [-1] * self.origin
                        self.penaltiesColumn = [-1] * self.destination
                        self.resultString += f"Iteration {iteration}" + "\n"
                        print(f"Iteration {iteration}")
                        self.print_tableau()
                        self.resultString += "\n"
                        print("\n")
                break

            max_row_penalty = max(active_row_penalties) if active_row_penalties else -1
            max_col_penalty = max(active_col_penalties) if active_col_penalties else -1

            if max_row_penalty >= max_col_penalty and max_row_penalty != -1:
                # Handle row with highest penalty
                row_index = self.penaltiesRow.index(max_row_penalty)
                
                # Find minimum cost column with remaining demand
                valid_cols = [(j, self.matrix[row_index][j][1]) 
                            for j in range(self.destination) 
                            if j not in self.columnsIgnored and self.demand[j] > 0]
                if not valid_cols:
                    self.rowsIgnored.append(row_index)
                    continue
                    
                min_cost_col = min(valid_cols, key=lambda x: x[1])[0]
                
                # Allocate
                allocation = min(self.offer[row_index], self.demand[min_cost_col])
                self.matrix[row_index][min_cost_col] = (
                    allocation, self.matrix[row_index][min_cost_col][1]
                )
                self.offer[row_index] -= allocation
                self.demand[min_cost_col] -= allocation
                
                if self.offer[row_index] == 0:
                    self.rowsIgnored.append(row_index)
                if self.demand[min_cost_col] == 0:
                    self.columnsIgnored.append(min_cost_col)
            elif max_col_penalty != -1:
                # Handle column with highest penalty
                col_index = self.penaltiesColumn.index(max_col_penalty)
                
                # Find minimum cost row with remaining offer
                valid_rows = [(i, self.matrix[i][col_index][1]) 
                            for i in range(self.origin) 
                            if i not in self.rowsIgnored and self.offer[i] > 0]
                if not valid_rows:
                    self.columnsIgnored.append(col_index)
                    continue
                    
                min_cost_row = min(valid_rows, key=lambda x: x[1])[0]
                
                # Allocate
                allocation = min(self.offer[min_cost_row], self.demand[col_index])
                self.matrix[min_cost_row][col_index] = (
                    allocation, self.matrix[min_cost_row][col_index][1]
                )
                self.offer[min_cost_row] -= allocation
                self.demand[col_index] -= allocation
                
                if self.offer[min_cost_row] == 0:
                    self.rowsIgnored.append(min_cost_row)
                if self.demand[col_index] == 0:
                    self.columnsIgnored.append(col_index)

            self.penaltiesRow, self.penaltiesColumn = self.calc_penalties()
            
            self.resultString += f"Iteration {iteration}" + "\n"
            print(f"Iteration {iteration}")
            self.print_tableau()
            self.resultString += "\n"
            print("\n")

        return self.matrix
    
    def solve(self) -> Tuple[bool, List[List[Tuple[int, int]]] | str]:
        # Check feasibility first
        is_feasible, message = self.is_feasible()
        if not is_feasible:
            return False, message
            
        # If feasible, solve using Vogel's approximation method
        try:
            solution = self.solve_vogel()
            # Verify the solution has the correct number of non-zero allocations
            non_zero_allocations = sum(
                1 for i in range(self.origin) 
                for j in range(self.destination) 
                if solution[i][j][0] > 0
            )
            required_allocations = self.origin + self.destination - 1
            
            if non_zero_allocations < required_allocations:
                return False, f"Solution is degenerate: Has {non_zero_allocations} allocations but needs {required_allocations}"
                
            return True, solution
        except Exception as e:
            return False, f"Error solving problem: {str(e)}"

    def get_matrix_parsed(self) -> Tuple[List[List[int]], List[List[int]], int]:
        allocations = []
        costs = []
        for row in self.matrix:
            rowAllocations = []
            rowCosts = []
            for allocation, cost in row:
                rowAllocations.append(allocation)
                rowCosts.append(cost)
            allocations.append(rowAllocations)
            costs.append(rowCosts)

        num_allocations = sum(element != 0 for row in allocations for element in row)

        return allocations, costs, num_allocations

if __name__ == '__main__':
    # EXAMPLE GETTED FROM CLASSROOM
    # matrix = [
    #     [12, 13, 4, 6],
    #     [6, 4, 10, 11],
    #     [10, 9, 12, 4]
    # ]
    # row = matrix.__len__()
    # column = matrix[0].__len__()
    # offer = [500, 700, 800]
    # demand = [400, 900, 200, 500]

    # EXAMPLE GETTED FROM HOMEWORK
    matrix = [
        [3, 2, 7, 6],
        [7, 5, 2, 3],
        [2, 5, 4, 5]
    ]
    row = matrix.__len__()
    column = matrix[0].__len__()
    offer = [5000, 6000, 2500]
    demand = [6000, 4000, 2000, 1500]

    obj = MAV(row, column, matrix, offer, demand)
    obj.resultString = "Initial Tableu"
    print("Initial Tableu")
    obj.print_tableau()
    obj.resultString += "\n"
    print()
    
    is_feasible, message = obj.is_feasible()
    obj.resultString += f"Feasibility check: {message}" + "\n"
    print(f"Feasibility check: {message}")
    obj.resultString += "\n"
    print("\n")
    if is_feasible:
        success, result = obj.solve()
        if success:
            obj.resultString += "Solution found!" + "\n"
            print("Solution found!")
            obj.print_tableau()
            obj.calc_cost()
        else:
            obj.resultString += f"Failed to solve: {result}" + "\n"
            print(f"Failed to solve: {result}")

    print(obj.get_matrix_parsed())

