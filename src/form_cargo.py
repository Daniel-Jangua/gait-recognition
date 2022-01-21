from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from db_service import DbService

class FormCargo(Toplevel):

    def __init__(self, root, size, title):
        super().__init__(root)
        self.geometry(size)
        self.title(title)
        self.resizable(False, False)
        self.db = DbService('database.gait')

        lbl_desc = Label(self, text='Descrição:', font=('Arial 11 bold'))
        lbl_acesso = Label(self, text='Nível de Acesso:', font=('Arial 11 bold'))
        self.cb_acesso = ttk.Combobox(self, values = [0, 1, 2], font=('Arial 10'), width=35)
        self.cb_acesso.current(0)
        self.entry_desc = Entry(self, width=40, font=('Arial 10'))
        lbl_desc.grid(row=0, column=0, padx=10, pady=10)
        lbl_acesso.grid(row=1, column=0, padx=10, pady=10)
        self.entry_desc.grid(row=0, column=1, padx=10, pady=10)
        self.cb_acesso.grid(row=1, column=1, padx=10, pady=10)

        self.btn_cad = Button(self, text='Cadastrar', font=('Arial', 10), width=10, command=self.cad_cargo)
        self.btn_cad.grid(row=2, column=1, pady=10)
    
    def cad_cargo(self):
        desc = self.entry_desc.get()
        acesso = self.cb_acesso.get()
        if desc == '':
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar cargo!', parent=self)
            return
        query = """INSERT INTO cargos (descricao, nivel_acesso) 
                    VALUES ('{}', '{}')""".format(desc, acesso)
        try:
            self.db.execute_query(query)
            messagebox.showinfo(title='Sucesso', message='Cargo cadastrado com sucesso!', parent=self)
            self.entry_desc.delete(0, END)
            self.cb_acesso.current(0)
        except Exception as e:
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar cargo!\n' + str(e), parent=self)
