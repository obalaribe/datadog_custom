import certifi
import pymongo
from bson.objectid import ObjectId

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"


class MyClass(AgentCheck):
    def check(self, instance):
        valid = 'VALIDATED'
        submitted = 'SUBMITTED'
        rejected = 'REJECTED'
        final_rejected = 'FINAL_REJECTED'

        valid_count = 0
        submitted_count = 0
        rejected_count = 0
        final_rejected = 0

        uri = 'mongodb+srv://mihai-datadog-test:XKhFpLsfoZtGjWqc@paid-ignition-uat.j2jsk.mongodb.net/ignition?retryWrites=true&w=majority'
        conn = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        database = conn.ignition
        customers_collection = database['customers']
        identities_collection = database['identities']
        for customer_item in identities_collection.find({}):
            customer = customers_collection.find_one({"_id": ObjectId(customer_item['customer'])})
            country = customer.get('country').get('name')
            if(valid.__eq__(customer_item['state'])):
                valid_count = valid_count + 1
                self.gauge("master.ventures.kyc.valid:", valid_count, tags=["country:%s" % country])
            if(submitted.__eq__(customer_item['state'])):
                submitted_count = submitted_count + 1
                self.gauge("master.ventures.kyc.submitted:", submitted_count, tags=[
                           "country:%s" % country])
            if(rejected.__eq__(customer_item['state'])):
                rejected_count = rejected_count + 1
                self.gauge("master.ventures.kyc.rejected:", rejected_count, tags=[
                           "country:%s" % country])
            if(final_rejected.__eq__(customer_item['state'])):
                final_rejected = final_rejected + 1
                self.gauge("master.ventures.kyc.final_rejected:", final_rejected, tags=[
                           "country:%s" %  country])

