a = ['Fizz' * (i % 3 == 0) + 'Buzz' * (i % 5 == 0) or i for i in range(1, 101)]


def fizz0(x):
    if x % 15 == 0: return "FizzBuzz"
    if x % 5 == 0: return "Buzz"
    if x % 5 == 0: return "Fizz"
    return str(x)


def fizz1(x):
    for num, s in [(15, "FizzBuzz"), (5, "Buzz"), (3, "Fizz")]:
        if x % num == 0: return s
    return str(x)
