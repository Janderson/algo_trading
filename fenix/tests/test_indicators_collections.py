import unittest
from app.indicators.base_indicator import BaseIndicator
from app.indicators.indicators_collection import IndicatorsCollection


class TestIndicatorCollections(unittest.TestCase):
    def test_create_a_collection_of_indicators_should_only_accept_indicators(self):
        collection = IndicatorsCollection()

        class FakeIndicator(BaseIndicator):
            def calc(self):
                pass
            def name(self):
                return "fake"

            def base_params(self):
                return {"oneparam": 12}

            def col_name(self):
                return {"oneparam": 12}

        self.assertTrue(collection.add(FakeIndicator(user_params={"oneparam":12})))
        self.assertEqual(type(FakeIndicator({"oneparam":12})), type(collection[0]))
        self.assertFalse(collection.add(FakeIndicator(None)))
        with self.assertRaises(Exception):
            collection.add("should not accept string")
