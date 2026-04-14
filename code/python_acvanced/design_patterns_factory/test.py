# 测试工厂模式
from class_factory import PersonFactory

pf = PersonFactory()

teacher = pf.create_person('张老师', 35, 'teacher')
print(teacher.name, teacher.age, teacher.job)

student = pf.create_person('小明', 18, 'student')
print(student.name, student.age, student.job)

worker = pf.create_person('李工', 28, 'worker')
print(worker.name, worker.age, worker.job)
