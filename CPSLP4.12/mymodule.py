def RenjieWen():
    print("he is cool")

def printLess100(n):
    for x in n:
        if x < 100:
            print(x)
        else:
            print("something larger than 100")

def defineRange(n):
    for x in n:
        if x < 0:
            print(x,'is a negative number')
        elif x >= 43 and x < 100:
            print(x , 'is inside the range')
        else:
            print(x, 'is outside the range')

def ifItemInList(instruments,inventory):
    for item in instruments:
        if item in inventory.keys():
            print(item,'is in the dictionary, the value is', inventory[item])
        else:
            print(item, 'is not in the dictionary')

def write_bottle_song():

    file = open('./!0GreenBottles.txt', 'w')
    for numBottle in range(10):
        s = str(10-numBottle) + " green bottles hanging on the wall, but if one bottle should accidentally fall. There will be " + str(9-numBottle) + " green bottles hanging on the wall\n"
        file.write(s)
    file.close()