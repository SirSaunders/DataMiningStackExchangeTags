import nltk as nltk
from nltk.corpus import wordnet as wn
import csv

with open('D:/Files/Downloads/biology.csv', encoding="utf8") as infile:
    reader = csv.reader(infile)
    columns = [[], [], []]
    firstSkipped = False
    for rows in reader:
        if not firstSkipped:
            firstSkipped = True
        else:
            title = rows[1]
            content = rows[2].replace("</p>", "").replace("<p>", "")  # I removed the  <p> </p> html tags
            tags = rows[3]
            columns[0].append(title)
            columns[1].append(content)
            columns[2].append(tags)
print("example")
print("title: " + columns[0][0])
print("content: " + columns[1][0])
print("Tag: " + columns[2][0])


