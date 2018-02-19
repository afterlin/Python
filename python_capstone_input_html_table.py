
import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin as ujoin
from urllib.parse import urlparse as upar
from urllib.request import urlopen as uopen
from bs4 import BeautifulSoup as soup
import csv



# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# using Amazon with keyword of laptop
my_url = "https://vincentarelbundock.github.io/Rdatasets/datasets.html"

try:
# opening up connection
    uClient = uopen(my_url, context=ctx)
    page_html = uClient.read()
    if page_html.getcode() !=200:
        print("Error on page", page_html.getcode())
    uClient.close()

    #html = soup (page_html."html.parser")
except:
    print("Unable to retrieve or parse page")



outfile = open("out_file1.csv", "w", newline='')
writer = csv.writer(outfile)

tree = soup(page_html,"html.parser")
table_tag1 = tree.select("table")[0]
table_tag = table_tag1.select("table")[0]
#tab_data = [[item.text.strip() for item in row_data.select("th, td")]
#           for row_data in table_tag.select("tr")]

list_of_rows = []
for row in table_tag.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll(["th", "td"]):
        text = cell.text.strip()
        if text == "CSV":
            taga = cell.a  # when cell.text is CSV , get the Tag a in this cell
            csvlink = taga.get("href")  # get the content of href
            text = csvlink  # update the text to be the content of href
        if text == "DOC":
            taga= cell.a # when cell.text is DOC, get Tag a in this cell
            doclink = taga.get("href")
            text = doclink

        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)


for data in list_of_rows:
    #data = data.strip();
    writer.writerow(data)
    # print(' '.join(data))

outfile.close()


f = open("out_file1.csv", "r", newline='')
next(f,None)  # skip the header row
reader = csv.reader(f)

conn = sqlite3.connect('webfile.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS web_data''')

cur.execute('''CREATE TABLE IF NOT EXISTS web_data
    (ID INTEGER  PRIMARY KEY AUTOINCREMENT,Package TEXT , Item TEXT, Title TEXT,
     Rows INTEGER, Cols INTEGER, csv TEXT, doc TEXT)''')

for row in reader:
    cur.execute("INSERT INTO web_data(Package, Item,Title,Rows,Cols,csv, doc) VALUES(?,?,?,?,?,?,?)",row)


f.close()
conn.commit()
conn.close()



