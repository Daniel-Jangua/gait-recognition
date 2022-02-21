from tkinter import *
from tkinter import messagebox
from main_window import MainWindow
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from db_service import DbService

class Login():
    
    def __init__(self, size, title):
        self.window = ThemedTk(theme='breeze')
        self.window.resizable(False, False)

        self.db_service = DbService('database.gait')

        self.window.geometry(size)
        self.window.title(title)

        fr_img = Frame(self.window)
        img = Image.open('./assets/logo2.png')
        img = img.resize((100,100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.lbl_imagem = Label(fr_img, image=photo, width=100, height=100)
        self.lbl_imagem.image = photo
        self.lbl_imagem.grid(row=0, column=0)
        fr_img.pack(side=LEFT)

        fr_info = Frame(self.window)
        lbl_login = Label(fr_info, text='Login', font=('Arial', 11, 'bold'))
        lbl_login.grid(row=0, column=0, pady=10, padx=10)
        self.entry_login = Entry(fr_info, width=30, font=('Arial', 10))
        self.entry_login.grid(row=0, column=1)

        lbl_senha = Label(fr_info, text='Senha', font=('Arial', 11, 'bold'))
        lbl_senha.grid(row=1, column=0, pady=10, padx=10)
        self.entry_senha = Entry(fr_info, width=30, show='*', font=('Arial', 10))
        self.entry_senha.grid(row=1, column=1)

        fr_btns = Frame(fr_info)
        fr_btns.columnconfigure(1, minsize=20, weight=1)
        btn_sair = Button(fr_btns, text='Sair', font=('Arial', 10), width=10, command=self.quit)
        btn_sair.grid(row=0, column=0)

        btn_entrar = Button(fr_btns, text='Entrar', font=('Arial', 10), width=10, command=self.log_in)
        btn_entrar.grid(row=0, column=2)
        fr_btns.grid(row=2, column=1)
        fr_info.pack(side=LEFT)
    
    def quit(self):
        self.window.destroy()
    
    def log_in(self):
        nome = self.entry_login.get()
        senha = self.entry_senha.get()
        query = """SELECT * FROM usuarios 
                    WHERE nome_usuario = '{}' AND senha = '{}'""".format(nome, senha)
        _, result = self.db_service.execute_query(query)
        if len(result):
            self.window.destroy()
            self.db_service.close_conn()
            app = MainWindow('1225x600', 'GaitID - ' + nome, 'http://9ab4-35-237-193-163.ngrok.io')
            app.window.mainloop()
        else:
            messagebox.showerror(title='Falha no Login', message='Usuário ou Senha incorreto(s)!')
            self.entry_login.delete(0, END)
            self.entry_senha.delete(0, END)
        
if __name__ == '__main__':
    login = Login('400x150', 'GaitID - Login')
    login.window.mainloop()
