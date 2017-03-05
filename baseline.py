# This script attempts to answer the question:
#   For our training sets, how often do the tags appear inside the title or question?
# We cannot use traditional ML methods here because of the transfer learning required
import csv
import re
from pprint import pprint

STRIP_HTML_REGEX = re.compile('<.*?>')

# Have a map of filename:percent_tags_in_corpus
FILENAMES = {'biology.csv': 0.0, 'cooking.csv': 0.0, 'crypto.csv': 0.0, 'diy.csv': 0.0, 'robotics.csv': 0.0,
             'travel.csv': 0.0}

# Loop through every file
for filename in FILENAMES.keys():
    count_of_tags_in_corpus = 0
    total_tag_count = 0
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        # Loop through every row in the file
        # Convert to lowercase, split by ' ' to get a list of words
        for row in reader:
            row['title'] = row['title'].lower().split(' ')
            row['content'] = re.sub(STRIP_HTML_REGEX, "", row['content']).lower().split(' ')
            row['tags'] = row['tags'].lower().split(' ')
            # Count the number of total tags, and the number of words in title or content that also appear in a tag
            for tag in row['tags']:
                total_tag_count += 1
                if tag in row['title'] or tag in row['content']:
                    count_of_tags_in_corpus += 1

    # At this point we've read all the rows in a file, so let's save our output
    # Get the percentage and record it back into our dictionary
    FILENAMES[filename] = (float(count_of_tags_in_corpus) / float(total_tag_count)) * 100.0

# Print out our dictionary
pprint(FILENAMES, indent=True)

# Output
# {'biology.csv': 16.275770472999486,
#  'cooking.csv': 45.79370885149963,
#  'crypto.csv': 31.953382514518914,
#  'diy.csv': 43.22582827377429,
#  'robotics.csv': 37.193251533742334,
#  'travel.csv': 29.238987357271867}
# We can see 16.27% of biology questions have the tag appearing in the title or content
# We can see 43.25% of DIY questions have the tag appearing in the title or content
