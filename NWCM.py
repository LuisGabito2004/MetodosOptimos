class NWCM:
    def __init__(self, cost_matrix,supply, demand,):
        self.cost_matrix = cost_matrix
        self.demand = demand
        self.supply = supply
        self.allocation = self.northwest_corner_method(self.cost_matrix, self.supply, self.demand)
        self.result = self.calculate_total_cost(self.allocation, self.cost_matrix)
        self.printTableus(self.allocation)
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
            self.printTableus(allocation, iteration)
            # Update supply and demand
            if supply[i] < demand[j]:
                demand[j] -= supply[i]
                supply[i] = 0
                i += 1  # Move to the next source
                iteration += 1
            elif supply[i] > demand[j]:
                supply[i] -= demand[j]
                demand[j] = 0
                j += 1  # Move to the next destination
                iteration += 1
            else:  # supply[i] == demand[j]
                supply[i] = 0
                demand[j] = 0
                i += 1
                j += 1  # Move diagonally to the next source and destination
                iteration += 1
        return allocation


    def calculate_total_cost(self, allocation, cost_matrix):
        total_cost = 0
        rows = len(allocation)
        cols = len(allocation[0])
        totalCostOperation = str("")

        for i in range(rows):
            for j in range(cols):
                total_cost += allocation[i][j] * cost_matrix[i][j]
                if(allocation[i][j] != 0 and cost_matrix[i][j] !=0):
                    totalCostOperation += str(allocation[i][j]) +"*" + str(cost_matrix[i][j])
                    if( i < rows-1 or j < cols-1):
                        totalCostOperation += " + "


        return totalCostOperation + " = " + str(total_cost)
    
    
    def printTableus(self, tableu, iteration = "Final Tableu:"):
        print("iteration #" ,iteration)
        for row in tableu:
            print(row)
        print("\n")
    
    def printResults(self, result):
        print("Total transportation Cost:", result)




# Example Input
cost_matrix = [
    [12, 13, 4, 6],
    [6, 4, 10, 11],
    [10, 9, 12, 4]
]

supply = [500, 700, 800]  # Supply for each source
demand = [400, 900,200, 500]  # Demand for each destination

NWCM(cost_matrix, supply, demand)