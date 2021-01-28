import friend


f1 = friend.Friend('Renjie', 23, ['Chinese','English'])
f1.printInfo()
f2 = friend.Friend()
#f2.printInfo()
f3 = friend.Friend(age = 23)
#f3.printInfo()

f1.setAge(88)
f1.printInfo()
f1.set('robot', 1, ['java', 'python'])
f1.printInfo()
print(f1.whoKnows)

