from tkinter import *
from db_service import DbService
from table_grid import TableGrid
import pandas as pd

class BuscaFuncionario(Toplevel):

    def __init__(self, root, size, title):
        super().__init__(root)
        self.geometry(size)
        self.title(title)
        self.resizable(False, False)
        self.db = DbService('database.gait')

        table_cols = ('id_funcionario', 'nome', 'descricao', 'nivel_acesso')
        col_names = ['ID', 'Nome', 'Cargo', 'Nível de Acesso']
        self.grid_hist = TableGrid(self, table_cols, col_names, 300)
        self.grid_hist.pack()
        self.populate_grid()

    def populate_grid(self):
        query = """
            SELECT funcionarios.id_funcionario, funcionarios.nome, cargos.descricao, cargos.nivel_acesso
            FROM funcionarios
            LEFT JOIN cargos ON funcionarios.id_cargo = cargos.id_cargo 
            ORDER BY funcionarios.id_funcionario
        """
        cur, result = self.db.execute_query(query)
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(result, columns=column_names)
        iid = 0
        for _, row in df.iterrows():
            self.grid_hist.insert_row((row['id_funcionario'], row['nome'], row['descricao'], row['nivel_acesso']), iid)
            iid += 1
