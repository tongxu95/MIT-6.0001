#MIT 6.0001 Introduction to Computer Science and Programming in Python, Problem Set 0
#Function: ask user to enter "x" and "y" and print x^y and log2(x)

#in python, you do not need to declare a variable, pythons sets the variable type based on the value
#assigned to it 
#input() always convert the input into strings so must cast to perform mathematic functions
#\n = Enter (skips to the next line; \t tab (indentation)
x=input('Enter number x:\n')
y=input('Enter number y:\n')
import math
X=float(x)
Y=float(y)
a=X**Y
b=math.log(X,2)

#can connect objects in print() using ',' or '+'. When using ',', python will automatically add a 
#space between objects separated by ','. When using '+', the objects are joined together withou 
#spaces, but all objects must be strings
print('x**y=',a)
print('log(x)=',b)