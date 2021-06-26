import psycopg2
import os
import logging
from dotenv import load_dotenv
from pydantic import  BaseModel
from traceback import format_exc
from datetime import datetime
load_dotenv()

class EventActivity(BaseModel):
    event_name: str
    event_status: str
    event_message: str
    machine_id: int


    def insert_record(self):
        try:
            conn = psycopg2.connect(self._connection_string())
            cursor = conn.cursor()
            cmd = f"""insert into activity.events (
                        event_name,
                        event_status,
                        event_timestamp,
                        event_message,
                        machine_id
                        ) values (
                        '{self.event_name}',
                        '{self.event_status}',
                        '{datetime.utcnow()}',
                        '{self.event_message}',
                        {self.machine_id}
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
