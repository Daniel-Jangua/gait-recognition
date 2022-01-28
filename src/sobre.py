from tkinter import *
from PIL import Image, ImageTk

class Sobre(Toplevel):

    def __init__(self, root, size, title):
        super().__init__(root)
        self.geometry(size)
        self.title(title)
        self.resizable(False, False)

        img = Image.open('./assets/logo2.png')
        img = img.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.lbl_imagem = Label(self, image=photo, width=200, height=200, anchor='center')
        self.lbl_imagem.image = photo
        self.lbl_imagem.grid(row=0, column=0, padx=45, pady=10)

        lbl_nome = Label(self, text='GaitID', font=('Arial', 15, 'bold'))
        lbl_nome.grid(row=1, column=0)

        lbl_1 = Label(self, text='Sistema de Reconhecimento Biométrico Baseado em Marcha', font=('Arial', 11), foreground='gray')
        lbl_1.grid(row=2, column=0, padx=5)
        lbl_2 = Label(self, text='TCC - Bacharelado em Ciência da Computação', font=('Arial', 11), foreground='gray')
        lbl_2.grid(row=3, column=0)
        lbl_3 = Label(self, text='Aluno: Daniel Ricardo S. Jangua', font=('Arial', 11), foreground='gray')
        lbl_3.grid(row=4, column=0)
        lbl_3 = Label(self, text='Orientador: Aparecido Nilceu Marana', font=('Arial', 11), foreground='gray')
        lbl_3.grid(row=5, column=0)
