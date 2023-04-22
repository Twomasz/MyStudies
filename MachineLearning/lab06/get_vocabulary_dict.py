#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from typing import Dict


def get_vocabulary_dict() -> Dict[int, str]:
    """
    Read the fixed vocabulary list from the datafile and return.
    :return: a dictionary of words mapped to their indexes
    """

    # - The file is saved in tab-separated values (TSV) format.
    # - Each line contains a word's ID and the word itself.
    # The output dictionary should map word's ID on the word itself, e.g.:
    #   {1: 'aa', 2: 'ab', ...}
    with open("data/vocab.txt") as file:
        tsv_file = csv.reader(file, delimiter="\t")

        vocab_dict = {int(line[0]): line[1] for line in tsv_file}

    return vocab_dict
