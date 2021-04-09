import psycopg2
import os
import logging
from dotenv import load_dotenv
from traceback import format_exc
from pydantic import BaseModel

load_dotenv()

class WebActivity(BaseModel):
    user_id:int
    event_status:str
    activity:str
    event_message:str
    machine_id:int

    def insert_record(self):
        try:
            conn = psycopg2.connect(self._connection_string())
            cursor = conn.cursor()
            logging.info(f"Insert Event | User: {self.user_id} | Activity: {self.activity}")
            cmd = f"""insert into web_activity.events (user_id,
                    event_status,
                    activity,
                    event_message,
                    machine_id)
                    values (
                    {self.user_id},
                    '{self.event_status}',
                    '{self.activity}',
                    '{self.event_message}',
                    {self.machine_id}
                    )"""
            cursor.execute(cmd)
            conn.commit()
            logging.info(f"Record Created")
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
