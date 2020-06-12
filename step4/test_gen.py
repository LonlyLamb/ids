def testgen():
    yield 1
    yield 2
    yield 3

g = testgen()

g

print(g)
print(g)
print(g)