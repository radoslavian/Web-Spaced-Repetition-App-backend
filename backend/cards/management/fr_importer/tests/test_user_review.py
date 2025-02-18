import json
import pprint
import unittest
from datetime import datetime, timedelta

from cards.management.fr_importer.modules.user_review import UserReview


class UserReviewTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # from the <fullrecall> opening attribute
        # first day of your FullRecall learning (in Unix time format)
        cls.time_of_start = 1186655166
        # input:
        cls.extracted_attributes = {
            # <item>'s attributes:
            # id number (in fact: time of creating item in Unix time format)
            "id": 1236435838,
            # time to repeat
            "tmtrpt": 6574,
            # time to repeat computed on not-ahead-of-scheduled-time review
            "stmtrpt": 6574,
            # last interval computed by ANN (in days; 0-2048)
            "livl": 1274,
            # real last interval (in days; 0-2048)
            "rllivl": 1764,
            # interval (in days; 0-2048)
            "ivl": 583,
            # number of not-ahead-of-scheduled-time reviews (0-128)
            "rp": 6,
            # grade (0-5; 0=the worst, 5=the best)
            "gr": 4
        }
        time_of_start = datetime.fromtimestamp(cls.time_of_start)
        # output:
        cls.user_review = {
            "computed_interval": 583,
            "lapses": 0,
            "reviews": 6,
            "total_reviews": 6,
            "last_reviewed": time_of_start + timedelta(
                days=cls.extracted_attributes["stmtrpt"]) - timedelta(
                days=cls.extracted_attributes["ivl"]),
            "introduced_on": datetime.fromtimestamp(
                cls.extracted_attributes["id"]),
            # actually the 'next review date'
            "review_date": time_of_start + timedelta(
                days=cls.extracted_attributes["stmtrpt"]),
            "grade": cls.extracted_attributes["gr"],
            "easiness_factor": 1.4,
            "crammed": False,
            "comment": None
        }

    def test_conversion(self):
        review = UserReview(self.extracted_attributes, self.time_of_start)
        self.assertDictEqual({**review}, self.user_review)

    def test_ef_too_low(self):
        """
        Should return 1.4 for a card where computed ef is lower than 1.4.
        """
        # the formula is: ivl/rlivl
        rllivl = 271  # last real interval
        ivl = 33  # (current) interval
        expected_ef = 1.4
        review_details = {
            **self.extracted_attributes,
            "rllivl": rllivl,
            "ivl": ivl
        }
        review = UserReview(review_details, self.time_of_start)
        self.assertEqual(expected_ef, review["easiness_factor"])

    def test_ef_right(self):
        """
        Should return not normalized ef (increase to 1.4 or reduce to 3.0).
        """
        rllivl = 673  # last real interval
        ivl = 1397  # (current) interval
        expected_ef = 2.08  # round to two decimal places
        review_details = {
            **self.extracted_attributes,
            "rllivl": rllivl,
            "ivl": ivl
        }
        review = UserReview(review_details, self.time_of_start)
        self.assertEqual(expected_ef, review["easiness_factor"])

    def test_ef_too_high(self):
        """
        Should return 4.0 for a card where a computed ef is higher than 4.0.
        """
        rllivl = 67  # last real interval
        ivl = 1397  # (current) interval
        expected_ef = 4.0
        review_details = {
            **self.extracted_attributes,
            "rllivl": rllivl,
            "ivl": ivl
        }
        review = UserReview(review_details, self.time_of_start)
        self.assertEqual(expected_ef, review["easiness_factor"])

    @unittest.skip
    def test_invalid_interval(self):
        """
        Raises ValueError in case of interval lower than 0.
        """
        user_review = {**self.extracted_attributes, "ivl": -10}
        self.assertRaises(ValueError,
                          lambda: UserReview(
                              user_review, self.time_of_start).easiness_factor)
