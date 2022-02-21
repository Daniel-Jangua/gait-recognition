from tkinter import *
from db_service import DbService
from table_grid import TableGrid
import pandas as pd

class BuscaCargos(Toplevel):

    def __init__(self, root, size, title):
        super().__init__(root)
        self.geometry(size)
        self.title(title)
        self.resizable(False, False)
        self.db = DbService('database.gait')

        table_cols = ('id_cargo', 'descricao', 'nivel_acesso')
        col_names = ['ID', 'Descrição', 'Nível de Acesso']
        self.grid_hist = TableGrid(self, table_cols, col_names, 200)
        self.grid_hist.pack()
        self.populate_grid()

    def populate_grid(self):
        query = """
            SELECT id_cargo, descricao, nivel_acesso
            FROM cargos
            WHERE id_cargo != 4
            ORDER BY id_cargo
        """
        cur, result = self.db.execute_query(query)
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(result, columns=column_names)
        iid = 0
        for _, row in df.iterrows():
            self.grid_hist.insert_row((row['id_cargo'], row['descricao'], row['nivel_acesso']), iid)
            iid += 1
