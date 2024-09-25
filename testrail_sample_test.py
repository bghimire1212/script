import os

a = 10
b = 5

def addition(a, b):
    print("This is the addition function")
    return a + b

def subtraction(a, b):
    print("This is the subtraction function")
    return a - b

def multiplication(a, b):
    print("This is the multiplication function")
    return a * b

def division(a, b):
    print("This is the division function")
    if b != 0:
        return a / b
    else:
        return "Division by zero is undefined"

def main():
    print(f"Addition result: {addition(a, b)}")
    print(f"Subtraction result: {subtraction(a, b)}")
    print(f"Multiplication result: {multiplication(a, b)}")
    print(f"Division result: {division(a, b)}")

if __name__ == "__main__":
    main()
