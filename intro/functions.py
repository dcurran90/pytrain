''' While easy to understand, the pure recursive method causes a tremendous 
    amount of recursion. Each fib causes 2 fibs which cause 2 fibs, etc until
    they hit 1 and roll up. fib(100) causes so many function calls, that it
    would take longer to execute than the age of the universe.
'''

def fib_recursive(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fib_recursive(x-1) + fib_recursive(x-2)

''' This uses the memorization method. Note how you can refer to variables 
    outside the scope of the fib_memorized_recursive() without effort.
'''

memo = {0:0, 1:1}
def fib_memorized_recursive(x):
    if not x in memo:
        memo[x] = fib_memorized_recursive(x-1) + fib_memorized_recursive(x-2)
    return memo[x]

''' This introduces the concept of a traditional for loop. Python loops are by 
    and large based on iterators because internally everything is an object.
    You won't see for (int i = 0; i <= foo, i++) in here!
'''

def fib_iterator(x):
    a, b = 0, 1
    for i in range(x):
        a, b = b, a + b
    return a

''' This is the coveted generator implementation. Generators are like loops
    that stop execution and return every call. That way, you don't have to 
    calculate the entire data set to start processing the results. This also
    makes it possible to process data larger than the amount of memory in 
    the system. Basically, you yield instead of return on a set.
'''

def fib_generator():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b

def fib_gen_wrap(x):
    fibg = fib_generator()
    return [fibg.next() for i in range(x + 1)][-1]

''' This is the binet's formula. It allows for quick calculation of numbers
    that would be unfortunate to calculate algorithmically. 
    Because of floating point precision, it's only accurate for x<70. 
    Note the math functions available to you. int(), float(), double(). str()
    for strings, and bool() evaluates things for boolean values (True or False)
'''

def fib_binet(x):
    phi = (1 + 5**0.5) / 2
    return int(round((phi**x - (1-phi)**x)  / 5**0.5))

''' This is a pretty cool method that uses bitshifting. You won't see this
    much unless you're doing IP math or something really low level (in that case
    you're probably doing it wrong).

    Also, notice that you can define functions inside of functions. This is a 
    concept you see a lot in python (though not *actually* with functions, 
    typically with lambdas and functool partials).
'''

def fib_bitshift(x):
    def powLF(n):
        if n == 1:
            return (1, 1)
        L, F = powLF(n//2)
        L, F = (L**2 + 5*F**2) >> 1, L*F
        if n & 1:
            return ((L + 5*F)>>1, (L + F) >> 1)
        else:
            return (L, F)
    if x & 1:
        return powLF(x)[1]
    else:
        L, F = powLF(x // 2)
        return L * F

    

''' Now we print the results. By the way, print formatting in python
    is awesome.
'''
val = 7
fibs = {"fib_recursive": fib_recursive(val),
        "fib_memorized_recursive": fib_memorized_recursive(val),
        "fib_iterator": fib_iterator(val),
        "fib_generator": fib_gen_wrap(val),
        "fib_binet": fib_binet(val),
        "fib_bitshift": fib_bitshift(val)}

for k,v in fibs.items():
    print "%-24s %d" % (str(k) + ":",v)



