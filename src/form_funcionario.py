from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from db_service import DbService
from PIL import Image, ImageTk

class FormFuncionario(Toplevel):

    def __init__(self, root, size, title):
        super().__init__(root)
        self.geometry(size)
        self.title(title)
        self.resizable(False, False)
        self.db = DbService('database.gait')

        lbl_nome = Label(self, text='Nome Completo:', font=('Arial 11 bold'))
        lbl_cargo = Label(self, text='Cargo:', font=('Arial 11 bold'))
        self.cargos = self.get_cargos()
        self.cb_cargo = ttk.Combobox(self, values=self.cargos, font=('Arial 10'), width=45)
        self.cb_cargo.current(0)
        self.entry_nome = Entry(self, width=50, font=('Arial 10'))
        lbl_nome.grid(row=0, column=0, padx=10, pady=10)
        lbl_cargo.grid(row=1, column=0, padx=10, pady=10)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)
        self.cb_cargo.grid(row=1, column=1, padx=10, pady=10)

        fr_btns = Frame(self)
        self.btn_img = Button(fr_btns, text='Buscar Imagem', font=('Arial', 10), width=14, command=self.buscar_img)
        self.btn_img.grid(row=0, column=0, pady=10, sticky='E')

        fr_img = Frame(self)
        img = Image.open('./assets/logo2.png')
        img = img.resize((200,200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.lbl_imagem = Label(fr_img, image=photo, width=200, height=200)
        self.lbl_imagem.image = photo
        self.lbl_imagem.grid(row=0, column=0)
        fr_img.grid(row=2, column=1, pady=10, padx=10)

        self.btn_cad = Button(fr_btns, text='Cadastrar', font=('Arial', 10), width=14, command=self.cad_funcionario)
        self.btn_cad.grid(row=0, column=1, pady=10, padx=10, sticky='E')
        fr_btns.grid(row=3, column=1, pady=10)
    
    def get_cargos(self):
        query = """SELECT id_cargo, descricao FROM cargos
                    ORDER BY id_cargo"""
        _, result = self.db.execute_query(query)
        res = [str(row[0]) + '-' + row[1] for row in result]
        return res
    
    def cad_funcionario(self):
        nome = self.entry_nome.get()
        cargo = int(self.cb_cargo.get().split('-')[0])
        if nome == '':
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar funcionário!', parent=self)
            return
        query = """INSERT INTO funcionarios (nome, id_cargo, foto_cracha) 
                    VALUES ('{}', {}, NULL)""".format(nome, cargo)
        try:
            self.db.execute_query(query)
            messagebox.showinfo(title='Sucesso', message='Funcionário cadastrado com sucesso!', parent=self)
            self.entry_nome.delete(0, END)
            self.cb_cargo.current(0)
        except Exception as e:
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar funcionário!\n' + str(e), parent=self)

    def buscar_img(self):
        filename = filedialog.askopenfilename(initialdir = "./assets",
                                            title = "Selecione uma imagem",
                                            filetypes = (("Imagens", "*.jpg*"),
                                                        ("Imagens", "*.jpeg*"),
                                                        ("Imagens", "*.png*")),
                                            parent=self)
        if len(filename):
            img = Image.open(filename)
            img = img.resize((200,200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.lbl_imagem.configure(image=photo)
            self.lbl_imagem.image = photo