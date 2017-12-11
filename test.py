import psycopg2
import csv

DB_NAME = 'buntu'
DB_ENDPOINT = 'localhost'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'root'
DB_PORT = 5432 


QUESTION="""cause ubuntu us upstart instead init different red hat get list runlevel 
number standing init 0 mean shutdown man init ca nt show list command man page cant print 
list thx"""

#ANS=official way use updatercd default setting usually 
# good updatercd bind9 default need explicitly chose startstop 
# runlevels updatercd bind9 start 19 3 5 stop 98 1 19 98 sequence 
# number determines startstop priority respectively 3 5 1 startstop runlevels 
# respectively runlevels exact numbering meaning found
def get_tags():
    conn = psycopg2.connect(host=DB_ENDPOINT, port=DB_PORT,
                                user=DB_USERNAME, password=DB_PASSWORD, dbname=DB_NAME)
    cur = conn.cursor()
    curins = conn.cursor()
    #sql="""select abody from postscleaned where qtags like '%services%'"""
    sql = "select qbody from postscleaned where qtags like '<runlevel>'"
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