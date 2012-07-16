''' let's start by looking at sets. Sets are unordered lists that contain 
    unique objects. If you add a duplicate, it won't add another 
    element to the list. Because they are identical to lists, you must start
    them off with set()
'''

set1 = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
set2 = set([2, 4, 6, 8, 10, 12, 14, 16, 18])
set3 = set([3, 6, 9, 12, 15, 18, 21, 24, 27])

# union the 2 sets
set1 | set2 

# intersection
set1 & set2 

# difference
set1 - set2 

# xor
set1 ^ set2

# Works much like +=, -=, etc does for number variables
set1 |= set([8,99]) 

# A frozenset is the same as a set, except it is immutable.

# Lists are just like sets, only they hold anything.

list1 = [1, 12, 123, 1, 12, 123]
list2 = [1, 3, 5, 7, 9, 12]
len(list1) == 6

''' You can do some fancy things with lists and slices.
    Short hand:
        list[start:end] = a list of items from list[start]
            to list[end - 1]
        list[start:] = items from list[start] through list[-1]
        list[:end] = items from beginning to list[end - 1]
        list[:] a copy of the list

    There's an optional "step" field that goes at the end. 
    It's defaulted to 1.

    list[start:end:2] = step through list[start] - list[end]
    , but only return every 2 values:
        list1[0:6:2] == [1, 123, 12] (even indexed entries in a list)
        list1[::-1] == [123, 12, 1, 123, 12, 1] (reverses a list)
'''

# A tuple is just like a list, only immutable and is started with ()

tuple1 = ("one", 2, -4)
tuple1[::-1] == (-4, 2, 'one')


''' Dictionaries are your best friends. They are basic hashmaps that you can
    store almost anything in. The one caveat is that the keys have to be 
    hashable (but that's almost everything).
'''

dict1 = {"one": 1, "two": 2, "three": 3}
dict2 = {"two": 2, "four": 4, "six": 6}

dict1['one'] == 1

''' List comprehensions are the last data type being covered. They allow
    you to powerfully build lists from loops and conditionals. We'll
    just look at simple ones now, but there are more coming up later.
'''

[l*2 for l in list1 if l % 2 == 0]
[("a" + str(a), "b" + str(b)) for a in list1 for b in list2]

f = lambda x: x*x
xs = [x**2 for x in range(20)]    
[f(x) for x in xs]
