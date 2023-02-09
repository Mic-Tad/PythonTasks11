from unittest import TestCase, main
from fastapi.testclient import TestClient

from mentorTask11.CRUDactions import add_trans,update_trans,delete_trans,get_trans,app
import pymongo
from mentorTask11.user import User
from mentorTask11.cl_currency import ClCurrency
from mentorTask11.statuses import Status
from mentorTask11.transaction_details import TransactionDetails
from mentorTask11.mongo_actions import clear_db,add_transaction,add_user


client = pymongo.MongoClient("localhost:27017")
db = client.Market
coll1 = db.Transactions
coll2 = db.Users
client=TestClient(app)

class CRUDactionsTest(TestCase):
    def test_get_trans_value_check(self):
        us1 = User("3214", [])
        add_user(us1,coll2=coll2)
        add_transaction(user_id=us1.user_id,details=TransactionDetails(
            transaction_id='tid200342',
            transaction_status=Status.Successful,
            amount=33,
            recipient_id='uid2345',
            currency=ClCurrency.EUR
        ),coll2=coll2,coll1=coll1)
        response=client.get('/get/tid200342')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
                    "transaction_id": "tid200342",
                    "transaction_status": 1,
                    "amount": "33",
                    "currency": 3,
                    "recipient_id": "uid2345"
        })

    