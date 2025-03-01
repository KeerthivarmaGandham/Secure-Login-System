from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import pymysql, os
import credentials as cr

class SignUp:
    def __init__(self, root):
        self.window = root
        self.window.title("Sign Up")
        self.window.geometry("1000x600+200+50")
        self.window.resizable(False, False)

        # Background Image
        original_img = Image.open("C:/Users/chand/OneDrive/Documents/Secure-Login-System/PHOTO2.JPG")
        resized_img = original_img.resize((1000, 600), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized_img)
        background = Label(self.window, image=self.bg_img)
        background.place(x=0, y=0, relwidth=1, relheight=1)

        # Signup Frame
        frame = Frame(self.window, bg="white", bd=2, relief=RIDGE)
        frame.place(x=275, y=100, width=450, height=500)

        title1 = Label(frame, text="Sign Up", font=("Arial", 22, "bold"), bg="white").place(x=160, y=20)
        title2 = Label(frame, text="Join us today!", font=("Arial", 12), bg="white", fg="gray").place(x=160, y=55)

        Label(frame, text="First Name", font=("Arial", 12, "bold"), bg="white").place(x=20, y=100)
        Label(frame, text="Last Name", font=("Arial", 12, "bold"), bg="white").place(x=240, y=100)
        
        self.fname_txt = Entry(frame, font=("Arial", 12))
        self.fname_txt.place(x=20, y=130, width=200)
        
        self.lname_txt = Entry(frame, font=("Arial", 12))
        self.lname_txt.place(x=240, y=130, width=180)
        
        Label(frame, text="Email", font=("Arial", 12, "bold"), bg="white").place(x=20, y=170)
        self.email_txt = Entry(frame, font=("Arial", 12))
        self.email_txt.place(x=20, y=200, width=400)
        
        Label(frame, text="Security Question", font=("Arial", 12, "bold"), bg="white").place(x=20, y=240)
        Label(frame, text="Answer", font=("Arial", 12, "bold"), bg="white").place(x=240, y=240)
        
        self.questions = ttk.Combobox(frame, font=("Arial", 12), state='readonly', justify=CENTER)
        self.questions['values'] = ("Select", "What's your pet name?", "Your first teacher's name", "Your birthplace", "Your favorite movie")
        self.questions.place(x=20, y=270, width=200)
        self.questions.current(0)
        
        self.answer_txt = Entry(frame, font=("Arial", 12))
        self.answer_txt.place(x=240, y=270, width=180)
        
        Label(frame, text="Password", font=("Arial", 12, "bold"), bg="white").place(x=20, y=310)
        self.password_txt = Entry(frame, font=("Arial", 12), show="*")
        self.password_txt.place(x=20, y=340, width=400)
        
        self.terms = IntVar()
        terms_and_con = Checkbutton(frame, text="I agree to the Terms & Conditions", variable=self.terms, onvalue=1, offvalue=0, bg="white", font=("Arial", 10)).place(x=20, y=380)
        
        self.signup = Button(frame, text="Sign Up", command=self.signup_func, font=("Arial", 14, "bold"), bd=0, cursor="hand2", bg="#28a745", fg="white")
        self.signup.place(x=120, y=420, width=200)
    
    def signup_func(self):
        if self.fname_txt.get() == "" or self.lname_txt.get() == "" or self.email_txt.get() == "" or self.questions.get() == "Select" or self.answer_txt.get() == "" or self.password_txt.get() == "":
            messagebox.showerror("Error!", "All fields are required", parent=self.window)
        elif self.terms.get() == 0:
            messagebox.showerror("Error!", "Please agree to the Terms & Conditions", parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("SELECT * FROM login_credentials WHERE email=%s", self.email_txt.get())
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error!", "Email already exists, please use another", parent=self.window)
                else:
                    cur.execute("INSERT INTO login_credentials (f_name, l_name, email, question, answer, password) VALUES (%s, %s, %s, %s, %s, %s)",
                                (self.fname_txt.get(), self.lname_txt.get(), self.email_txt.get(), self.questions.get(), self.answer_txt.get(), self.password_txt.get()))
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Success!", "Registration successful", parent=self.window)
                    self.reset_fields()
            except Exception as es:
                messagebox.showerror("Error!", f"Error due to {es}", parent=self.window)
    
    def reset_fields(self):
        self.fname_txt.delete(0, END)
        self.lname_txt.delete(0, END)
        self.email_txt.delete(0, END)
        self.questions.current(0)
        self.answer_txt.delete(0, END)
        self.password_txt.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    obj = SignUp(root)
    root.mainloop()
