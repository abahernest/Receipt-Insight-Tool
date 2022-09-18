from django.test import TestCase
import json
# import unittest
from .views import ReceiptView

ReceiptView = ReceiptView()

class FindColumnAxes (TestCase):
    def test_should_return_correct_start_and_end_col_index(self):
        input_word = "    sample text  "
        output = {"start":4,"end":14}
        self.assertEqual(ReceiptView.find_axes(input_word), output)

    def test_should_parse_word_containing_type1_newline_character(self):
        input_word = "    sample text\n"
        output = {"start": 4, "end": 14}
        self.assertEqual(ReceiptView.find_axes(input_word), output)

    def test_should_parse_word_containing_type2_newline_character(self):
        input_word = "    sample text\r"
        output = {"start": 4, "end": 14}
        self.assertEqual(ReceiptView.find_axes(input_word), output)

    def test_should_parse_word_containing_type3_newline_character(self):
        input_word = "    sample text\r\n"
        output = {"start": 4, "end": 14}
        self.assertEqual(ReceiptView.find_axes(input_word), output)

    def test_should_parse_word_space_after_newline_character(self):
        input_word = "    sample text  \n"
        output = {"start": 4, "end": 14}
        self.assertEqual(ReceiptView.find_axes(input_word), output)


class ContainsDelimiter (TestCase):
    delimiters = []
    def setup(self):
        self.delimiters = [
            {
                "value":json.dumps("-"),
                "count":3
            },
            {
                "value": json.dumps("#"),
                "count": 3
            }
        ]
        """All variations of Newline characters are default delimiters.
        'count' is the minimum value for a delimiter below which it will not be seen as a delimiter
        if 'value' is '#' and 'count' is 3, then ## isnt a delimiter, onlyy ### and above
        """
    def test_should_return_True_if_contains_default_delimiter(self):
        input_word1 = "\n"
        input_word2 = "\r\n"
        input_word3 = "\r"
        self.assertEqual(ReceiptView.contains_delimeter(input_word1,self.delimiters), True)
        self.assertEqual(ReceiptView.contains_delimeter(input_word2,self.delimiters), True)
        self.assertEqual(ReceiptView.contains_delimeter(input_word3,self.delimiters), True)

    def test_should_return_False_if_delimiter_not_found(self):
        input_word1 = "  simply sucre"
        input_word2 = " your eyes only\n"
        input_word3 = "  srrrr\r\n"
        self.assertEqual(ReceiptView.contains_delimeter(
            input_word1, self.delimiters), False)
        self.assertEqual(ReceiptView.contains_delimeter(
            input_word2, self.delimiters), False)
        self.assertEqual(ReceiptView.contains_delimeter(
            input_word3, self.delimiters), False)
