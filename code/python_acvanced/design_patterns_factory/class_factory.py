# 工厂模式

class Person:
    def __init__(self, name : str, age : int , job : str):
        self.name = name
        self.age = age
        self.job = job

class Teacher(Person):
    def __init__(self, name: str, age: int):
        super().__init__(name, age, 'teacher')

class Student(Person):
    def __init__(self, name: str, age: int):
        super().__init__(name, age, 'student')

class Worker(Person):
    def __init__(self, name: str, age: int):
        super().__init__(name, age, 'worker')


class PersonFactory:
    def create_person(self, name: str, age: int, job: str):
        if job == 'teacher':
            return Teacher(name, age)
        elif job == 'student':
            return Student(name, age)
        elif job == 'worker':
            return Worker(name, age)
        else:
            return None
        
        