import json
import unittest

from timeseries import FlatBufferRows
from tests.lib.api_test_base import APITestBase
import time
from tablestore.flatbuffer import timeseries_flat_buffer_encoder
from tablestore import metadata
from tablestore import *


class TimeseriesApiTest(APITestBase):
    """TimeseriesFlatBufferTest"""



    def test_timeseries_api(self):
        client = self.client_test
        prefix = "python_sdk_test"
        table_name = prefix + str(int(time.time()))

        try:
            b = client.list_timeseries_table()
            for item in b:
                if item.timeseries_table_name.startswith(prefix):
                    client.delete_timeseries_table(item.timeseries_table_name)
        except Exception as e:
            print(e)

        print("start to sleep")
        time.sleep(30)
        print("finish sleep")

        meta = metadata.TimeseriesTableMeta(table_name)
        meta.field_primary_keys = [('a1', 'INTEGER'), ('b1', 'STRING')]
        meta.timeseries_keys = ["a", "b"]
        meta.timeseries_table_options = metadata.TimeseriesTableOptions(172800)
        request = metadata.CreateTimeseriesTableRequest(meta)
        client.create_timeseries_table(request)

        self.logger.info("start to sleep")
        time.sleep(30)
        self.logger.info("finish sleep")

        b = client.list_timeseries_table()
        self.assertTrue(len(b) > 0, "num of timeseries table should be more than one")

        for item in b:
            if item.timeseries_table_name == table_name:
                table_item = item
                found = True
        self.assertTrue(found, "do not find expected table")

        self.assert_equal(table_item.timeseries_table_options.time_to_live, 172800)
        self.assert_equal(len(table_item.timeseries_keys), 2)
        self.assert_equal(table_item.timeseries_keys[0], meta.timeseries_keys[0])
        self.assert_equal(table_item.timeseries_keys[1], meta.timeseries_keys[1])
        i = 0
        while i < 5:
            try:
                resp = client.describe_timeseries_table(table_name)
                break
            except Exception as e:
                i=i+1
                time.sleep(20)

        self.assert_equal(resp.table_meta.timeseries_table_name, table_name)
        self.assert_equal(resp.table_meta.timeseries_table_options.time_to_live, 172800)
        self.assert_equal(len(resp.table_meta.timeseries_keys), 2)
        self.assert_equal(resp.table_meta.timeseries_keys[0], meta.timeseries_keys[0])
        self.assert_equal(resp.table_meta.timeseries_keys[1], meta.timeseries_keys[1])
        self.assert_equal(resp.table_meta.status, "CREATED")

        print("start to sleep")
        time.sleep(30)
        print("finish sleep")

        client.delete_timeseries_table(table_name)
        try:
            resp = client.describe_timeseries_table(table_name)
            self.fail("fail")
        except Exception as e:
            print("1")
        print("finish")



if __name__ == '__main__':
    unittest.main()
