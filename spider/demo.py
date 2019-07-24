class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(self.name, self.age)


class Student(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.gender = '男'
    def show2(self):

        super(Student, self).show()


# student = Student('tom', 18)
# student.show2()
# print(student.name)

# import time
# a = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# print(a, type(a))


a = float(40)
b = float('%.2f' % a)
print(b)

