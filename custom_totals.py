import certifi
import pymongo

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"


class MyClass(AgentCheck):
    def check(self, instance):
        uri = 'mongodb+srv://mihai-datadog-test:XKhFpLsfoZtGjWqc@paid-ignition-uat.j2jsk.mongodb.net/ignition?retryWrites=true&w=majority'
        conn = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        database = conn.ignition
        for collection_name in database.list_collection_names():
            self.gauge("master_ventures.uat.ignition.total", database[collection_name].count_documents(
                {}), tags=["collection:%s" % collection_name])
