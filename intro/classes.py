import locale
locale.setlocale( locale.LC_ALL, '' )

class Employee():
    def __init__(self, fname, lname, title, salary):
        self._fname = fname
        self._lname = lname
        self.title = title
        self._salary = int(salary)
    def _get_fname(self):
        return "%s" % self._fname.capitalize()
    def _get_lname(self):
        return "%s" % self._lname.capitalize()
    def _get_salary(self):
        return "%s USD" % locale.currency(self._salary, grouping=True)
    fname = property(_get_fname)
    lname = property(_get_lname)
    salary = property(_get_salary)
    def give_raise(self,percentage=5):
        self._salary = self._salary * (percentage * .01 + 1)



class Developer(Employee):
    def give_raise(self, percentage=5):
        percentage +=2.5
        Employee.give_raise(self, percentage)


bob = Developer("bob", "last", "dev", 10000)
paul = Employee("paul", "sims", "manager", 5000)
print "Bob's salary: %s" % bob.salary
bob.give_raise()
print "%s's salary after raise: %s" % (bob.fname, bob.salary)
paul.give_raise()
print "poor %s: %s" % (paul.fname, paul.salary)
