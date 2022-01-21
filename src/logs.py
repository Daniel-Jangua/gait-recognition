from unittest import result
import pandas as pd
from db_service import DbService

class Logs():

    def __init__(self):
        self.db = DbService('database.gait')
    
    def get_df_logs(self):
        query = """SELECT log_det.data_det, funcionarios.nome, cargos.descricao, log_det.autorizado, funcionarios.foto_cracha 
                    FROM funcionarios
                    LEFT JOIN log_det ON funcionarios.id_funcionario = log_det.id_funcionario
                    LEFT JOIN cargos ON funcionarios.id_cargo = cargos.id_cargo 
                    ORDER BY log_det.data_det"""
        cur, result = self.db.execute_query(query)
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(result, columns=column_names)
        return df