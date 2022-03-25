import certifi
import pymongo
import datetime

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"


class Lotteries(AgentCheck):
    def check(self, instance):
        uri = 'mongodb+srv://mihai-datadog-test:XKhFpLsfoZtGjWqc@paid-ignition-uat.j2jsk.mongodb.net/ignition?retryWrites=true&w=majority'
        conn = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
        database = conn.ignition
        self.gauge('master_ventures.uat.ignition.lotteries.total', database['lotteries'].count_documents({}))
        lottery_collection = database['lotteries']
        for lottery in lottery_collection.find({}):
            close_string = lottery.get('closeDate')
            close_string_str = str(close_string)
            close_date = datetime.datetime.fromisoformat(close_string_str).date()
            self.gauge('master_ventures.uat.ignition.lotteries', 1, tags=['slug:%s' % lottery.get('slug'), 'last_update:%s' % close_date])
