import os
import traceback
import psycopg2
from datetime import datetime

class ErrorHandling:
    def __init__(self, usr, pwd, bd_pg, bd_port, bd_company):
        self.usr = usr
        self.pwd = pwd
        self.bd_pg = bd_pg
        self.bd_port = bd_port
        self.bd_procesos = "procesos"
        self.bd_company = bd_company
    

    def handle_error(self, table_name):
        outdir_error = './errors/'
        if not os.path.exists(outdir_error):
            os.mkdir(outdir_error)
        
        tb = traceback.format_exc()
        with open(f'{outdir_error}/ERROR {table_name}.txt', 'w') as f:
            f.write(tb)

        try:
            connection = psycopg2.connect(user=self.usr,
                                          password=self.pwd,
                                          host=self.bd_pg,
                                          port=self.bd_port,
                                          database=self.bd_procesos)
            today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            cursor = connection.cursor()
            qry_add_data_comp_net_pt1 = "INSERT INTO public.procesos (proceso,accion,estado,fecha) "
            qry_add_data_comp_net_pt2 = f"VALUES ('{self.bd_company.upper()}','{table_name.upper()}','ERROR','{today}');"
            qry_add_data_comp_net_final = qry_add_data_comp_net_pt1 + qry_add_data_comp_net_pt2
            print(qry_add_data_comp_net_final)
            cursor.execute(qry_add_data_comp_net_final)
            connection.commit()
        except psycopg2.Error as e:
            print("Error while connecting to PostgreSQL", e)
        finally:
            if 'connection' in locals():
                cursor.close()
        outdir_error = './errors/'
        if not os.path.exists(outdir_error):
            os.mkdir(outdir_error)
        
        tb = traceback.format_exc()
        with open(f'{outdir_error}/{table_name}.txt', 'w') as f:
            f.write(tb)

        try:
            connection = psycopg2.connect(user=self.usr,
                                          password=self.pwd,
                                          host=self.bd_pg,
                                          port=self.bd_port,
                                          database=self.bd_procesos)
            
            cursor = connection.cursor()
            qry_add_data_comp_net_final = f"""
                    update procesos
                    set accion ='ERROR {table_name}'
                    ,fecha_fin = CURRENT_TIMESTAMP AT TIME ZONE 'America/Santiago'
                    ,estado = 'ERROR'
                    ,tiempo_ejecucion = AGE(CURRENT_TIMESTAMP AT TIME ZONE 'America/Santiago',fecha)
                    WHERE proceso ='{proceso.upper()}'
                    and fecha::date = current_date::date
                    and cliente = '{self.bd_company.upper()}'
                    AND id = ( select max(id) from procesos where proceso ='{proceso.upper()}'
                    and fecha::date = current_date::date
                    and cliente = '{self.bd_company}')
                    """
            cursor.execute(qry_add_data_comp_net_final)
            
            connection.commit()
        except psycopg2.Error as e:
            print("Error while connecting to PostgreSQL", e)
        finally:
            if 'connection' in locals():
                cursor.close()