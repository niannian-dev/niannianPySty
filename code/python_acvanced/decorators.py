# python 装饰器内容

def decorator(func):
    def wrapper():
        print('start')
        func()
        print('end')
    return wrapper

@decorator
def fun1():
    print('fun1')

fun1()
