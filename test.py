import psycopg2
import csv

DB_NAME = 'buntu'
DB_ENDPOINT = 'localhost'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'root'
DB_PORT = 5432 


QUESTION="""changed ubuntu theme day ago worked perfectly mediterranean something 
like gtk theme wanted change cursor theme worked well although make quite 
mess file icon folder also put icon theme worked restarted pc several day 
combination ambiance theme apps look like theme nautilus look like ambiance icon pack 
removed completely well mouse work tried logging back also restarting repair ubuntu theme"""


def get_tags():
    conn = psycopg2.connect(host=DB_ENDPOINT, port=DB_PORT,
                                user=DB_USERNAME, password=DB_PASSWORD, dbname=DB_NAME)
    cur = conn.cursor()
    curins = conn.cursor()
    sql="""select abody from postscleaned where qtags like '%icons%' or 
    qtags like 'themes' or qtags like '%icon-themes%'"""
    cur.execute(sql)
    result = cur.fetchone()
    f = open("answer.csv", "w")
    while(result):
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(result)
        print(result)
        result=cur.fetchone()
    f.close()


if __name__ == "__main__":
    get_tags()