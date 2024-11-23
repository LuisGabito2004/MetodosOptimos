import numpy as np

class NWCM:
    def __init__(self, cost_matrix, supply, demand):
        self.cost_matrix = cost_matrix
        self.original_supply = supply[:]
        self.original_demand = demand[:]

        # Perform the Northwest Corner Method
        self.allocation, self.final_demand, self.final_supply = self.northwest_corner_method(
            cost_matrix, supply[:], demand[:]
        )

        # Calculate the total cost
        self.result = self.calculate_total_cost(self.allocation, self.cost_matrix)

        # Print the final allocation matrix
        self.printTableus(self.allocation, self.final_supply, self.final_demand, "Final Tableu")
        self.printResults(self.result)

    def northwest_corner_method(self, cost_matrix, supply, demand):
        iteration = 0
        rows = len(supply)
        cols = len(demand)
        allocation = [[0] * cols for _ in range(rows)]

        i, j = 0, 0  # Start at the top-left corner

        while i < rows and j < cols:
            # Allocate the minimum of supply and demand
            allocation[i][j] = min(supply[i], demand[j])
            
            # Update supply and demand
            if supply[i] < demand[j]:
                demand[j] -= supply[i]
                supply[i] = 0
                i += 1  # Move to the next source
            elif supply[i] > demand[j]:
                supply[i] -= demand[j]
                demand[j] = 0
                j += 1  # Move to the next destination
            else:  # supply[i] == demand[j]
                supply[i] = 0
                demand[j] = 0
                i += 1
                j += 1  # Move diagonally to the next source and destination

            # Print intermediate tableau
            if(i != rows and j != cols):
                self.printTableus(allocation, supply, demand, iteration)
                iteration += 1

        return allocation, demand, supply

    def calculate_total_cost(self, allocation, cost_matrix):
        total_cost = 0
        rows = len(allocation)
        cols = len(allocation[0])
        total_cost_operation = str("")

        for i in range(rows):
            for j in range(cols):
                total_cost += allocation[i][j] * cost_matrix[i][j]
                if allocation[i][j] != 0 and cost_matrix[i][j] != 0:
                    total_cost_operation += str(allocation[i][j]) + "*" + str(cost_matrix[i][j])
                    if i < rows - 1 or j < cols - 1:
                        total_cost_operation += " + "

        return total_cost_operation + " = " + str(total_cost)

    def printTableus(self, tableau, supply, demand, iteration="Final Tableau"):
        print(f"Iteration #{iteration}")
        rows = len(tableau)
        cols = len(tableau[0])

        # Print the column headers with "Supply" at the end
        print(" " * (cols * 6 + 3) + "    Supply")

        # Print each row with supply at the end
        for i in range(rows):
            print(f"{i + 1:2} |", end="")  # Row label with alignment
            for j in range(cols):
                print(f"{tableau[i][j]:6}", end="")  # Align matrix values
            print(f" {(supply[i] if i < len(supply) else 0):6}")  # Current supply value

        # Print the demand row at the bottom
        print("Demand", end=" ")
        for j in range(cols):  # Match tableau's column count
            print(f"{(demand[j] if j < len(demand) else 0):6}", end="")  # Align demand values
        print("\n")


    def printResults(self, result):
        print("Total Transportation Cost:", result)


# Example Input
cost_matrix = [
    [12, 13, 4, 6],
    [6, 4, 10, 11],
    [10, 9, 12, 4]
]

supply = [500, 700, 800]  # Supply for each source
demand = [400, 900, 200, 500]  # Demand for each destination

NWCM(cost_matrix, supply, demand)
