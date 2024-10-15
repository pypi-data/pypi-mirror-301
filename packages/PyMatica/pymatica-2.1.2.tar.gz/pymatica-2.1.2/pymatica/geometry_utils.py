class MathConstants:
    PI = 3.141592653589793
    E = 2.718281828459045

class GeometryUtilities:
    @staticmethod
    def area_circle(radius):
        """Calculate the area of a circle given its radius."""
        return MathConstants.PI * radius ** 2

    @staticmethod
    def perimeter_circle(radius):
        """Calculate the perimeter (circumference) of a circle given its radius."""
        return 2 * MathConstants.PI * radius

    @staticmethod
    def area_rectangle(length, width):
        """Calculate the area of a rectangle given its length and width."""
        return length * width

    @staticmethod
    def perimeter_rectangle(length, width):
        """Calculate the perimeter of a rectangle given its length and width."""
        return 2 * (length + width)

    @staticmethod
    def area_triangle(base, height):
        """Calculate the area of a triangle given its base and height."""
        return 0.5 * base * height

    @staticmethod
    def perimeter_triangle(a, b, c):
        """Calculate the perimeter of a triangle given its three sides."""
        return a + b + c

    @staticmethod
    def area_square(side):
        """Calculate the area of a square given its side length."""
        return side ** 2

    @staticmethod
    def perimeter_square(side):
        """Calculate the perimeter of a square given its side length."""
        return 4 * side

    @staticmethod
    def distance(x1, y1, x2, y2):
        """Calculate the distance between two points in 2D space."""
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    @staticmethod
    def distance_3d(x1, y1, z1, x2, y2, z2):
        """Calculate the distance between two points in 3D space."""
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5

    @staticmethod
    def volume_cylinder(radius, height):
        """Calculate the volume of a cylinder given its radius and height."""
        return MathConstants.PI * radius ** 2 * height

    @staticmethod
    def volume_sphere(radius):
        """Calculate the volume of a sphere given its radius."""
        return (4 / 3) * MathConstants.PI * radius ** 3

    @staticmethod
    def volume_cone(radius, height):
        """Calculate the volume of a cone given its radius and height."""
        return (1 / 3) * MathConstants.PI * radius ** 2 * height

   

# Example Usage:
# print(GeometryUtilities.area_circle(5))        # Output: 78.53981633974483
# print(GeometryUtilities.perimeter_rectangle(4, 6))  # Output: 20
# print(GeometryUtilities.volume_cylinder(3, 5))   # Output: 28.274333882308138
# print(GeometryUtilities.distance_3d(1, 2, 3, 4, 5, 6))  # Output: 5.196152422706632
