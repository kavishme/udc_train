from google.cloud import bigquery
import datetime
import os
import csv

client = bigquery.Client()

"""
Store posts to CSV files by tags
"""
def saveToCSV(result, filename="categories_data.csv"):
    try:
        outdir = "output_" + datetime.datetime.now().strftime('%Y%d%m%H%M')
        os.makedirs(outdir)

        header = ["id","title","question","tags","accepted_ans_id","answer_body"]
        # header.extend(tags)

        of = open(os.path.join(outdir, filename), 'w')
        wr = csv.writer(of, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        for que in result:
            wr.writerow(que)

        return outdir
    except Exception as err:
        print("ERR: ")
        print(err)

def main():
    client = bigquery.Client()
    query_job = client.query("""
        select q.id,q.title,q.body as question_body,q.tags ,q.accepted_answer_id,a.body as answer_body from 
        `bigquery-public-data.stackoverflow.posts_questions`  q 
        join `bigquery-public-data.stackoverflow.posts_answers` a on q.accepted_answer_id = a.id;""")

    results = query_job.result()
    # for row in results:
    #     print(row.id)
    saveToCSV(results)


main()




