from tkinter import *
from tkinter import messagebox
from db_service import DbService

class FormUsuario(Toplevel):

    def __init__(self, root, size, title):
        super().__init__(root)
        self.geometry(size)
        self.title(title)
        self.resizable(False, False)
        self.db = DbService('database.gait')

        lbl_nome = Label(self, text='Nome de Usuário:', font=('Arial 11'))
        lbl_senha = Label(self, text='Senha:', font=('Arial 11'))
        self.entry_nome = Entry(self, width=40, font=('Arial 10'))
        self.entry_senha = Entry(self, width=40, font=('Arial 10'), show='*')
        lbl_nome.grid(row=0, column=0, padx=10, pady=10)
        lbl_senha.grid(row=1, column=0, padx=10, pady=10)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)
        self.entry_senha.grid(row=1, column=1, padx=10, pady=10)

        self.btn_cad = Button(self, text='Cadastrar', font=('Arial', 10), width=10, command=self.cad_usuario)
        self.btn_cad.grid(row=2, column=1, pady=10)
    
    def cad_usuario(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        if nome == '' or senha == '':
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar usuário!', parent=self)
            return
        query = """INSERT INTO usuarios (nome_usuario, senha) 
                    VALUES ('{}', '{}')""".format(nome, senha)
        try:
            self.db.execute_query(query)
            messagebox.showinfo(title='Sucesso', message='Usuário cadastrado com sucesso!', parent=self)
            self.entry_nome.delete(0, END)
            self.entry_senha.delete(0, END)
        except Exception as e:
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar usuário!\n' + str(e), parent=self)
