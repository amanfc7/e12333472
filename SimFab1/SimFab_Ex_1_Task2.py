import numpy as np
import sys
from SimFab_Ex_1_Task1 import SDFGrid as BaseGrid  # importing the functions from Task 1

# Using the SDFGrid class from the SimFab_Ex_1_Task1 file

class SDFGrid(BaseGrid):
    def __init__(self, n_x, n_y, spacing):
        # Initializing the base class without boundary_condition
        super().__init__(n_x, n_y, spacing, boundary_condition = None)

    # Calculation of numerical derivatives at the point (x, y) using central differences:
    # x: x-coordinate index in the grid
    # y: y-coordinate index in the grid
    # It returns: Derivatives (D_x, D_y)  
    def numerical_derivative(self, x, y):
        D_x = (self.grid[min(x + 1, self.n_x - 1), y] - self.grid[max(x - 1, 0), y]) / (2 * self.spacing)
        D_y = (self.grid[x, min(y + 1, self.n_y - 1)] - self.grid[x, max(y - 1, 0)]) / (2 * self.spacing)
        return D_x, D_y

    # Calculation of the normal vector at the point (x, y) using numerical derivatives:
    # It returns: Normal vector [D_x / magnitude, D_y / magnitude]
    def normal(self, x, y, p = 1e-10):
        D_x, D_y = self.numerical_derivative(x, y)
        magnitude = np.sqrt(D_x**2 + D_y**2)
        if magnitude > p:
            return D_x / (magnitude + p), D_y / (magnitude + p)
        else:
            return 0.0, 0.0     # to avoid division by zero by returning a zero vector

    # Calculation of the curvature at the point (x, y) using numerical derivatives and normal:
    # It returns: Curvature (curv)
    def curvature(self, x, y):
        n_x, n_y = self.normal(x, y)

        n_x_right, n_y_right = self.normal(min(x + 1, self.n_x - 1), y)
        n_x_left, n_y_left = self.normal(max(x - 1, 0), y)
        n_x_top, n_y_top = self.normal(x, min(y + 1, self.n_y - 1))
        n_x_bottom, n_y_bottom = self.normal(x, max(y - 1, 0))

        Dn_x = (n_x_right - n_x_left) / (2 * self.spacing)
        Dn_y = (n_y_top - n_y_bottom) / (2 * self.spacing)

        curv = Dn_x + Dn_y
        return curv

def main():     # To pass arguments using cmd and calculate normal vector and curvature
    args = sys.argv[1:]
    if len(args) < 9:   # here, the exact no. of arguments are 9 for circle and 10 for rectangle
        print("Give the following values: ./grid x-size y-size spacing [Circle | Rectangle] [parameters] x y")
        return

    n_x = int(args[0])
    n_y = int(args[1])
    spacing = float(args[2])
    shape = args[3]
    
    grid = SDFGrid(n_x, n_y, spacing)

    if shape == 'Circle':
        # args[4] and args[5]: x and y - coordinates of the center of the circle
        # args[6]: Radius of the circle
        center = (float(args[4]), float(args[5]))
        radius = float(args[6])
        x = int(args[7])
        y = int(args[8])
        if len(args) > 9:
            print("Error: Please provide exactly 9 arguments")
            return

        grid.distance_circle(center, radius)

    elif shape == 'Rectangle':
        # args[4] and args[5]: x and y - coordinates of the minimum corner of the rectangle
        # args[6] and args[7]: x and y - coordinate of the maximum corner of the rectangle
        min_corner = (float(args[4]), float(args[5]))
        max_corner = (float(args[6]), float(args[7]))
        x = int(args[8])
        y = int(args[9])
        if len(args) > 10:
            print("Error: Please provide exactly 10 arguments")
            return
        
        grid.distance_rectangle(min_corner, max_corner)

    normal = grid.normal(x, y)
    curvature = grid.curvature(x, y)

    normal_vector = (f"{normal[0]:.5f}i + {normal[1]:.5f}j")

    # the normal vector and curvature, rounded to 5 decimal places:

    print(f"Normal at ({x},{y}): {normal_vector}")
    print(f"Curvature at ({x},{y}): {curvature:.5f}")

if __name__ == "__main__":
    main()
