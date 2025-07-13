"""
Problem: Fizz Buzz
Description: Print numbers from 1 to n. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', and for numbers which are multiples of both print 'FizzBuzz'.
"""

def fizz_buzz(n):
    # Implement a function that prints numbers from 1 to n with FizzBuzz logic.
        # Write the exact code to solve this problem. When finished, append the comment #Done! on the last line.
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)    #Done!
    pass
