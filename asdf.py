def fib(n):
    a, b = 0, 1
    for i in range(n-1):
        a, b = b, a + b
    print(a)

# for i in range(10):
fib(10)