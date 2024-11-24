class NWCM:
    def __init__(self, cost_matrix, supply, demand):
        self.cost_matrix = cost_matrix
        self.original_supply = supply[:]
        self.original_demand = demand[:]
        self.isNotBalanced = False

        # Storage for all tableau strings
        self.tableau_strings = []

        self.original_supply, self.original_demand, self.cost_matrix, self.isNotBalanced = self.handle_unbalanced_problem(self.original_supply, self.original_demand, self.cost_matrix)

        # Perform the Northwest Corner Method
        self.allocation, self.final_demand, self.final_supply = self.northwest_corner_method(
            self.cost_matrix, self.original_supply, self.original_demand
        )

        # Calculate the total cost
        self.result = self.calculate_total_cost(self.allocation, self.cost_matrix)

        # Print the final allocation matrix
        self.collect_tableau(self.allocation, self.final_supply, self.final_demand, "Tabla Final")
        self.collect_results(self.result)

    def northwest_corner_method(self, cost_matrix, supply, demand):
        iteration = 1
        rows = len(supply)
        cols = len(demand)
        allocation = [[0] * cols for _ in range(rows)]

        i, j = 0, 0  # Start at the top-left corner

        self.collect_tableau(allocation, supply[:], demand[:], 0)

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

            # Collect intermediate tableau
            if i != rows and j != cols:
                self.collect_tableau(allocation, supply[:], demand[:], iteration)
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

    def collect_tableau(self, tableau, supply, demand, iteration="Tabla Final"):
        rows = len(tableau)
        cols = len(tableau[0])

        tableau_str = []
        tableau_str.append(f"Iteracion #{iteration}")
        tableau_str.append(" " * (cols * 6 + 3) + "    Oferta")

        for i in range(rows):
            row_str = f"{i + 1:2} |"
            for j in range(cols):
                row_str += f"{tableau[i][j]:6}"
            row_str += f" {(supply[i] if i < len(supply) else 0):6}"
            tableau_str.append(row_str)

        demand_str = "Dem." + "".join(
            f"{(demand[j] if j < len(demand) else 0):6}" for j in range(cols)
        )
        tableau_str.append(demand_str)
        tableau_str.append("\n")

        # Join the tableau strings and add to the collection
        self.tableau_strings.append("\n".join(tableau_str))

    def handle_unbalanced_problem(self, supply, demand, cost_matrix):
        total_supply = sum(supply)
        total_demand = sum(demand)

        if total_supply == total_demand:
            return supply, demand, cost_matrix, False

        self.tableau_strings.append("el problema esta desbalanceado. Balanceandolo automaticamente...")
        self.tableau_strings.append("\n")

        if total_supply > total_demand:
            self.tableau_strings.append("Agregando valor de demanda de " + str((total_supply - total_demand)) + ".")
            self.tableau_strings.append("\n")
            demand.append(total_supply - total_demand)
            for row in cost_matrix:
                row.append(0)
        elif total_supply < total_demand:
            self.tableau_strings.append("Agregando valor de oferta de " + str(total_demand - total_supply)+ ".")
            self.tableau_strings.append("\n")
            supply.append(total_demand - total_supply)
            cost_matrix.append([0] * len(demand))
    
        return supply, demand, cost_matrix, True
    
    def collect_results(self, result):
        self.tableau_strings.append(f"Costo de transporte total: {result}")

    def get_result(self):
        # Return all tableaus and the result as a single string
        return "\n".join(self.tableau_strings)
