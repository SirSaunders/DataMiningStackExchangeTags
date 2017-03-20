import csv
import nltk


# nltk.download() #or got to http://www.nltk.org/data.html

def get_cvs_data(file_location):
    with open(file_location, encoding="utf8") as infile:
        reader = csv.reader(infile)
        columns = [[], [], []]
        first_skipped = False
        for rows in reader:
            if not first_skipped:
                first_skipped = True
            else:
                title = rows[1]
                taggedTitle = nltk.pos_tag(nltk.word_tokenize(title))
                content = rows[2].replace("</p>", "").replace("<p>", "")  # I removed the  <p> </p> html tags
                taggedContent = nltk.pos_tag(nltk.word_tokenize(content))
                tags = rows[3]
                taggedTags = nltk.pos_tag(nltk.word_tokenize(tags))

                columns[0].append([title, taggedTitle])
                columns[1].append([content, taggedContent])
                columns[2].append([tags, taggedTags])
    print("example")
    print("title:")
    print(columns[0][0][0])
    print("content: ")
    print(columns[1][0][0])
    print("Tag: ")
    print(columns[2][0][0])
    return columns


# returns a matrix with all the training data in it example get_training_data_matrix()[0][0][0] should get you the
# first training files first title the first [index] is what training set the second [index] is what row in that
# training set the third [index] is the column in that training set
# the fourth index is whether you want just the text [0] or the array  of text with NLTK tags [1]
def get_training_data_matrix():
    training_data = [get_cvs_data('robotics.csv'), get_cvs_data('biology.csv'), get_cvs_data('cooking.csv'),
                     get_cvs_data('crypto.csv'), get_cvs_data('robotics.csv')]

    return training_data


# this takes a several of minutes to read in
print(get_training_data_matrix()[0][0][0][0])
