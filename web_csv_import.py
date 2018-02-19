import csv
import requests
from contextlib import closing
import codecs
import sqlite3

def copy_web_csv(url, type2):
    
    url_name = url.split('/')[-1]
    table_name = type2 + '_' + url_name

    outfile = open(table_name, "w", newline='')
    writer = csv.writer(outfile)

    with closing(requests.get(url, stream=True)) as r:
        reader = csv.reader(codecs.iterdecode(r.iter_lines(),'utf-8'), delimiter=',', quotechar='"')
        for row in reader:
            writer.writerow(row)

    outfile.close()


conn = sqlite3.connect('webfile.sqlite')
cur = conn.cursor()

cur.execute('''SELECT CSV, PACKAGE FROM web_data WHERE UPPER(ITEM) LIKE '%TITANIC%' ''')

for curone in cur:  # loop to get each record, otherwise, cur.fetchone() to get just ONE record;
    row = curone[0]
    rtype = curone[1]

    copy_web_csv(row,rtype)
