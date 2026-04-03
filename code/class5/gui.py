import tkinter as tk
import time
from tkinter import messagebox


def send_message():
    local_time = time.localtime()
    return f"{local_time.tm_year}-{local_time.tm_mon}-{local_time.tm_mday} {local_time.tm_hour}:{local_time.tm_min}:{local_time.tm_sec}"

def print_message(message):
    output_text.insert("end", message)
    output_text.insert("end", "\n")


def handle_button_click():
    message = entry.get()
    if message:
        print_message(message)
        entry.delete(0, tk.END)

# 创建主窗口
root = tk.Tk()
root.title("mini ChatGPT Code")
root.geometry("900x700")

# 创建输入框
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

user_input = entry.get()

# 创建多行输出框
output_text = tk.Text(root, height=25, width=100)
output_text.pack()


output_text.insert("end", send_message())


output_text.delete("5.0", "end")

output_text.insert("end", "\n")
output_text.insert("end", "helloWorld")
output_text.insert("end", "\n")

user_input = entry.get()

button = tk.Button(root, text="执行", command=handle_button_click)
button.pack(pady=10)

messagebox.showinfo("提示", "执行完成")
messagebox.showerror("错误", "出错了")

# 进入主循环
root.mainloop()

