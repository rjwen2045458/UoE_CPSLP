import mymodule

# creates some variables
n = [-5, 23, 43, 68, 99, 100, 101, 3433]

instruments = ['piano', 'guitar', 'banjo', 'flute', 'drums']

inventory = {'piano': 2, 'guitar':5, 'drums': 7}

# test the functions
mymodule.RenjieWen()

mymodule.printLess100(n)

mymodule.defineRange(n)

mymodule.ifItemInList(instruments,inventory)

mymodule.write_bottle_song()

# file = open('./!0GreenBottles.txt', 'a')
# file.write("hello world")
# file.close()
