#!usr/bin/env python3

from utils import QLearning
__author__ = 'Max Allred'
__version__ = 'Spring 2022'
__pylint__ = 'Version 2.12.2'
'''
A simple program that shows an example of qlearning
'''



ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1

def main():
    '''
    starts the application
    '''
    test = QLearning(ALPHA, GAMMA, EPSILON)
    iteration_amount = input("Enter how many training episodes?\n")
    amount = int(iteration_amount)
    test.train(amount)
    print(test.find_policy())


if __name__ == "__main__":
    main()
