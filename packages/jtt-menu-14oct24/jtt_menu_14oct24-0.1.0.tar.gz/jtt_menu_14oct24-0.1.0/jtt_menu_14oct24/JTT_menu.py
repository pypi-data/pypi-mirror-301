import random
import pytest

def menu(**kwargs):
    """
    Return the user selected function from the
    input dictionary of key/values function names
    / functions. 
    """
    while True:
        print('The selectable options are: ', end='\n\t-')
        print('\n\t-'.join([keyword for
                            keyword in sorted(kwargs)]))
        userInput = input('Please select an option: ')
        if userInput in kwargs:
            return kwargs[userInput]()
        else:
            print('Error! Try again')
