from tkinter import *
from tkinter import  messagebox
import pymysql
#from PIL import Image, ImageTk
from signuppage import SignUp

class Login:
    def __init__(self, root):
        self.window = root
        self.window.title("Login Page")
        self.window.geometry("1000x600+200+50")
        self.window.resizable(False, False)
        
        # Left Frame
        self.left_frame = Frame(self.window, bg="#03353b")
        self.left_frame.place(x=0, y=0, width=500, height=600)
        
        title = Label(self.left_frame, text="Secure Login System", font=("Arial", 20, "bold"), fg="white", bg="#03353b")
        title.place(x=80, y=50)
        
        subtitle = Label(self.left_frame, text="Built with Python", font=("Arial", 14, "italic"), fg="white", bg="#03353b")
        subtitle.place(x=160, y=100)
        
        bottom_text = Label(self.left_frame, text="Made for you", font=("Arial", 12, "italic"), fg="white", bg="#03353b")
        bottom_text.place(x=180, y=550)
        
        # Right Frame
        self.right_frame = Frame(self.window, bg="#aeaeaf")
        self.right_frame.place(x=500, y=0, width=500, height=600)
        
        title2 = Label(self.right_frame, text="Login", font=("Arial", 22, "bold"), bg="#aeaeaf", fg="black")
        title2.place(x=200, y=50)
        
        Label(self.right_frame, text="Email", font=("Arial", 14, "bold"), bg="#aeaeaf", fg="black").place(x=50, y=120)
        self.email_txt = Entry(self.right_frame, font=("Arial", 12))
        self.email_txt.place(x=50, y=150, width=400)
        
        Label(self.right_frame, text="Password", font=("Arial", 14, "bold"), bg="#aeaeaf", fg="black").place(x=50, y=200)
        
        self.password_txt = Entry(self.right_frame, font=("Arial", 12), show="*")
        self.password_txt.place(x=50, y=230, width=400)
        
        # Show Password Option
        self.show_var = IntVar()
        self.show_password = Checkbutton(self.right_frame, text="Show Password", variable=self.show_var, command=self.toggle_password, bg="#aeaeaf")
        self.show_password.place(x=50, y=260)
        
        self.login_btn = Button(self.right_frame, text="Login", font=("Arial", 14, "bold"), command=self.login, bg="green", fg="white", cursor="hand2")
        self.login_btn.place(x=50, y=320, width=400)
        
        self.forgot_pass_btn = Button(self.right_frame, text="Forgot Password?", font=("Arial", 12), fg="blue", bg="#aeaeaf", bd=0, command=self.forgot_password)
        self.forgot_pass_btn.place(x=50, y=370)
        
        self.signup_btn = Button(self.right_frame, text="New User? Sign Up", font=("Arial", 12), fg="black", bg="#aeaeaf", bd=0, command=self.open_signup)
        self.signup_btn.place(x=50, y=400)
    
    def toggle_password(self):
        if self.show_var.get():
            self.password_txt.config(show="")
        else:
            self.password_txt.config(show="*")
    
    def login(self):
        email = self.email_txt.get()
        password = self.password_txt.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.window)
        else:
            try:
                connection = pymysql.connect(host="localhost", user="root", password="Keerthi@2004", database="login_data")
                cur = connection.cursor()
                cur.execute("SELECT * FROM login_credentials WHERE email=%s AND password=%s", (email, password))
                row = cur.fetchone()
                connection.close()

                if row is None:
                    messagebox.showerror("Error", "Invalid email or password", parent=self.window)
                else:
                    messagebox.showinfo("Success", "Login successful", parent=self.window)
                    self.window.destroy()  # Close login window
                    self.open_welcome()  # Open welcome window
            except Exception as es:
                messagebox.showerror("Error", f"Error due to {str(es)}", parent=self.window)

    def open_welcome(self):
        self.new_win = Tk()
        self.new_win.title("Welcome")
        self.new_win.geometry("1000x600+200+50")
        self.new_win.resizable(False, False)

        Label(self.new_win, text="Welcome to the Dashboard!", font=("Arial", 20, "bold")).pack(pady=50)

    def forgot_password(self):
        self.new_win = Toplevel(self.window)
        self.new_win.title("Reset Password")
        self.new_win.geometry("400x300+550+250")
        
        Label(self.new_win, text="Enter Email", font=("Arial", 12, "bold")).pack(pady=20)
        self.reset_email = Entry(self.new_win, font=("Arial", 12))
        self.reset_email.pack(pady=5)
        
        Button(self.new_win, text="Reset Password", font=("Arial", 12, "bold"), command=self.reset_password).pack(pady=20)
    
    def reset_password(self):
        email = self.reset_email.get()
        if email == "":
            messagebox.showerror("Error", "Please enter your email", parent=self.new_win)
        else:
            messagebox.showinfo("Success", "Reset link sent to your email", parent=self.new_win)
    
    def open_signup(self):
        from signuppage import SignUp
        self.new_win = Toplevel(self.window)
        SignUp(self.new_win)

if __name__ == "__main__":
    root = Tk()
    Login(root)
    root.mainloop()
