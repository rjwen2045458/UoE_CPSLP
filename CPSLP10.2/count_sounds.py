#!/usr/bin/env python
# encoding: utf-8
"""
count_sounds.py

Created by Rob Clark on 2007-10-01.
Edited by Mark Sinclair 11-2015
Edited by Korin Richmond 10-2016 and 10-2017
Copyright (c) 2007-2017 CSTR All rights reserved.
"""

import re
import words2

r = re.compile(r'^(.*):.*:.*:.*{(.*)}.*:.*:.*')


def load_dictionary(filename):
    d = {}
    with open(filename, 'r') as f:
        for entry in f:
            m = r.match(entry)
            d[m.group(1)] = m.group(2).split()
    return d


def count_words_in_file(filename, lexdict):
    words_found = {}
    words_not_in_dictionary = []
    with open(filename, 'r') as f:
        for line in f:
            for w in line.split():
                try:
                    t = re.search('\w+-?\w*', w).group()
                    tl = t.lower()
                    # p = lexdict[w]
                    p = lexdict[tl]
                    try:
                        # words_found[w].increment_count()
                        words_found[t].increment_count()
                    except KeyError:
                        # words_found[w] = words2.Word(w, p)
                        words_found[t] = words2.Word(t, p)
                except KeyError:
                    # words_not_in_dictionary.append(w)
                    words_not_in_dictionary.append(t)
                    # print("Word not in dictionary: {0}".format(w))
    print("Words no in dictionary: ", words_not_in_dictionary)
    return words_found


def count_sounds(words_dict):
    sounds = {}
    for entry in words_dict.values():
        for symbol in entry.get_pronunciation():
            try:
                sounds[symbol] += entry.get_count()
            except KeyError:
                sounds[symbol] = entry.get_count()
    return sounds

def main():
    print("Loading dicitionary...")
    lexdict = load_dictionary("dictionary.txt")
    print("  loaded {0} words from lexicon file dictionary.txt".format(len(lexdict)))

    print("Parsing file...")
    words_in_file = count_words_in_file("scotland.txt", lexdict)
    print("   found {0} unique words".format(len(words_in_file)))

    sounds = count_sounds(words_in_file)
    print(sounds)

if __name__ == '__main__':
    main()
