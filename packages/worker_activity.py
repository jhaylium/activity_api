import psycopg2
import os
import logging
from dotenv import load_dotenv
from pydantic import  BaseModel
from traceback import format_exc
load_dotenv()

class WorkerActivity(BaseModel):
    worker_id:int
    status:str
    activity:str
    event_message:str


    def insert_record(self):
        try:
            conn = psycopg2.connect(self._connection_string())
            cursor = conn.cursor()
            cmd = f"""insert into worker_activty.events (
                        worker_id,
                        status,
                        activity,
                        event_message
                        ) values (
                        {self.worker_id},
                        {self.status},
                        {self.activity},
                        {self.event_message}
                        )               
                        """
            cursor.execute(cmd)
            conn.commit()
            cursor.close()
            conn.close()
            return 0
        except Exception:
            error_msg = format_exc()
            logging.error(f"{error_msg}")
            return -1

    def _connection_string(self):
        return f"""user={os.environ['main_db_user']} 
                    password={os.environ['main_db_pw']} 
                    host={os.environ['main_db_host']} 
                    port={os.environ['main_db_port']} 
                    dbname={os.environ['main_db_name']}"""
