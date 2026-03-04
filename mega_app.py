from tkinter import *
from tkinter import messagebox
import os
import math

DB_FILE = "users.txt"

root = Tk()
root.title("Mega App")
root.geometry("400x600")
root.config(bg="#1e1e2f")
root.resizable(False, False)

# ================= DATABASE =================
def register():
    user = username.get()
    pw = password.get()

    if user == "" or pw == "":
        status.config(text="Isi semua field!", fg="red")
        return

    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for line in f:
                if user == line.split(",")[0]:
                    status.config(text="Username sudah ada!", fg="red")
                    return

    with open(DB_FILE, "a") as f:
        f.write(user + "," + pw + "\n")

    status.config(text="Registrasi berhasil!", fg="lime")

def login():
    user = username.get()
    pw = password.get()

    if not os.path.exists(DB_FILE):
        status.config(text="Belum ada akun!", fg="red")
        return

    with open(DB_FILE, "r") as f:
        for line in f:
            u, p = line.strip().split(",")
            if user == u and pw == p:
                open_dashboard(user)
                return

    status.config(text="Login gagal!", fg="red")

def logout():
    dashboard_frame.pack_forget()
    login_frame.pack(pady=80)
    username.delete(0, END)
    password.delete(0, END)

# ================= DASHBOARD =================
def open_dashboard(user):
    login_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)
    welcome_label.config(text=f"Halo {user} 👋")

# ================= KALKULATOR =================
def press(num):
    calc_entry.insert(END, str(num))

def clear():
    calc_entry.delete(0, END)

def calculate():
    try:
        result = eval(calc_entry.get())
        calc_entry.delete(0, END)
        calc_entry.insert(0, str(result))
    except:
        calc_entry.delete(0, END)
        calc_entry.insert(0, "Error")

# ================= KOMPAS =================
angle = 0

def update_compass():
    canvas.delete("all")
    canvas.create_oval(50, 50, 250, 250, outline="white")
    x = 150 + 80 * math.sin(math.radians(angle))
    y = 150 - 80 * math.cos(math.radians(angle))
    canvas.create_line(150,150,x,y,fill="red",width=3)
    canvas.create_text(150,30,text=f"{angle}°",fill="white")

def rotate_left():
    global angle
    angle = (angle - 15) % 360
    update_compass()

def rotate_right():
    global angle
    angle = (angle + 15) % 360
    update_compass()

# ================= LOGIN UI =================
login_frame = Frame(root, bg="#2c2c3e", padx=20, pady=20)
login_frame.pack(pady=80)

Label(login_frame, text="mika Login",
      font=("Arial",18,"bold"),
      bg="#2c2c3e",
      fg="white").pack(pady=10)

username = Entry(login_frame, width=25)
username.pack(pady=10)

password = Entry(login_frame, width=25, show="*")
password.pack(pady=10)

Button(login_frame,text="Login",width=20,command=login,
       bg="#6c63ff",fg="white").pack(pady=5)

Button(login_frame,text="Register",width=20,command=register,
       bg="#00c853",fg="white").pack(pady=5)

status = Label(login_frame,text="",bg="#2c2c3e")
status.pack()

# ================= DASHBOARD UI =================
dashboard_frame = Frame(root, bg="#1e1e2f")

welcome_label = Label(dashboard_frame,
                      text="",
                      font=("Arial",16,"bold"),
                      bg="#1e1e2f",
                      fg="white")
welcome_label.pack(pady=10)

# ===== KALKULATOR =====
Label(dashboard_frame,text="Kalkulator",
      bg="#1e1e2f",fg="white").pack()

calc_entry = Entry(dashboard_frame,width=25,font=("Arial",14))
calc_entry.pack(pady=5)

btn_frame = Frame(dashboard_frame,bg="#1e1e2f")
btn_frame.pack()

buttons = [
    '7','8','9','/',
    '4','5','6','*',
    '1','2','3','-',
    '0','.','=','+'
]

row=0
col=0
for b in buttons:
    if b == "=":
        cmd = calculate
    else:
        cmd = lambda x=b: press(x)
    Button(btn_frame,text=b,width=5,height=2,
           command=cmd).grid(row=row,column=col,padx=2,pady=2)
    col+=1
    if col>3:
        col=0
        row+=1

Button(dashboard_frame,text="Clear",
       command=clear,bg="#ff4b5c",fg="white").pack(pady=5)

# ===== KOMPAS =====
Label(dashboard_frame,text="Kompas Digital",
      bg="#1e1e2f",fg="white").pack(pady=10)

canvas = Canvas(dashboard_frame,width=300,height=300,
                bg="#1e1e2f",highlightthickness=0)
canvas.pack()

update_compass()

Button(dashboard_frame,text="⟲ Kiri",
       command=rotate_left).pack(side=LEFT,padx=40,pady=10)

Button(dashboard_frame,text="Kanan ⟳",
       command=rotate_right).pack(side=RIGHT,padx=40,pady=10)

Button(dashboard_frame,text="Logout",
       command=logout,bg="#ff4b5c",fg="white").pack(pady=20)

root.mainloop(
# update terbaru
