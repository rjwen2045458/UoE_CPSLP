

# f1 = friend.Friend('Renjie', 23, ['Chinese','English'])

#

'''hello this is doc string'''


class Friend():
    def __init__(self,  firstName = '', age = 0, languagesSpoken = []):
        self.firstName = firstName
        self.age = age
        self.languagesSpoken = languagesSpoken

    def setAge(self, age):
        self.whoKnows = "hello world"
        self.age = age

    # the function input swap all three variables in a Friend instance
    def set(self, firstName, age, languagesSpoken):
        self.firstName = firstName
        self.age = age
        self.languagesSpoken = languagesSpoken

    def printInfo(self):
        self.setAge(self.age)
        print('The name is: ', self.firstName)
        print('The friend`s age is: ', self.age)
        print('The language ', self.languagesSpoken)
        print(self.whoKnows)




