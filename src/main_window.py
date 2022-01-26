from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkvideo import tkvideo
from form_cargo import FormCargo
from table_grid import TableGrid
from form_usuario import FormUsuario
from form_funcionario import FormFuncionario
from form_registro import FormRegistro
from logs import Logs
import threading

class MainWindow():

    def __init__(self, size, title, http):
        self.window = ThemedTk(theme='breeze')
        self.window.resizable(False, False)
        self.video_name = './assets/last_det.mp4'
        self.log_service = Logs()
        self.http = http

        s = ttk.Style()
        s.configure('TNotebook.Tab', font=('Arial','11','bold') )

        self.window.geometry(size)
        self.window.title(title)
        menubar = tk.Menu(self.window)

        tab_control = ttk.Notebook(self.window)
        tab_main = ttk.Frame(tab_control)
        self.tab_hist = ttk.Frame(tab_control)
        tab_control.add(tab_main, text='Última Detecção')
        tab_control.add(self.tab_hist, text='Histórico de Detecções')
        tab_control.pack(expand=1, fill='both')

        self.table_cols = ('data', 'funcionario', 'cargo', 'status')
        self.col_names = ['Data-Hora', 'Funcionário', 'Cargo', 'Status']
        self.grid_hist = TableGrid(self.tab_hist, self.table_cols, self.col_names, 300)
        self.grid_hist.pack()
        
        cad_menu = tk.Menu(menubar, tearoff=0)
        cad_menu.add_command(label='Usuários', font=('Arial', 11), command=self.forms_cad_usuario)
        cad_menu.add_command(label='Funcionários', font=('Arial', 11), command=self.forms_cad_funcionario)
        cad_menu.add_command(label='Cargos', font=('Arial', 11), command=self.forms_cad_cargo)
        menubar.add_cascade(label='Cadastros', menu=cad_menu, font=('Arial', 11))

        menubar.add_command(label='Registro', font=('Arial', 11), command=self.forms_register)

        search_menu = tk.Menu(menubar, tearoff=0)
        search_menu.add_command(label='Funcionários', font=('Arial', 11))
        search_menu.add_command(label='Cargos', font=('Arial', 11))
        menubar.add_cascade(label='Consultas', menu=search_menu, font=('Arial', 11))

        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label='Sobre', font=('Arial', 11))
        menubar.add_cascade(label='Ajuda', menu=about_menu, font=('Arial', 11))
        
        fr_feed = tk.Frame(tab_main)
        fr_feed.columnconfigure(0, minsize=200, weight=1)

        self.str_nome = StringVar(value='Nome do Funcionário')
        self.str_cargo = StringVar(value='Cargo: GERENTE')
        self.str_datetime = StringVar(value='Data: 10/01/22 20:15:50')
        self.str_status = StringVar(value='AUTORIZADO')

        lbl_name = tk.Label(fr_feed, textvariable=self.str_nome, font=('Arial', 16, 'bold'))
        lbl_name.grid(row=1, column=0, padx=10)
        lbl_cargo = tk.Label(fr_feed, textvariable=self.str_cargo, font=('Arial', 13))
        lbl_cargo.grid(row=3, column=0, padx=10, pady=5)
        lbl_datetime = tk.Label(fr_feed, textvariable=self.str_datetime, font=('Arial', 13))
        lbl_datetime.grid(row=4, column=0, padx=10, pady=5)
        self.lbl_status = tk.Label(fr_feed, textvariable=self.str_status, font=('Arial', 15, 'bold'), foreground='green')
        self.lbl_status.grid(row=5, column=0, padx=10, pady=5)
        
        img = Image.open('./assets/refresh_icon.png')
        img = img.resize((50,50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.btn_refesh = tk.Button(fr_feed, text='Atualizar', font=('Arial', 13), image=photo, compound=LEFT, command=self.update_logs)
        self.btn_refesh.image = photo
        self.btn_refesh.grid(row=6, column=0, pady=10)

        img = Image.open('./assets/foto_cracha.png')
        img = img.resize((200,200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.lbl_imagem = tk.Label(fr_feed, image=photo, width=200, height=200, borderwidth=1, relief='solid')
        self.lbl_imagem.image = photo
        self.lbl_imagem.grid(row=2, column=0, pady=20, padx=20)
        fr_feed.grid(row=0, column=0)

        fr_video = tk.Frame(tab_main)
        fr_video.columnconfigure(0, minsize=50, weight=1)
        fr_video.rowconfigure(0, minsize=30, weight=1)
        lb_video = tk.Label(fr_video, relief='solid', borderwidth=1)
        lb_video.grid(row=1, column=1)
        fr_video.grid(row=0, column=1)

        player = tkvideo(self.video_name, lb_video, loop = 1, size = (900, 500))
        player.play()
        self.update_logs()

        self.window.config(menu=menubar)

    def forms_cad_usuario(self):
        FormUsuario(self.window, '450x150', 'Cadastro de Usuários')
    
    def forms_cad_cargo(self):
        FormCargo(self.window, '450x150', 'Cadastro de Cargos')
    
    def forms_cad_funcionario(self):
        FormFuncionario(self.window, '600x400', 'Cadastro de Funcionários')

    def forms_register(self):
        FormRegistro(self.window, '640x160', 'Registro de Templates', self.http)

    def write_to_file(self, filename, data):
        with open(filename, 'wb') as f:
            f.write(data)

    def update_logs(self):
        label_status = {0 : 'NEGADO', 1 : 'AUTORIZADO'}
        color_status = {0 : 'red', 1 : 'green'}
        df = self.log_service.get_df_logs()
        last_log = df.iloc[-1]
        blob_img = last_log['foto_cracha']
        self.str_nome.set(last_log['nome'])
        self.str_cargo.set(last_log['descricao'])
        self.str_datetime.set('Data: ' + last_log['data_det'])
        autorizado = int(last_log['autorizado'])
        self.str_status.set(label_status[autorizado])
        self.lbl_status.configure(foreground=color_status[autorizado])
        self.grid_hist.delete_rows()
        iid = 0
        for _, row in df.iterrows():
            if row['data_det'] is not None:
                self.grid_hist.insert_row((row['data_det'], row['nome'], row['descricao'], label_status[int(row['autorizado'])]), iid)
                iid += 1
        if blob_img is not None and str(blob_img) != '' and str(blob_img) != 'NULL':
            self.write_to_file('./assets/foto_cracha.png', blob_img)
        img = Image.open('./assets/foto_cracha.png')
        img = img.resize((200,200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.lbl_imagem.configure(image=photo)
        self.lbl_imagem.image = photo
        if not autorizado:
            t = threading.Thread(target=messagebox.showwarning, args=('Alerta de Segurança', 'Atenção! Acesso não autorizado detectado.',))
            t.start()

# if __name__ == '__main__':
#     root = MainWindow('1225x600', 'GaitID - ')
#     form = FormFuncionario(root.window, '450x150', 'Cadastro de Usuários') 
#     root.window.mainloop()     