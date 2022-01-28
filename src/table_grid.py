from tkinter import *
from tkinter import ttk

class TableGrid(Frame):

    def __init__(self, root, table_cols, col_names, col_width):
        super().__init__(root)
        scroll_v = Scrollbar(self)
        scroll_v.pack(side=RIGHT, fill=Y)

        scroll_h = Scrollbar(self, orient='horizontal')
        scroll_h.pack(side=BOTTOM, fill=X)

        self.table = ttk.Treeview(self, yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)
        self.table.pack()

        scroll_v.config(command=self.table.yview)
        scroll_h.config(command=self.table.xview)

        self.table['columns'] = table_cols
        txt = col_names
        i = 0
        self.table.column("#0", width=0,  stretch=NO)
        self.table.heading("#0",text="",anchor=CENTER)
        for tb_name in self.table['columns']:
            self.table.column(tb_name, anchor=CENTER, width=col_width)
            self.table.heading(tb_name, text=txt[i], anchor=CENTER)
            i += 1

    def insert_row(self, values, iid):
        self.table.insert(
            parent='', index='end',iid=iid, text='',
            values=values)
        self.table.pack()
    
    def delete_rows(self):
        self.table.delete(*self.table.get_children())
        