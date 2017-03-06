
import csv


def get_cvs_data(file_location):
    with open(file_location, encoding="utf8") as infile:
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
    return columns

# returns a matrix with all the training data in it
# example get_training_data_matrix()[0][0][0] should get you the first training files first title
# the first [index] is what training set the second [index] is what row in that training set the third [index] is the colum in that training set
def get_training_data_matrix():
    training_data = []
    training_data.append(get_cvs_data('robotics.csv'))
    training_data.append(get_cvs_data('biology.csv'))
    training_data.append(get_cvs_data('cooking.csv'))
    training_data.append(get_cvs_data('crypto.csv'))
    training_data.append(get_cvs_data('robotics.csv'))

    return training_data


print(get_training_data_matrix()[0][0][0])
