import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import logging
import os

# 设置日志
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 默认用户名和密码
DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = 'admin'

# 家庭用户
home_users = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

# 登录函数
def login(username_entry, password_entry, window):
    username = username_entry.get()
    password = password_entry.get()
    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        logging.info(f"User {username} logged in successfully")
        window.destroy()
        user_info_window = tk.Tk()
        user_info_window.title("User Information")
        user_info_window.geometry("700x600")
        
        # 添加系统logo
        add_logo(user_info_window)
        
        # 添加头像
        add_avatar(user_info_window)
        
        # Create Change Password button
        change_password_button = tk.Button(user_info_window, text="Change Password", command=lambda: change_password(user_info_window, username))
        change_password_button.pack(pady=10)
        
        # Create Set Home User button
        set_home_user_button = tk.Button(user_info_window, text="Set Home User", command=lambda: set_home_user(user_info_window))
        set_home_user_button.pack(pady=10)
        
        user_info_window.mainloop()
    else:
        logging.warning(f"User {username} failed to log in")
        messagebox.showerror("Login Failed", "Incorrect username or password!")

# 更改密码函数
def change_password(window, username):
    window.destroy()
    change_password_window = tk.Tk()
    change_password_window.title("Change Password")
    change_password_window.geometry("700x600")
    
    # 添加系统logo
    add_logo(change_password_window)
    
    new_password_label = tk.Label(change_password_window, text="Enter new password:")
    new_password_label.pack(pady=10)
    
    new_password_entry = tk.Entry(change_password_window, show="*")
    new_password_entry.pack(pady=10)
    
    confirm_button = tk.Button(change_password_window, text="Confirm", command=lambda: update_password(username, new_password_entry.get(), change_password_window))
    confirm_button.pack(pady=10)
    
    change_password_window.mainloop()

def update_password(username, new_password, window):
    global DEFAULT_PASSWORD, home_users
    if username == DEFAULT_USERNAME:
        DEFAULT_PASSWORD = new_password
        logging.info("Admin password updated")
    elif username in home_users:
        home_users[username] = new_password
        logging.info(f"Password for user {username} updated")
    else:
        logging.warning("User does not exist")
        messagebox.showerror("User does not exist", "This user does not exist!")
    messagebox.showinfo("Password Updated", "Password updated successfully!")
    window.destroy()

# 设置家庭用户函数
def set_home_user(window):
    window.destroy()
    set_user_window = tk.Tk()
    set_user_window.title("Set Home User")
    set_user_window.geometry("700x600")
    
    # 添加系统logo
    add_logo(set_user_window)
    
    username_label = tk.Label(set_user_window, text="Username:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(set_user_window)
    username_entry.pack(pady=10)
    
    password_label = tk.Label(set_user_window, text="Password:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(set_user_window, show="*")
    password_entry.pack(pady=10)
    
    confirm_button = tk.Button(set_user_window, text="Confirm", command=lambda: add_home_user(username_entry.get(), password_entry.get(), set_user_window))
    confirm_button.pack(pady=10)
    
    set_user_window.mainloop()

def add_home_user(username, password, window):
    global home_users
    home_users[username] = password
    logging.info(f"Home user {username} added")
    messagebox.showinfo("User Added", f"Home user {username} added successfully!")
    window.destroy()

# 创建登录界面
def create_login_gui():
    login_window = tk.Tk()
    login_window.title("Login System")
    login_window.geometry("700x600")

    # 添加系统logo
    add_logo(login_window)
    
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.insert(0, "admin")
    username_entry.pack(pady=10)

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=10)

    login_button = tk.Button(login_window, text="Login", command=lambda: login(username_entry, password_entry, login_window))
    login_button.pack(pady=10)

    login_window.mainloop()

# 添加系统logo函数
def add_logo(window):
    current_dir = os.path.dirname(__file__)
    logo_path = os.path.join(current_dir, "logoicon.png")
    if os.path.exists(logo_path):
        logo_image = Image.open(logo_path)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(window, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.pack(pady=10)
    else:
        logging.warning("Logo image not found")

# 添加头像函数
def add_avatar(window):
    current_dir = os.path.dirname(__file__)
    avatar_path = os.path.join(current_dir, "avatar.png")
    if os.path.exists(avatar_path):
        avatar_image = Image.open(avatar_path)
        avatar_image = avatar_image.resize((200, 200))
        avatar_photo = ImageTk.PhotoImage(avatar_image)
        avatar_label = tk.Label(window, image=avatar_photo)
        avatar_label.image = avatar_photo
        avatar_label.pack(pady=10)
    else:
        logging.warning("Avatar image not found")

# 空的 main 函数
def main():
    pass

# 测试代码
if __name__ == "__main__":
    create_login_gui()
