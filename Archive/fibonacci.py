#Attempting to determine if a number is a Fibonacci number.
#Fibonacci numbers are the sum of the two previous values in the sequence

#Generator of Fibonacci numbers
def sequence():
    """
    Steps through Fibonacci sequences, and yields one value at a time
    Agrs: none
    Return: yields a: int
    """
    a = 0
    b = 1
    while True:
        yield a
        c = a + b
        a = b
        b = c
#Prompt user for input
def user_input():
    """
    Ask user for number, conver to Int, and return the value
    Args: none
    Return target: int
    """
    target = int(input("Enter a number: "))
    return target

#Invokes generator, and looks for Target
def fibonacci():
    """
    Takes user input as target, invokes generator, checks for boolan, prints result
    Args: none
    Returns: prints boolean result
    """
    target = user_input()
    series = sequence()
    for i in series:
        if i == target:
            print("True")
            return True
        if i > target:
            print("False")
            return False
#Invoke it
fibonacci()