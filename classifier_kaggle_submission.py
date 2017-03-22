# Classifier for submitting to kaggle
# Created file submission.csv
# Based on what we have learned in baseline.py, there is almost nothing useful is training
# This is not even really an ML or data mining problem, it's weird why it's hosted on Kaggle
import nltk
import csv
import re
import random
import collections
import io

# Load the tagger in RAM
# Every time pos_tag is called, NLTK unpickels from disk, which is so ungodly slow
# This trick will add a few seconds to startup, but is obviously well worth it to amortize this
# Credit to: http://stackoverflow.com/questions/11610076/slow-performance-of-pos-tagging-can-i-do-some-kind-of-pre-warming
# In fact, NLTK is notorious for having the slowest damn POS tagger around
from nltk.tag.perceptron import PerceptronTagger

TAGGER = PerceptronTagger()

STRIP_HTML_REGEX = re.compile('<.*?>')
FILENAME_TO_READ = 'test.csv'
FILENAME_TO_WRITE = 'submission.csv'
STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
STOP_WORDS.update(
    ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
POS_TO_KEEP = set(["NNS", "NN"])  # keep plural nouns and possessive nouns
CSV_FILE_HEADER = ["id", "tags"]


def get_tags(title_str, content_str):
    """Given the title and content, return the tags as a list.
       Does a few interesting things:
       1. Removes HTML using a regex
       2. Removes stop words
       3. Remove words that aren't nouns
       4. Nouns appearing more than once will be tags
       5. If no nouns appear more than once, pick two at random
    """
    # Remove HTML using a regex
    title_str = re.sub(STRIP_HTML_REGEX, "", title_str).lower()
    content_str = re.sub(STRIP_HTML_REGEX, "", content_str).lower()

    # Decode UTF-8
    title_str = title_str.decode('utf-8')
    content_str = content_str.decode('utf-8')

    # Generate a list of tokens
    title_tokens = nltk.word_tokenize(title_str)
    content_tokens = nltk.word_tokenize(content_str)

    # Remove stop words or words < 3 length
    title_tokens = [word for word in title_tokens if word not in STOP_WORDS and len(word) >= 3]
    content_tokens = [word for word in content_tokens if word not in STOP_WORDS and len(word) >= 3]

    # Get Part of Speech
    title_pos = TAGGER.tag(title_tokens)
    content_pos = TAGGER.tag(content_tokens)

    tags_based_on_part_of_speech = collections.Counter()  # Counter of <word, count>
    for word, part_of_speech in title_pos + content_pos:
        # If the word is a noun, keep it
        if part_of_speech in POS_TO_KEEP:
            # Update our dictionary that shows <word, count>
            if word in tags_based_on_part_of_speech:
                tags_based_on_part_of_speech[word] += 1
            else:
                tags_based_on_part_of_speech[word] = 1

    # We have a list of POSSIBLE tags in the tags_based_on_part_of_speech with a count.
    # Let's get the most common 3 or 4 possible tags. How many we pick is going to be random.
    num_tags_to_keep_max = random.choice([3, 4])
    most_common_tags = tags_based_on_part_of_speech.most_common(num_tags_to_keep_max)

    # Now we have a list of the 3 or 4 most common tags. Let's remove all words with frequencies of 1 (they are poor tags)
    tags_to_keep = set()  # use a set to prevent any duplicates
    for word, freq in most_common_tags:
        if freq > 1:
            tags_to_keep.add(word)

    if len(tags_to_keep) == 0:
        # We have no tags occurring at greater than 1 frequency, so pick two at random
        tags_to_keep.add(random.choice(most_common_tags)[0])
        tags_to_keep.add(random.choice(most_common_tags)[0])

    return list(tags_to_keep)


with open(FILENAME_TO_READ, 'r') as csv_file_to_read:
    with open(FILENAME_TO_WRITE, 'wb') as csv_file_to_write:
        reader = csv.DictReader(csv_file_to_read)
        writer = csv.DictWriter(csv_file_to_write, fieldnames=CSV_FILE_HEADER, delimiter=',')
        writer.writeheader()
        # Loop through every row in the file
        # Convert to lowercase, split by ' ' to get a list of words
        for row in reader:
            new_row = dict()
            new_row['id'] = row['id']
            new_row['tags'] = ' '.join(get_tags(row['title'], row['content'])).encode('utf-8').strip()
            writer.writerow(new_row)
