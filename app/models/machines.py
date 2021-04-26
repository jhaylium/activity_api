import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Machine:

    def __init__(self, machine_id:int=None, new_machine:bool=False):
        if new_machine:
            pass
        else:
            self.machine_id = machine_id
            machine_info = self._get_machine_info()
            self.machine_type = machine_info['machine_type']
            self.environment = machine_info['environment']
            self.ip_address = machine_info['ip_address']
            self.machine_name = machine_info['machine_name']

    def _get_machine_info(self):
        conn = psycopg2.connect(self._connection_string())
        cursor = conn.cursor()
        cmd = f"""with base as (select machine_name, environment, ip_address, machine_type from web_activity.machines
                where machine_id  = {self.machine_id}),
                    p1 as (select to_jsonb(base) as jrow
                    from base)
                    select *
                    from p1;"""
        cursor.execute(cmd)
        data = cursor.fetchall()[0][0]
        return data

    def _create_machine(self, machine_name, environment, ip_addr, machine_type, ram, cpu):
        conn = psycopg2.connect(self._connection_string())
        cursor = conn.cursor()
        cmd = f"""insert into web_activity.machines(machine_name, environment, ip_address, machine_type, ram, cpu)
                VALUES ({machine_name}, {environment}, {ip_addr}, {machine_type}, {ram}, {cpu})"""
        cursor.execute(cmd)
        conn.commit()
        cursor.close()
        conn.close()

    def _connection_string(self):
        return f"""user={os.environ['main_db_user']} 
                    password={os.environ['main_db_pw']} 
                    host={os.environ['main_db_host']} 
                    port={os.environ['main_db_port']} 
                    dbname={os.environ['main_db_name']}"""


if __name__ == "__main__":
    m = Machine(machine_id=1)
    print(m.environment)