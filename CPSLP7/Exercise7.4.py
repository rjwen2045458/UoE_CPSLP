#!/usr/bin/env python

import argparse

def do_ok_function():
    pass

def do_divide_by_zero():
    6/0

def do_index_error():
    'CPSLP'[23]

def do_value_error():
    int('kdhfds')

def do_key_error():
    {}['missing_key']

def do_attribute_error():
    'somestring'.does_not_have_this_attribute

fundict = { 'ZeroDivideError': do_divide_by_zero,
            'IndexError': do_index_error,
            'ValueError': do_value_error,
            'KeyError': do_key_error,
            'AttributeError': do_attribute_error,
            'OKFunction': do_ok_function}

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument( '-v', '--verbose', action='store_true', default=False, help="print verbose info")
    parser.add_argument( 'errorname', nargs='+', help="names of functions to run" )
    args = parser.parse_args()

    verbose = args.verbose

    for i, fname in enumerate(args.errorname,1):
        try:
            f = fundict[fname]
        except KeyError:
            raise ValueError('The function name you specified was not found: {}'.format(fname))

        try:
            print('** Trying function {0}: {1} **'.format(i, f.__name__))
            f()
        except ZeroDivisionError as e:
            print('Oops, caused a ZeroDivisionError')
            if verbose:
                print(type(e), e)
        except (IndexError, AttributeError, KeyError) as e:
            print('Tried to use something that is not there')
            if verbose:
                print(type(e), e)
        except ValueError as e:
            print('Oops, caused a ValueError')
            if verbose:
                print(type(e), e)
        else:
            print('Function "{}" ran without problem'.format(f.__name__))

        print('') # add a newline in between each time through the loop

if __name__ == '__main__':
    main()