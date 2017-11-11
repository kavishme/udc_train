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

"""
Return dictionary of tags - posts
"""
def getPostsByTags():
    try:
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
        while(result):
            for tag in getTags(result[0]):
                if tag not in postsByTags:
                    postsByTags[tag] = []
                postsByTags[tag].append(result[1] + ' ' + result[2])

            print(result[0])
            result = cur.fetchone()
        
        return postsByTags
    except Exception as err:
        print("ERR: ")
        print(err)


"""
Store posts to CSV files by tags
"""
def saveToCSV(postByQues, tags, filename="categories_data.csv"):
    try:
        outdir = "output_" + datetime.datetime.now().strftime('%Y%d%m%H%M')
        os.makedirs(outdir)

        header=["question"]
        header.extend(tags)

        of = open(os.path.join(outdir, filename), 'w')
        wr = csv.writer(of, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        
        for que in postByQues:
            data = [que]
            data.extend(postByQues[que])
            wr.writerow(data)
        
        return outdir
    except Exception as err:
        print("ERR: ")
        print(err)


def tagsWithMinQues(posts, min_ques, max_other, max_ques_len):
    p = {}
    p["others"] = []
    for tag in posts:
        if max_ques_len > 0:
            questions = [' '.join(q.split()[:max_ques_len]) for q in posts[tag]]
        else:
            questions = posts[tag]

        if len(posts[tag]) < min_ques:
            p["others"].extend(questions)
        else:
            p[tag] = questions
    
    if len(p["others"]) > max_other:
        p["others"] = random.sample(p["others"], k=max_other)
    
    return p

def toColumns(p):
    ques = {}
    tags = list(p.keys())

    for tag in tags:
        for q in p[tag]:
            
            if q not in ques:
                ques[q] = [0]*len(tags)

            i = tags.index(tag)
            ques[q][i] = 1
    
    return ques, tags


# def cat_count(posts):
#     filepath = "cat_count.csv"
#     f = open(filepath, 'w')
#     t = []

#     for p in posts:
#         t.append( (p,len(posts[p])) )
#     t = sorted(t, key=lambda lts: lts[1])
#     wr = csv.writer(f, quoting=csv.QUOTE_ALL)
#     wr.writerows(t)
#     f.close()

if __name__ == "__main__":
    # get data in {tag:[questions]}
    p = getPostsByTags()

    # File already created, not required to do again
    # cat_count(p)    
    
    # filter by number of questions and put all else under "other" tag
    # tagsWithMinQues(postsData, min_ques_per_tag, max_other_ques, max_ques_len)
    p = tagsWithMinQues(p, 1000, 6000, 160)

    # convert {tag:[questions]} to {ques:[0,1,0,0,0,1...]} format
    p, tags = toColumns(p)

    saveToCSV(p, tags)
