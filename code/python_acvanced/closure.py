# python 闭包内容

def outer(a):
    # def inner(b : str):
    #     print(a , ':' , b)
    # return inner

    def inner2(c : int):
        nonlocal a
        a += 5
        print(a , ':' , c)
    return inner2



fun1 = outer(1)
fun1(2)
fun1(5)

fun2 = outer(10)
fun2(2)
fun2(5)

fun3 = outer(100)
fun3(100)
