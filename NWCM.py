class NWCM:
    def __init__(self, cost_matrix,supply, demand,):
        self.cost_matrix = cost_matrix
        self.demand = demand
        self.supply = supply
        self.allocation = self.northwest_corner_method(self.cost_matrix, self.supply, self.demand)
        self.result = self.calculate_total_cost(self.allocation, self.cost_matrix)
        self.printTableusNresults(self.allocation, self.result)


    def northwest_corner_method(self, cost_matrix, supply, demand):
        rows = len(supply)
        cols = len(demand)
        allocation = [[0] * cols for _ in range(rows)]
        tempallocaion = []
        
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
        return allocation


    def calculate_total_cost(self, allocation, cost_matrix):
        total_cost = 0
        rows = len(allocation)
        cols = len(allocation[0])
        
        for i in range(rows):
            for j in range(cols):
                total_cost += allocation[i][j] * cost_matrix[i][j]
        
        return total_cost
    
    
    def printTableusNresults(self, tableu, result):
        for row in tableu:
            print(row)

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
