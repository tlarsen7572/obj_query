import datetime
import unittest
import json
from obj_query import DataMap
from obj_query import Query


class QueryTests(unittest.TestCase):
    def test_json_property(self):
        json_data = json.loads('{"property":"abc"}')

        retriever = Query().get('property').finalize()
        value = retriever.get_from(json_data)
        self.assertEqual('abc', value)

    def test_attribute(self):
        class TestObj:
            def __init__(self):
                self.SomeValue = 20

        test_obj = TestObj()

        retriever = Query().get('SomeValue').finalize()
        value = retriever.get_from(test_obj)
        self.assertEqual(20, value)

    def test_missing_attribute(self):
        json_data = json.loads('{"something":1}')

        retriever = Query().get("la la la").finalize()
        value = retriever.get_from(json_data)
        self.assertIsNone(value)

    def test_get_index(self):
        json_data = json.loads('["a","b","c"]')

        retriever = Query().index(1).finalize()
        value = retriever.get_from(json_data)
        self.assertEqual('b', value)

    def test_invalid_index(self):
        json_data = json.loads('["a","b","c"]')

        retriever = Query().index(10).finalize()
        value = retriever.get_from(json_data)
        self.assertIsNone(value)

    def test_nested_objects(self):
        json_data = json.loads('{"something":{"property":["a","b","c"]}}')

        retriever = Query().get("something").get("property").index(2).finalize()
        value = retriever.get_from(json_data)
        self.assertEqual('c', value)

    def test_get_first_item(self):
        json_data = json.loads('["a","b","c"]')

        retriever = Query().first().finalize()
        value = retriever.get_from(json_data)
        self.assertEqual('a', value)

    def test_get_last_item(self):
        json_data = json.loads('["a","b","c"]')

        retriever = Query().last().finalize()
        value = retriever.get_from(json_data)
        self.assertEqual('c', value)

    def test_retrieve_none(self):
        data = None

        retriever = Query().get("something").finalize()
        value = retriever.get_from(data)
        self.assertIsNone(value)

    def test_data_map(self):
        class DataSetter:
            def __init__(self):
                self.Key1 = None
                self.Key2 = None

            def set_key1(self, value):
                self.Key1 = value

            def set_key2(self, value):
                self.Key2 = value

        consumer = DataSetter()
        data_map = DataMap({
            consumer.set_key1: Query().get("Key1").finalize(),
            consumer.set_key2: Query().get("Key2").finalize()
        })

        json_data = json.loads('{"Key1":"abc", "Key2": 20}')
        data_map.transfer(json_data)
        self.assertEqual('abc', consumer.Key1)
        self.assertEqual(20, consumer.Key2)

    def test_convert_datetime(self):
        json_data = json.loads('{"value":"2020-01-02 03:04:05"}')
        retriever = Query().get("value").to_datetime("%Y-%m-%d %H:%M:%S").finalize()
        value = retriever.get_from(json_data)
        self.assertEqual(datetime.datetime(2020, 1, 2, 3, 4, 5), value)


if __name__ == '__main__':
    unittest.main()
