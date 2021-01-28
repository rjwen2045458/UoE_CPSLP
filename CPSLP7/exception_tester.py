#!/usr/bin/env python3

# ZeroDivisionError demo
def ZDE():
    x = 10 / 0


try:
    ZDE()
except ZeroDivisionError:
    print('ZeroDivisionError catched')


# IndexError demo
def IE():
    x = [0, 1, 2]
    y = x[3]


try:
    IE()
except IndexError:
    print('Index Error catched')


# ValueError demo
def VE():
    x = float('hello')


try:
    VE()
except ValueError:
    print('Value error catched')


# KeyError demo
def KE():
    dict = {"CPSLP": 10, "MLP": 20, "ANLP": 20}
    x = dict["HCI"]


try:
    KE()
except KeyError:
    print('Key error catched')


# AttributeError demo
def AE():
    x = int.hello()


try:
    AE()
except AttributeError:
    print('attribue error catched')


# success function
def noError():
    pass


ErrorFunction = [ZDE, IE, VE, KE, AE, noError]

for function in ErrorFunction:
    print('the funcion is:', function.__name__)
    try:
        function()
    except (ZeroDivisionError, IndexError) as exp:
        print('Oops, caused an', ZeroDivisionError.__name__, exp.__class__.__name__)
    except (ValueError, AttributeError, KeyError) as exp1:
        print('Oops, tried to use something that is not there', exp1)
    else:
        print('function', function.__name__, 'ran without problem')


if __name__ == '__main__':
    print('hello')