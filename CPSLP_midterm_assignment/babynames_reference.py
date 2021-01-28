# -*- coding: utf-8 -*-
# Copyright 2019 Korin Richmond

import re
from operator import itemgetter
from collections import defaultdict, Counter


class Babies:
    """A class for parsing text files with babyname data, and then computing various statistics using the data."""

    gmap = {'BOY': 0, 'GIRL': 1, 'M': 0, 'F': 1}  # handy gender map (name -> list index)

    # the regexp for parsing a name origin text file
    origin_pat = re.compile(r'^\s*(?P<name>[\s\w\'-]+)\ {3}'
                            r'(?P<sex>[FM])\s+'
                            r'(?P<origin>[^,]+),',
                            re.VERBOSE)

    def __init__(self, filepath):
        """Constructor takes FILEPATH - the path to a *babies.txt data file."""
        self.names = defaultdict(lambda: [0, 0])  # (counts for [BOYs, GIRLs]) - filled by read_names_from_file
        self.origins = defaultdict(lambda: [[], []])  # (origins for [BOYs,GIRLs]) - filled by read_origins_from_file
        self.read_names_from_file(filepath)

    def read_names_from_file(self, filepath):
        """Read data from a textfile at FILEPATH, having line format '<baby with name>  <gender = 'BOY' or 'GIRL'>."""
        with open(filepath, 'r') as datafile:
            for line in datafile:
                name, gender = line.split()
                self.names[name][self.gmap[gender]] += 1

    def read_origins_from_file(self, filepath):
        """Read data from a textfile at FILEPATH, containing information on genders and origins for names"""
        with open(filepath, 'r') as f:
            for line in f:
                mo = self.origin_pat.search(line)
                (name, origin, gender_index) = (mo['name'], mo['origin'], self.gmap[mo['sex']])
                self.origins[name][gender_index].append(origin)

    def get_origin_counts(self, use_gender=False):
        """Return a list of tuples of name origins (e.g. 'Welsh', 'German' etc.) and the count of babies born with each.

        Set USE_GENDER to True or False (default) to take gender of babies born into account when
        estimating the counts (people variously choose to do either, so need both answers to check!)."""
        counts = Counter()
        for name, ncount in self.names.items():
            try:
                origins = self.origins[name]
            except KeyError:
                continue

            if use_gender:
                for gender_ind, origins_for_gender in enumerate(origins):
                    for origin in origins_for_gender:
                        counts[origin] += ncount[gender_ind]
            else:
                for o in origins[0] + origins[1]:
                    counts[o] += sum(ncount)

        return sorted(counts.items(), reverse=True, key=itemgetter(1))

    def get_total_births(self, gender=None):
        """Return the total count of babies born.  GENDER can be 'BOY', 'GIRL' or None (default, gives total baby count)."""
        self._validate_gender(gender)
        gender_totals = self.get_gender_totals()
        if gender is not None:
            return gender_totals[self.gmap[gender]]
        else:
            return sum(gender_totals)

    def get_gender_ratio(self, gender):
        """Return proportion of boy or girl babies born.  GENDER must be 'BOY' or 'GIRL'."""
        self._validate_gender(gender, allow_none=False)

        totals = self.get_gender_totals()

        return totals[self.gmap[gender]] / sum(totals)

    def get_gender_totals(self):
        """Return a list of total boy and girl baby births (i.e. [num_boys, num_girls])."""
        return [sum(gender_count) for gender_count in zip(*self.names.values())]

    def get_names_beginning_with(self, first_char, gender=None):
        """Return a list of names given to babies beginning with letter FIRST_CHAR.
        GENDER can be 'BOY', 'GIRL' or None (default, whereby both boy and girl names are included)."""
        self._validate_gender(gender)
        self._validate_single_char(first_char)

        first_char = first_char.lower()
        if gender is None:
            names = [k for k, v in self.names.items()
                     if k[0].lower() == first_char and sum(v) > 0]
        else:
            gender_ind = self.gmap[gender]  # only need to look this up once
            names = [k for k, v in self.names.items()
                     if k[0].lower() == first_char and v[gender_ind] > 0]
        names.sort()
        return names

    def get_top_N(self, N, gender=None):
        """Return a list of tuples of names and their respective counts, sorted by descending count.
        Parameter N specifies the number of most popular names to include in the list.
        Parameter GENDER can be 'BOY', 'GIRL' or None (default=include both boy and girl names)."""
        self._validate_gender(gender)
        self._validate_pos_int(N)

        if gender is None:
            count_list = [(k, sum(v)) for k, v in self.names.items()]
        else:
            gender_ind = self.gmap[gender]  # only need to look this up once
            count_list = [(k, v[gender_ind]) for k, v in self.names.items()]

        count_list.sort(reverse=True, key=itemgetter(1))

        return count_list[:N]


    #  a few private utility functions below to keep the code above uncluttered
    def _validate_gender(self, gender, allow_none=True):
        if not ((gender is None and allow_none) or (gender in self.gmap)):
            raise ValueError("gender {0} is not valid".format(str(gender)))

    def _validate_pos_int(self, N):
        if not isinstance(N, int):
            raise TypeError('N must be a positive integer value')
        if N <= 0:
            raise ValueError('N must be a positive integer value')

    def _validate_single_char(self, s):
        if not isinstance(s, str):
            raise TypeError('Argument must be a string')
        if len(s) != 1:
            raise ValueError('Argument must be a single character string')


if __name__ == "__main__":

    # Just a few timing tests, just for interest...
    import timeit

    setup = 'from __main__ import Babies; from operator import itemgetter; B=Babies("test/scotbabies2015.txt")'

    tests = [
        'B.get_total_births()',
        'B.get_total_births("BOY")',
        'B.get_names_beginning_with("K")',
        'B.get_top_N(20, "GIRL")',
        ]

    for test in tests:
        t = timeit.timeit(test, setup=setup, number=100)
        print(f'Time to run {test} => {t:.3f} seconds\n')
