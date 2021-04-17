import nltk
import sys
import os
import string
import math
from heapq import nlargest

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    loop = True
    while loop:
        # Prompt user for query
        query = set(tokenize(input("Query: ")))
        if 'stop' in query:
            break

        # Determine top file matches according to TF-IDF
        filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

        # Extract sentences from top files
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens

        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)

        # Determine top sentence matches
        matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        for match in matches:
            print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary = {}
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            key = file.replace(".txt", "")
            with open(directory + os.sep + file) as txtFile:
                text = txtFile.read()
                dictionary[key] = text
    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    lower = document.lower()
    list = nltk.word_tokenize(lower)
    for word in list.copy():
        if word in nltk.corpus.stopwords.words("english") or word[0] in string.punctuation:
            list.remove(word)
    return list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dictionary = {}

    for document in documents:
        words = set(documents[document])
        for word in words:
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1

    total = len(documents)

    for word in dictionary:
        dictionary[word] = math.log(total / dictionary[word])

    return dictionary


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    dictionary = {}

    for file in files:
        sum = 0
        for word in query:
            if word in idfs:
                sum += idfs[word] * files[file].count(word)
        dictionary[file] = sum

    return nlargest(n, dictionary, key=dictionary.get)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    dictionary = {}
    for sentence in sentences:
        score = 0
        for word in query:
            if word in sentences[sentence]:
                score += idfs[word]
        dictionary[sentence] = score

    return nlargest(n, dictionary, key=dictionary.get)


if __name__ == "__main__":
    main()
