# define Python user-defined exceptions
class Error(Exception):
"""Base class for other exceptions"""
pass
class ValueTooSmallError(Error):
"""Raised when the input value is too small"""
pass
class ValueTooLargeError(Error):
"""Raised when the input value is too large"""
pass
# Start of Program
# you need to guess this number
number = 10
# user guesses a number until he/she gets it right
while True:
try:
guess = int(input("Enter a number: "))
if guess == number:
break
elif guess < number:
raise ValueTooSmallError
elif guess > number:
raise ValueTooLargeError
except ValueTooSmallError:
print("This value is too small, try again!")
print()
except ValueTooLargeError:
print("This value is too large, try again!")
print()
print("Congratulations! You guessed it correctly.")
