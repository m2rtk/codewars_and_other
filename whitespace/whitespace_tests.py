from whitespace.whitespace import whitespace


def tprint(actual, expected):
    print(f"Output:   '{actual}'")
    print(f"Expected: '{expected}'")
    print()


print("Testing push, output of numbers 0 through 3")
output1 = "   \t\n\t\n \t\n\n\n"
output2 = "   \t \n\t\n \t\n\n\n"
output3 = "   \t\t\n\t\n \t\n\n\n"
output0 = "    \n\t\n \t\n\n\n"
tprint(whitespace(output1), "1")
tprint(whitespace(output2), "2")
tprint(whitespace(output3), "3")
tprint(whitespace(output0), "0")

print("Testing ouput of numbers -1 through -3")
outputNegative1 = "  \t\t\n\t\n \t\n\n\n"
outputNegative2 = "  \t\t \n\t\n \t\n\n\n"
outputNegative3 = "  \t\t\t\n\t\n \t\n\n\n"
tprint(whitespace(outputNegative1), "-1")
tprint(whitespace(outputNegative2), "-2")
tprint(whitespace(outputNegative3), "-3")

print("Testing output of letters A through C")
outputA = "   \t     \t\n\t\n  \n\n\n"
outputB = "   \t    \t \n\t\n  \n\n\n"
outputC = "   \t    \t\t\n\t\n  \n\n\n"
tprint(whitespace(outputA), "A")
tprint(whitespace(outputB), "B")
tprint(whitespace(outputC), "C")