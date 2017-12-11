import psycopg2
import re
import os
import datetime
import csv
import random
import copy
import json

DB_NAME = 'buntu'
DB_ENDPOINT = 'localhost'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'root'
DB_PORT = 5432  # default port

regex = re.compile('<([\w\.\-\_\s]+)>')

"""
Returns list of tags parsed from tag string.
"""


def getTags(text):
    return regex.findall(text.lower())

def getPostsByTags():
    try:
        outdir = "output_" + datetime.datetime.now().strftime('%Y%d%m%H%M')
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        postsByTags = {}
        conn = psycopg2.connect(host=DB_ENDPOINT, port=DB_PORT,
                                user=DB_USERNAME, password=DB_PASSWORD, dbname=DB_NAME)
        cur = conn.cursor()
        curins = conn.cursor()

        sql = """
            SELECT qtags, qtitle, qbody
            FROM postscleaned;
         """
        cur.execute(sql)
        result = cur.fetchone()
        labels = set()
        number = 1
        while(result):
            labof = open(os.path.join(outdir, str(number) + '.lab'), 'w')
            txtof = open(os.path.join(outdir, str(number) + '.txt'), 'w')
            labs = getTags(result[0])
            print(labs)
            labof.writelines("%s\n" % l for l in labs)
            txtof.write(result[1] + ' ' + result[2])
            labof.close()
            txtof.close()
            labels.update(labs)
            result = cur.fetchone()
            number = number + 1

        labof = open(os.path.join(outdir, 'askubuntu.labels'), 'w')
        labof.writelines("%s\n" % l for l in labels)
        labof.close()

    except Exception as err:
        print("ERR: ")
        print(err)


if __name__ == "__main__":
    getPostsByTags()
