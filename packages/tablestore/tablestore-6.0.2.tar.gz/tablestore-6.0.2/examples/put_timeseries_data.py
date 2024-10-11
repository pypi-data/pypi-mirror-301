from example_config import *
from tablestore import *
from tablestore.metadata import *
import time

def put_timeseries_data(client: OTSClient):
    tags = {"tag1": "t1", "tag2": "t2"}
    field1 = {"long_field": 1, "string_field": "string", "bool_field": True, "double_field": 0.3}
    field2 = {"binary_field2": b'a'}
    key2 = TimeseriesKey("measure2", "datasource2", tags)
    key1 = TimeseriesKey("measure1", "datasource1", tags)
    time1 = time.time()
    row1 = TimeseriesRow(key1, field1, int(time1 * 1000000))
    time2 = time.time()
    row2 = TimeseriesRow(key2, field2, int(time2 * 1000000))
    rows = [row1, row2]

    tablename = "python"
    client.put_timeseries_data(tablename, rows)


if __name__ == '__main__':
    client = OTSClient(OTS_ENDPOINT, OTS_ACCESS_KEY_ID, OTS_ACCESS_KEY_SECRET, OTS_INSTANCE)
    put_timeseries_data(client)