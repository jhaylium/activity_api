import mailchimp_marketing
import os
import psycopg2
import logging
from traceback import format_exc
from dotenv import load_dotenv
from pydantic import  BaseModel
from typing import Optional
from mailchimp_marketing.api_client import ApiClientError




load_dotenv()

class Prospect(BaseModel):
    email: str = None
    name: str = None
    company: str = None
    title: str = None
    company_size: str = None
    list_name: str = None


def add_member_to_mailing_list():
    add_member_to_mailing_list()
    add_member_to_linkedin()


def add_member_to_mailing_list_chimp(email:str, list_id:str):
    try:
        client = mailchimp_marketing.Client()
        client.set_config({
            "api_key": os.environ['mail_chimp'],
            "server": "us1"
        })
        response = client.lists.add_list_member(list_id,
                                     {"email_address":email,
                                      "status": "pending"})
        return (0, response)
    except ApiClientError as error:

        return (-1, error.text)


def add_member_to_linkedin(body):
    cmd = f"""insert into prospects.linkedin_users (name, company,
            title, outreach_step, list_name) values (
            '{body['name']}',
            '{body['company']}',
            '{body['title']}',
            'not contacted',
            '{body['list_name']}'
            )"""
    conn = psycopg2.connect(connection_string())
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()
    return 0



def add_member_to_mailing_list_db(email):
    cmd = f"""insert into prospects.mailing_list (email) values (
            '{email}'
            )"""
    conn = psycopg2.connect(connection_string())
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()
    return 0


def get_prospects():
    pass


def get_mailing_list():
    cmd = f"""with base as (select * from prospects.mailing_list)
                    select to_jsonb(base.*) as jrow from base 
                    """
    conn = psycopg2.connect(connection_string())
    cursor = conn.cursor()
    cursor.execute(cmd)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_linkedin_prospects():
    try:
        cmd = f"""with base as (select * from prospects.linkedin_users)
                select to_jsonb(base.*) as jrow from base 
                """

        conn = psycopg2.connect(connection_string())
        cursor = conn.cursor()
        cursor.execute(cmd)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info("0 - List Retrieved")
        return data
    except Exception:
        logging.error(format_exc())
        return (-1, format_exc())


def connection_string():
    return f"""user={os.environ['main_db_user']} 
                password={os.environ['main_db_pw']} 
                host={os.environ['main_db_host']} 
                port={os.environ['main_db_port']} 
                dbname={os.environ['main_db_name']}"""
