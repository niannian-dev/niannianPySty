#print函数
#不换行输出
a = 10
b = 20
print(a , b , "hello")

#输出ASCII码
print(chr(65))
print(ord('c'))
print(ord('北'))
print(chr(21271))

#输出到文件中
fp = open("test.txt","w")   #w表示写入模式
fp.write("hello world")
fp.close()

#完整格式
fp1 = open("test1.txt","w")   #w表示写入模式
print(a,b,"hello",sep=' ',end='\n',file=fp1)
fp1.close()
