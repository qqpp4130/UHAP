import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")  # 设置窗口标题
        self.master.geometry("400x400")  # 设置窗口大小
        self.master.configure(bg="#fafafa")  # 设置窗口背景颜色

        # 加载指定的 logo 图片
        self.logo_image = Image.open("/home/asher/Desktop/logo.png")
        self.logo_image = self.logo_image.resize((100, 100))  # 调整图片大小
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.master, image=self.logo, bg="#fafafa")
        self.logo_label.pack(pady=20)

        # 创建登录界面的输入框和按钮
        self.label_username = tk.Label(self.master, text="Username", bg="#fafafa", font=("Arial", 12))
        self.label_username.pack()
        self.entry_username = tk.Entry(self.master, bg="#f0f0f0", fg="black", font=("Arial", 12), relief=tk.FLAT)
        self.entry_username.pack(ipadx=10, ipady=5, pady=5)

        self.label_password = tk.Label(self.master, text="Password", bg="#fafafa", font=("Arial", 12))
        self.label_password.pack()
        self.entry_password = tk.Entry(self.master, show="*", bg="#f0f0f0", fg="black", font=("Arial", 12), relief=tk.FLAT)
        self.entry_password.pack(ipadx=10, ipady=5, pady=5)

        self.button_frame = tk.Frame(self.master, bg="#fafafa")
        self.button_frame.pack(pady=10)

        self.button_login = tk.Button(self.button_frame, text="Login", font=("Arial", 10), command=self.login, bg="#4CAF50", fg="white", relief=tk.FLAT)
        self.button_login.pack(side=tk.LEFT, ipadx=10, ipady=5, padx=5, fill=tk.X, expand=True)

        self.button_register = tk.Button(self.button_frame, text="Register", font=("Arial", 10), command=self.register, bg="#2196F3", fg="white", relief=tk.FLAT)
        self.button_register.pack(side=tk.LEFT, ipadx=10, ipady=5, padx=5, fill=tk.X, expand=True)

        # 连接 SQLite 数据库
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()

        # 创建用户表
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            password TEXT
                            )''')
        self.conn.commit()

    def login(self):
        # 获取用户名和密码输入框中的内容
        username = self.entry_username.get()
        password = self.entry_password.get()

        # 查询数据库中是否存在对应的用户名和密码
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            # 如果查询到用户，显示登录成功的消息框
            messagebox.showinfo("Login Success", "Welcome, {}!".format(username))
            self.master.destroy()  # 登录成功后关闭登录窗口
        else:
            # 如果用户名或密码错误，显示登录失败的消息框
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def register(self):
        # 获取用户名和密码输入框中的内容
        username = self.entry_username.get()
        password = self.entry_password.get()

        # 检查用户名是否已存在
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            messagebox.showerror("Registration Failed", "Username already exists")
        else:
            # 注册新用户并显示注册成功的消息框
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Registration Success", "Account {} registered successfully!".format(username))

def show_login_window():
    # 创建 Tkinter 窗口实例
    root = tk.Tk()
    # 创建登录应用实例，并将窗口对象作为参数传递给它
    app = LoginApp(root)
    # 进入 Tkinter 事件循环，显示窗口
    root.mainloop()

# 调用此函数以显示登录界面
show_login_window()
