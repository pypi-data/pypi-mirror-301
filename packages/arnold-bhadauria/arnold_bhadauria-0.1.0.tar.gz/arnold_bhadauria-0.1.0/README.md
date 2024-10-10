# Arnold Package

This Python project provides classes to represent and calculate properties for various geometric shapes: Square, Rectangle, Circle, and Triangle. Each class supports methods to calculate the area and perimeter.

## Classes

### Square

- **Constructor**: `Square(length: float)`
    - **Parameters**:
        - `length`: Length of the square's side (positive integer or float).
  
- **Methods**:
    - `area()`: Returns the area of the square.
    - `perimeter()`: Returns the perimeter of the square.

### Rectangle

- **Constructor**: `Rectangle(width: float, height: float)`
    - **Parameters**:
        - `width`: Width of the rectangle (positive integer or float).
        - `height`: Height of the rectangle (positive integer or float).

- **Methods**:
    - `area()`: Returns the area of the rectangle.
    - `perimeter()`: Returns the perimeter of the rectangle.

### Circle

- **Constructor**: `Circle(radius: float)`
    - **Parameters**:
        - `radius`: Radius of the circle (positive integer or float).

- **Methods**:
    - `area()`: Returns the area of the circle.
    - `perimeter()`: Returns the circumference of the circle.

### Triangle

- **Constructor**: `Triangle(base: float = None, height: float = None, side1: float = None, side2: float = None, side3: float = None)`
    - **Parameters**:
        - `base`: Base of the triangle (positive integer or float).
        - `height`: Height of the triangle (positive integer or float).
        - `side1`: Length of the first side (positive integer or float).
        - `side2`: Length of the second side (positive integer or float).
        - `side3`: Length of the third side (positive integer or float).

- **Methods**:
    - `area()`: Returns the area of the triangle (uses either base and height or all three sides).
    - `perimeter()`: Returns the perimeter of the triangle.

## Usage Example

Here’s a simple example of how to use the classes:

```python
from arnold import Square, Rectangle, Circle, Triangle

# Create a Square object
square = Square(4)
print(f"Square Area: {square.area()}")
print(f"Square Perimeter: {square.perimeter()}")

# Create a Rectangle object
rectangle = Rectangle(3, 5)
print(f"Rectangle Area: {rectangle.area()}")
print(f"Rectangle Perimeter: {rectangle.perimeter()}")

# Create a Circle object
circle = Circle(2)
print(f"Circle Area: {circle.area()}")
print(f"Circle Perimeter: {circle.perimeter()}")

# Create a Triangle object
triangle = Triangle(base=3, height=4, side1=3, side2=4, side3=5)
print(f"Triangle Area: {triangle.area()}")
print(f"Triangle Perimeter: {triangle.perimeter()}")
