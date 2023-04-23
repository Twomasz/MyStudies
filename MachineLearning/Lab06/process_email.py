#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import List
from nltk import PorterStemmer
from get_vocabulary_dict import get_vocabulary_dict


def process_email(email_contents: str) -> List[int]:
    """
    Pre-process the body of an email and return a list of indices of the
    words contained in the email.

    :param email_contents: the body of an email
    :return: a list of indices of the words contained in the email
    """

    # Load the vocabulary.
    vocabulary_dict = get_vocabulary_dict()

    # Initialize the return value.
    word_indices = list()

    # ========================== Preprocess Email ===========================

    # Find the Headers ( \n\n and remove )
    # Uncomment the following lines if you are working with raw emails with the
    # full headers

    # header_token = '\n\n'
    # header_start = email_contents.find(header_token)
    # email_contents = email_contents[header_start+len(header_token):]

    # Convert email content to lower case.
    email_contents = email_contents.lower()

    # Strip all HTML
    # Looks for any expression that starts with < and ends with > and replace
    # and does not have any < or > in the tag it with a space
    email_contents = re.sub(r'<[^<>]+>', ' ', email_contents)

    # Handle numbers.
    # Convert all sequences of digits (0-9) to a 'number' token.
    email_contents = re.sub(r'\d+', 'number', email_contents)

    # Handle URLs.
    # Convert all strings starting with http:// or https:// to a 'httpaddr' token.
    email_contents = re.sub(r'(http[s]?://\S+)', 'httpaddr', email_contents)

    # Handle email addresses.
    # Convert all strings with @ in the middle to a 'emailaddr' token.
    email_contents = re.sub(r'\S+\@\S+', 'emailaddr', email_contents)

    # Handle $ sign
    # Convert all sequences of $ signs to a 'dollar' token.
    email_contents = re.sub(r'\$+', 'dollar', email_contents)

    # ========================== Tokenize Email ===========================

    # Output the email to screen as well
    print('\n==== Processed Email ====\n\n')

    # Process file
    col = 0

    # Tokenize and also get rid of any punctuation
    tokens = re.split(r'[ @$/#.-:&*\+=\[\]?!\(\)\{\},''">_<;#\n\r]', email_contents)

    for token in tokens:

        # Remove any non-alphanumeric characters
        token = re.sub(r'[^a-zA-Z0-9]', '', token)

        # Stem the word
        token = PorterStemmer().stem(token.strip())

        # Skip the word if it is too short
        if len(token) < 1:
            continue

        # Look up the word in the dictionary and add to word_indices if found
        #
        # Instructions: Fill in this function to add the index of str to
        #               word_indices if it is in the vocabulary. At this point
        #               of the code, you have a stemmed word from the email in
        #               the variable str. You should look up str in the
        #               vocabulary list (vocabulary_dict). If a match exists, you
        #               should add the index of the word to the word_indices
        #               vector. Concretely, if str = 'action', then you should
        #               look up the vocabulary list to find where in vocabulary_dict
        #               'action' appears. For example, if vocabulary_dict{18} =
        #               'action', then, you should add 18 to the word_indices
        #               vector (e.g., word_indices = [word_indices ; 18]; ).
        #
        # Note: vocabulary_dict{idx} returns a word with index idx in the
        #       vocabulary list.
        #
        # Note: You can use strcmp(str1, str2) to compare two strings (str1 and
        #       str2). It will return 1 only if the two strings are equivalent.
        #
        # ========================== YOUR CODE HERE ======================

        for key in vocabulary_dict:
            if vocabulary_dict[key] == token:
                word_indices.append(key)

        # ========================= END OF YOUR CODE ==========================

        # Print to screen, ensuring that the output lines are not too long
        if (col + len(token) + 1) > 78:
            print('')
            col = 0
        print('{} '.format(token), end='', flush=True)
        col = col + len(tokens) + 1

    # Print footer
    print('\n\n=========================\n')

    return word_indices
