def add(a, b):
    """Adds two numbers together."""
    return a + b

def subtract(a, b):
    """Subtracts b from a."""
    return a - b

def multiply(a, b):
    """Multiplies two numbers together."""
    return a * b

def divide(a, b):
    """Divides a by b. Raises an error if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
