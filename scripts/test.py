#!/usr/bin/env python

def multiple(arg,*args):
    print("arg: ",arg)

    for value in args:
        print ("other args:", value)

if __name__ == '__main__':
    multiple(1,'a',True)
