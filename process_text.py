from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from collections import Counter
from nltk.stem import WordNetLemmatizer


def get_part_of_speech(word):
    """ finds the most probable part-of-speech of an English word to improve lemmatizer performance
    :param word: python string object containing English word
    :return: python string object containing part-of-speech of word
    """

    probable_part_of_speech = wordnet.synsets(word)

    pos_counts = Counter()

    pos_counts["n"] = len([item for item in probable_part_of_speech if item.pos() == "n"])
    pos_counts["v"] = len([item for item in probable_part_of_speech if item.pos() == "v"])
    pos_counts["a"] = len([item for item in probable_part_of_speech if item.pos() == "a"])
    pos_counts["r"] = len([item for item in probable_part_of_speech if item.pos() == "r"])

    most_likely_part_of_speech = pos_counts.most_common(1)[0][0]

    return most_likely_part_of_speech


def lemmatize_string(string):
    """ converts a string of words to a list of lemmatized words
    :param string: python string object containing words
    :return: tokenized and lemmatized list of words in string
    """

    string_lower = string.lower()
    tokenized_string = word_tokenize(string_lower)
    lemmatizer = WordNetLemmatizer()
    lemmatized_string = [lemmatizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized_string]

    return lemmatized_string
