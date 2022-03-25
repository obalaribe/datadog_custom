import certifi
import pymongo
import country_converter as coco

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"


class MyClass(AgentCheck):
    def check(self, instance):
        uri = 'mongodb+srv://mihai-datadog-test:XKhFpLsfoZtGjWqc@paid-ignition-uat.j2jsk.mongodb.net/ignition?retryWrites=true&w=majority'
        conn = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        database = conn.ignition
        customer_collection = database['customers']
        for customer in customer_collection.find({}):
            country_code3 = customer.get('country').get('code3')
            country_code = coco.convert(country_code3, to='ISO2')
            country = customer.get('country').get('name')
            self.gauge('master.ventures.country.codes', 1, tags=[
                       'customer_email:%s' % customer.get('email'), "country_code:%s" % country_code, "country:%s" % country])

