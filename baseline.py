# This script attempts to answer the question:
#   For our training sets, how often do the tags appear inside the title or question?
# We cannot use traditional ML methods here because of the transfer learning required
import csv
import re
from pprint import pprint
from itertools import combinations

STRIP_HTML_REGEX = re.compile('<.*?>')

# Have a map of filename:percent_tags_in_corpus
FILENAMES_PERCENT_MAPPING = {'biology.csv': 0.0, 'cooking.csv': 0.0, 'crypto.csv': 0.0, 'diy.csv': 0.0,
                             'robotics.csv': 0.0,
                             'travel.csv': 0.0}

FILENAMES_ALL_TAGS = {'biology.csv': set(), 'cooking.csv': set(), 'crypto.csv': set(), 'diy.csv': set(), 'robotics.csv': set(),
                      'travel.csv': set()}

# Loop through every file
for filename in FILENAMES_PERCENT_MAPPING.keys():
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
                FILENAMES_ALL_TAGS[filename].add(tag)  # add every tag to the set
                total_tag_count += 1
                if tag in row['title'] or tag in row['content']:
                    count_of_tags_in_corpus += 1

    # At this point we've read all the rows in a file, so let's save our output
    # Get the percentage and record it back into our dictionary
    FILENAMES_PERCENT_MAPPING[filename] = (float(count_of_tags_in_corpus) / float(total_tag_count)) * 100.0

# Print out our dictionary for percents
print ( "PERCENT OF TAGS APPEARING IN TITLE OR CONTENT BY FILE")
pprint(FILENAMES_PERCENT_MAPPING, indent=True)

# Output
# {'biology.csv': 16.275770472999486,
#  'cooking.csv': 45.79370885149963,
#  'crypto.csv': 31.953382514518914,
#  'diy.csv': 43.22582827377429,
#  'robotics.csv': 37.193251533742334,
#  'travel.csv': 29.238987357271867}
# We can see 16.27% of biology questions have the tag appearing in the title or content
# We can see 43.25% of DIY questions have the tag appearing in the title or content

# Print out tags via transfer learning
# Does cooking tags share anything with biology tags? And vice versa.
# To do this, we need all of the combinations of files in our list.
# E.g. we need to compare biology with everything else, cooking with everything else, etc.
filename_combinations_list = combinations(FILENAMES_ALL_TAGS.keys(), 2)
print( "filename1 : filename2: percent_shared1 : perecent_shared2")
# Loop through the different combinations and determine percentage of shared tags
for filename_one, filename_two in filename_combinations_list:
    set_intersection_size = len(FILENAMES_ALL_TAGS[filename_one].intersection(FILENAMES_ALL_TAGS[filename_two]))
    filename_one_tags_in_filename_two = float(set_intersection_size) / float(len(FILENAMES_ALL_TAGS[filename_one]))
    filename_two_tags_in_filename_one = float(set_intersection_size) / float(len(FILENAMES_ALL_TAGS[filename_two]))
    print( filename_one + " : " + filename_two + " : " + str(filename_two_tags_in_filename_one * 100.0) + " : " + str(filename_one_tags_in_filename_two * 100.0))


# Output
# filename1 : filename2: percent_shared1 : perecent_shared2
# diy.csv : biology.csv : 1.76991150442 : 1.6348773842
# diy.csv : robotics.csv : 7.79220779221 : 2.45231607629
# diy.csv : travel.csv : 1.21580547112 : 2.72479564033
# diy.csv : cooking.csv : 3.9402173913 : 3.95095367847
# diy.csv : crypto.csv : 0.765306122449 : 0.408719346049
# biology.csv : robotics.csv : 4.329004329 : 1.47492625369
# biology.csv : travel.csv : 1.21580547112 : 2.94985250737
# biology.csv : cooking.csv : 3.66847826087 : 3.98230088496
# biology.csv : crypto.csv : 2.29591836735 : 1.32743362832
# robotics.csv : travel.csv : 0.547112462006 : 3.8961038961
# robotics.csv : cooking.csv : 0.407608695652 : 1.2987012987
# robotics.csv : crypto.csv : 0.765306122449 : 1.2987012987
# travel.csv : cooking.csv : 2.03804347826 : 0.911854103343
# travel.csv : crypto.csv : 1.27551020408 : 0.303951367781
# cooking.csv : crypto.csv : 1.5306122449 : 0.815217391304
# We can see different files do not share much in terms of tags.