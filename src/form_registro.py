from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from db_service import DbService
import os, requests

class FormRegistro(Toplevel):

    def __init__(self, root, size, title, http):
        super().__init__(root)
        self.geometry(size)
        self.title(title)
        self.resizable(False, False)
        self.db = DbService('database.gait')
        self.str_folder = StringVar()
        self.str_folder.set('Selecione uma pasta de templates.')
        self.http = http

        lbl_funcioanrio = Label(self, text='Funcionário:', font=('Arial 11 bold'))
        self.funcioanrios = self.get_funcioanrios()
        self.cb_funcionario = ttk.Combobox(self, values=self.funcioanrios, font=('Arial 10'), width=45)
        self.cb_funcionario.current(0)
        self.lbl_folder = Label(self, textvariable=self.str_folder, font=('Arial 11 bold'), width=30)
        self.btn_buscar = Button(self, text='Buscar Template', font=('Arial', 10), width=14, command=self.buscar_folder)
        self.btn_registrar = Button(self, text='Registrar Template', font=('Arial', 10), width=14, command=self.register_desc)

        lbl_funcioanrio.grid(row=0, column=0, padx=10, pady=10)
        self.cb_funcionario.grid(row=0, column=1, padx=10, pady=10)
        self.btn_buscar.grid(row=1, column=1, padx=10, pady=10, sticky='E')
        self.lbl_folder.grid(row=1, column=0, padx=10, pady=10)
        self.btn_registrar.grid(row=2, column=1, padx=10, pady=10, sticky='E')
    
    def buscar_folder(self):
        foldername = filedialog.askdirectory(initialdir = "./assets",
                                            title = "Selecione um diretório",
                                            parent=self)
        if len(foldername):
            self.str_folder.set('/' + foldername.split('/')[-1] + '/')
            self.foldername = foldername
  
    def get_funcioanrios(self):
        query = """SELECT id_funcionario, nome FROM funcionarios ORDER BY id_funcionario"""
        _, result = self.db.execute_query(query)
        res = [str(row[0]) + '-' + row[1] for row in result]
        return res

    def create_descriptors(self):
        folder = self.foldername
        payload={}
        frames = os.listdir(folder)
        files = []
        for frame in frames:
            files.append(('files', (frame, open(folder + '/' + frame, 'rb'), 'image/jpeg')))
        headers = {}
        response = requests.request("POST", self.http + '/extractfeatures/', headers=headers, data=payload, files=files)
        if response.status_code == 200:
            return response.json()
        return False

    def register_desc(self):
        try:
            descriptor = self.create_descriptors()
            if not descriptor:
                raise
            id_func = int(self.cb_funcionario.get().split('-')[0])
            query = """INSERT INTO templates (id_funcionario, descritor) VALUES ({}, '{}')""".format(id_func, str(descriptor))
            self.db.execute_query(query)
            messagebox.showinfo(title='Sucesso', message='Template registrado com sucesso!', parent=self)
            self.cb_funcionario.current(0)
        except Exception as e:
            messagebox.showerror(title='Falha no Registro', message='Erro ao registrar template!\n' + str(e), parent=self)
    