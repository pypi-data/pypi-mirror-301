
from example_config import *
from tablestore import *
from tablestore.metadata import *

def create_timeseries_table(client: OTSClient):
    tableOption = TimeseriesTableOptions(172800)
    metaOption = TimeseriesMetaOptions(None, False)
    tableMeta = TimeseriesTableMeta("ts4",tableOption,metaOption)
    analytical_store = TimeseriesAnalyticalStore("as",2592000,SYNC_TYPE_FULL)
    lastPointIndex = LastpointIndexMeta("last1")
    request = CreateTimeseriesTableRequest(tableMeta,[analytical_store],True,[lastPointIndex])
    ret = client.create_timeseries_table(request)
    print(ret)

if __name__ == '__main__':
    client = OTSClient(OTS_ENDPOINT, OTS_ACCESS_KEY_ID, OTS_ACCESS_KEY_SECRET, OTS_INSTANCE)
    create_timeseries_table(client)
