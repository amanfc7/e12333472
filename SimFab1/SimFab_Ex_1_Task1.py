import numpy as np
import matplotlib.pyplot as plt
import sys

class SDFGrid:
    def __init__(self, n_x, n_y, spacing, boundary_condition):    # Constructor for grid dimensions, spacing and Boundary conditions (BC).
        
        self.n_x = n_x           # No. of grid points along x-axis
        self.n_y = n_y           # No. of grid points along x-axis
        self.spacing = spacing         # Grid spacing
        self.boundary_condition = boundary_condition     # BC (Reflective or Periodic)
        self.grid = np.zeros((n_x, n_y))  # initializing the grid

    def BC(self, i, j):  # function to implement boundary conditions (i, j are the indexes in the x and y directions)
       
       # x and y are mapped coordinates

        if self.boundary_condition == 'reflective':
            x = self.reflective(i, self.n_x)
            y = self.reflective(j, self.n_y)
        elif self.boundary_condition == 'periodic':
            x = self.periodic(i, self.n_x)
            y = self.periodic(j, self.n_y)
        else:
            x = i * self.spacing
            y = j * self.spacing
        return x, y    

    def distance_circle(self, centre, radius):  # method to calculate signed distance function for circle.
         
        x0, y0 = centre    # co-ordinates of the centre of circle
        for i in range(self.n_x):
            for j in range(self.n_y):
                x, y = self.BC(i, j)

            # now to calculate the distance of a point from the grid surface

                distance = np.sqrt((x - x0)**2 + (y - y0)**2) - radius
                self.grid[i, j] = distance

    def distance_rectangle(self, min_corner, max_corner):   # Method to calculate SDF for rectangle.
        
        x_min, y_min = min_corner   # Coordinates of the rectangle's minimum corner
        x_max, y_max = max_corner   #  Coordinates of the rectangle's maximum corner

        for i in range(self.n_x):
            for j in range(self.n_y):
                x, y = self.BC(i, j)
                d_x = max(x_min - x, 0, x - x_max)
                d_y = max(y_min - y, 0, y - y_max)
                distance = np.sqrt(d_x**2 + d_y**2)
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    distance = -min(x - x_min, x_max - x, y - y_min, y_max - y)
                self.grid[i, j] = distance
   
   # applying boundary conditions: 

    def reflective(self, index, max_index):  # to implement reflective boundary condition on indices
      
        # index =  index that is to be reflected
        # max_index = Maximum index in the dimension
        
        if index < 0:
            return -index * self.spacing
        elif index >= max_index:
            return (2 * max_index - index - 1) * self.spacing
        else:
            return index * self.spacing

    def periodic(self, index, max_index):  # to implement periodic boundary condition on indices
       
        if index < 0:
            return (max_index + index) * self.spacing
        elif index >= max_index:
            return (index - max_index) * self.spacing
        else:
            return index * self.spacing

    # for saving the grid to a .csv file

    def save_to_csv(self, filename): 
        np.savetxt(filename, self.grid, delimiter=',')

# Visualization of the grid 

    def visualize(self, title):
        
        x = np.linspace(0, self.n_x * self.spacing, self.n_x)
        y = np.linspace(0, self.n_y * self.spacing, self.n_y)
        X, Y = np.meshgrid(x, y)
        
        plt.figure(figsize=(8, 6))
        contour = plt.contourf(X, Y, self.grid.T, levels=50, cmap='RdYlBu')
        plt.colorbar(contour, label='Signed Distance of a point on the grid')
        plt.contour(X, Y, self.grid.T, levels=[0], colors='black')  
        plt.title(title)
        plt.xlabel('X - axis')
        plt.ylabel('Y - axis')
        plt.grid(True)
        plt.show()
        

def main():      # for running arguments, generating the grid and its visualization through command line.  
    
    args = sys.argv[1:]
    if len(args) < 8:  # As the minimum conditions for a circle is 8, and 9 for a rectangle, so if the no. of arguments is less than 8 it will print the sentence below: 
        
        print("Provide the following values: ./Grid[x-size(n_x) y-size(n_y)] [spacing] [Circle / Rectangle] [reflective / periodic] [parameters]")
        return
   
    # for size of the grid and other parameters
    n_x = int(args[0])
    n_y = int(args[1])
    spacing = float(args[2])
    shape = args[3]    # Shape - Circlr or rectangle
    boundary_condition = args[4]   # boundary_condition = 'reflective' or 'periodic' 
    
    grid = SDFGrid(n_x, n_y, spacing, boundary_condition)

    if shape == "Circle":
        # args[5] and args[6] = x and y-coordinates of the center of circle
        # args[7] = Radius of the circle
        center = (float(args[5]), float(args[6]))
        radius = float(args[7])
        if len(args) > 8:
            print("Error: Please provide exactly 8 arguments")
            return
        grid.distance_circle(center, radius)
        if args[4] == 'reflective':
            grid.visualize('Signed Distance Function - Circle (Reflective)')
        elif args[4] == 'periodic':
            grid.visualize('Signed Distance Function - Circle (Periodic)')
        grid.save_to_csv('circle_grid.csv')

    elif shape == "Rectangle":
        # args[5] and args[6] = x and y-coordinates of the minimum corner of rectangle
        # args[7] and args[8] = x and y-coordinates of the maximum corner of rectangle
        min_corner = (float(args[5]), float(args[6]))
        max_corner = (float(args[7]), float(args[8]))
        if len(args) > 9:
            print("Error: Please provide exactly 9 arguments")
            return
        grid.distance_rectangle(min_corner, max_corner)
        if args[4] == 'reflective':
            grid.visualize('Signed Distance Function - Rectangle (Reflective)')
        elif args[4] == 'periodic':
            grid.visualize('Signed Distance Function - Rectangle (Periodic)')
        grid.save_to_csv('rectangle_grid.csv')

if __name__ == '__main__':
    main()
