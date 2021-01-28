"""A suite of unittests for testing an implementation of the babynames.Babies class"""

import babynames_reference  # the reference implementation - provides correct answers
import babynames
import unittest

maxtime = 10.0

constructorWorks = None
A = None


def setup_module():
    """ setup any state specific to the execution of the given module."""
    global constructorWorks
    global A
    try:
        A = babynames.Babies("scotbabies2015.txt")
        constructorWorks = True
    except TypeError:
        # most likely the constructor args have not been observed correctly
        constructorWorks = False


class TestBabynames(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.ref_code = babynames_reference.Babies("scotbabies2015.txt")
        cls.student_code = A
        cls.constructorWorks = constructorWorks

    def test_constructor(self):
        """Can we create an instance of the Babies class correctly?"""
        self.assertTrue(self.constructorWorks)

    def test_totals_none(self):
        """Does the Babies instance compute the total number of births correctly?"""
        self.assertEqual(self.student_code.get_total_births(), self.ref_code.get_total_births())

    def test_totals_boy(self):
        """Does the Babies instance compute the total number of boy births correctly?"""
        self.assertEqual(self.student_code.get_total_births(gender="BOY"), self.ref_code.get_total_births(gender="BOY"))

    def test_totals_girl(self):
        """Does the Babies instance compute the total number of girl births correctly?"""
        self.assertEqual(self.student_code.get_total_births(gender="GIRL"), self.ref_code.get_total_births(gender="GIRL"))

    def test_begwith_none_lower(self):
        """Does the Babies instance return a list of babies with names beginning with
        a given lower case character correctly?"""
        self.assertSequenceEqual(self.student_code.get_names_beginning_with('k'),
                                 self.ref_code.get_names_beginning_with('k'))

    def test_begwith_none_upper(self):
        """Does the Babies instance return a list of babies with names beginning with
        a given upper case character correctly?"""
        self.assertSequenceEqual(self.student_code.get_names_beginning_with('K'),
                                 self.ref_code.get_names_beginning_with('K'))

    def test_begwith_boy_upper(self):
        """Does the Babies instance return the list of all boy babies with names beginning with
        a given upper case character correctly?"""
        self.assertSequenceEqual(self.student_code.get_names_beginning_with('K', 'BOY'),
                                 self.ref_code.get_names_beginning_with('K', 'BOY'))

    def test_begwith_girl_upper(self):
        """Does the Babies instance return the list of all girl babies with names beginning with
        a given upper case character correctly?"""
        self.assertSequenceEqual(self.student_code.get_names_beginning_with('K', 'GIRL'),
                                 self.ref_code.get_names_beginning_with('K', 'GIRL'))

    def test_topN_none(self):
        """Does the Babies instance return the list of top 5 baby names correctly?"""
        self.assertSequenceEqual(self.student_code.get_top_N(5), self.ref_code.get_top_N(5))

    def test_topN_boy(self):
        """Does the Babies instance return the list of top 5 boy baby names correctly?"""
        self.assertSequenceEqual(self.student_code.get_top_N(5, 'BOY'), self.ref_code.get_top_N(5, 'BOY'))

    def test_topN_girl(self):
        """Does the Babies instance return the list of top 5 girl baby names correctly?"""
        self.assertSequenceEqual(self.student_code.get_top_N(5, 'GIRL'), self.ref_code.get_top_N(5, 'GIRL'))

    def test_ratio_boy(self):
        """Does the Babies instance return the proportion of boy babies correctly?"""
        self.assertEqual(self.student_code.get_gender_ratio("BOY"), self.ref_code.get_gender_ratio("BOY"))

    def test_ratio_girl(self):
        """Does the Babies instance return the proportion of girl babies correctly?"""
        self.assertEqual(self.student_code.get_gender_ratio("GIRL"), self.ref_code.get_gender_ratio("GIRL"))

    def test_begwith_wrongin_kwargs_int(self):
        """Does the Babies instance raise the correct exception for a "first_char" argument of the wrong type?"""
        self.assertRaises(TypeError, self.student_code.get_names_beginning_with, **{"first_char": 1})

    def test_begwith_wrongin_kwargs_longstring(self):
        """Does the Babies instance raise the correct exception for an long string "first_char" argument?"""
        self.assertRaises(ValueError, self.student_code.get_names_beginning_with, **{"first_char": "ABC"})

    def test_topN_wrongin_kwargs_zero(self):
        """Does the Babies instance raise the correct exception for a zero int "topN" argument?"""
        self.assertRaises(ValueError, self.student_code.get_top_N, **{"N": 0})

    def test_topN_wrongin_kwargs_negint(self):
        """Does the Babies instance raise the correct exception for a negative int "topN" argument?"""
        self.assertRaises(ValueError, self.student_code.get_top_N, **{"N": -1})

    def test_topN_wrongin_kwargs_float(self):
        """Does the Babies instance raise the correct exception for a non-int "topN" argument?"""
        self.assertRaises(TypeError, self.student_code.get_top_N, **{"N": 1.5})

    def test_topN_wrongin_kwargs_gender(self):
        """Does the Babies instance raise the correct exception for an incorrect "topN" gender argument?"""
        self.assertRaises(ValueError, self.student_code.get_top_N, **{"N": 10, "gender": "ABC"})

    def test_begwith_wrongin_kwargs_gender(self):
        """Does the Babies instance raise the correct exception for an incorrect
        "get_names_beginning_with" gender argument?"""
        self.assertRaises(ValueError, self.student_code.get_names_beginning_with, **{"first_char": "A", "gender": "ABC"})

    def test_totals_wrongin_kwargs_gender(self):
        """Does the Babies instance raise the correct exception for an incorrect "get_total_births" gender argument?"""
        self.assertRaises(ValueError, self.student_code.get_total_births, **{"gender": "ABC"})

    def test_ratio_wrongin_kwargs_gender(self):
        """Does the Babies instance raise the correct exception for an incorrect "get_gender_ratio" gender argument?"""
        self.assertRaises(ValueError, self.student_code.get_gender_ratio, **{"gender": "ABC"})

    def test_begwith_wrongin_posargs_int(self):
        """Does the Babies instance raise the correct exception for a positional argument of incorrect type passed
         to the "get_names_beginning_with" method?"""
        self.assertRaises(TypeError, self.student_code.get_names_beginning_with, *[1])

    def test_begwith_wrongin_posargs_longstring(self):
        """Does the Babies instance raise the correct exception for a positional argument of incorrect value passed
        to the "get_names_beginning_with" method?"""
        self.assertRaises(ValueError, self.student_code.get_names_beginning_with, *["ABC"])

    def test_topN_wrongin_posargs_zero(self):
        """Does the Babies instance raise the correct exception for a positional argument of 0 passed
        to the "get_top_N" method?"""
        self.assertRaises(ValueError, self.student_code.get_top_N, *[0])

    def test_topN_wrongin_posargs_negint(self):
        """Does the Babies instance raise the correct exception for a positional argument of -1 passed
        to the "get_top_N" method?"""
        self.assertRaises(ValueError, self.student_code.get_top_N, *[-1])

    def test_topN_wrongin_posargs_float(self):
        """Does the Babies instance raise the correct exception for a positional argument of a non-integer passed
        to the "get_top_N" method?"""
        self.assertRaises(TypeError, self.student_code.get_top_N, *[1.5])

    def test_topN_wrongin_posargs_gender(self):
        """Does the Babies instance raise the correct exception for a positional argument of a non-gender passed
        to the "get_top_N" method?"""
        self.assertRaises(ValueError, self.student_code.get_top_N, *[10, "ABC"])

    def test_begwith_wrongin_posargs_gender(self):
        """Does the Babies instance raise the correct exception for a positional argument of a non-gender passed
        to the "get_names_beginning_with" method?"""
        self.assertRaises(ValueError, self.student_code.get_names_beginning_with, *["A", "ABC"])

    def test_totals_wrongin_posargs_gender(self):
        """Does the Babies instance raise the correct exception for a positional argument of a non-gender passed
        to the "get_total_births" method?"""
        self.assertRaises(ValueError, self.student_code.get_total_births, *["ABC"])

    def test_ratio_wrongin_posargs_gender(self):
        """Does the Babies instance raise the correct exception for a positional argument of a non-gender passed
        to the "get_gender_ratio" method?"""
        self.assertRaises(ValueError, self.student_code.get_gender_ratio, *["ABC"])

    def test_origins(self):
        """Does the Babies instance compute the correct origin counts?
        Note: by default we assume gender has not been taken into account.  However, if that fails, we
        also try testing it when taking gender into account to see whether that passes instead."""
        self.student_code.read_origins_from_file('./namesdb.txt')
        self.ref_code.read_origins_from_file('./namesdb.txt')

        testcode_answer = self.student_code.get_origin_counts()

        # first try not taking gender into account (most likely)
        err = []
        try:
            self.assertSequenceEqual(testcode_answer, self.ref_code.get_origin_counts())
        except AssertionError as e:
            err.append(e)
            pass

        # if that didn't fly, then try again, taking gender into account this time
        if err:
            self.assertSequenceEqual(testcode_answer, self.ref_code.get_origin_counts(True))

    # def test_origins_usegender(self):
    #     self.student_code.read_origins_from_file('./namesdb.txt')
    #     self.ref_code.read_origins_from_file('./namesdb.txt')
    #     self.assertSequenceEqual(self.student_code.get_origin_counts(), self.ref_code.get_origin_counts(True))
