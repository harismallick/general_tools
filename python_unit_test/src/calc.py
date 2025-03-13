def add(x, y) -> int:
    return x + y

def subtract(x, y) -> int:
    return x - y

def multiply(x, y) -> int:
    return x * y 

def divide(x, y) -> float:
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

