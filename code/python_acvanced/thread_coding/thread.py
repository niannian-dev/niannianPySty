#  多线程编码
import time
import threading

def func1(str):
    while True:
        time.sleep(1)
        print(str)

def func2(str):
    while True:
        time.sleep(1)
        print(str)

def func3(str):
    while True:
        time.sleep(1)
        print(str)



'''
threading.Thread([group [,target [,name[,args[,kwargs]]]]])
Thread参数  
    target: 线程要执行的函数
    args: 函数的参数,元组
    kwargs: 函数的参数字典
    name: 线程的名称
    group: 线程组
'''

if __name__ == '__main__':
    func1 = threading.Thread(target=func1, args=('func1',))
    func2 = threading.Thread(target=func2, args=('func2',))
    func3 = threading.Thread(target=func3, kwargs={'str': 'func3'})
    func1.start()
    func2.start()
    func3.start()