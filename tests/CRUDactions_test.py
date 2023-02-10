import sys
from unittest import TestCase, main

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, "C:/Users/mykhailot/PyTask/PythonTasks11/mentorTask11")
import CRUDactions
import pymongo
from cl_currency import ClCurrency
from mongo_actions import add_transaction, clear_db, get_transaction, update_user
from statuses import Status
from transaction_details import TransactionDetails
from user import User

client = pymongo.MongoClient("localhost:27017")
db = client.Market
coll1 = db.Transactions
coll2 = db.Users
client = TestClient(CRUDactions.app)
clear_db(coll2)
clear_db(coll1)


class CRUDactionsTest(TestCase):
    def test_get_trans_value_check(self):
        us1 = User("3214", [])
        update_user(us1, coll2=coll2)
        add_transaction(
            user_id=us1.user_id,
            details=TransactionDetails(
                transaction_id="tid200342",
                transaction_status=Status.Successful,
                amount=33,
                recipient_id="uid2345",
                currency=ClCurrency.EUR,
            ),
            coll2=coll2,
            coll1=coll1,
        )

        response = client.get("/get?t_id=tid200342")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "transaction_id": "tid200342",
                "transaction_status": 1,
                "amount": 33,
                "currency": 3,
                "recipient_id": "uid2345",
            },
        )

    def test_update_trans_execution_check(self):
        t_id = "tid200342"
        response = client.put(
            f"/put/transaction?transaction_id={t_id}&transaction_status=Successful&amount=43&recipient_id=uid2345&currency=USD"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), f"Transaction {t_id} updated successfully")
        self.assertEqual(
            get_transaction(t_id, coll1),
            TransactionDetails(
                transaction_id="tid200342",
                transaction_status=Status.Successful,
                amount=43,
                recipient_id="uid2345",
                currency=ClCurrency.USD,
            ),
        )

    def test_delete_trans_execution_check(self):
        t_id = "tid200342"
        response = client.delete(f"/delete?t_id={t_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), f"Transaction {t_id} deleted successfully")
        self.assertEqual(get_transaction(t_id, coll1), "We cannot get nonexistent transaction")

    def test_add_trans_execution_check(self):
        t_id = "tid200342"
        u_id = "uid3290"
        response = client.post(
            f"/post/user/{u_id}/transaction?transaction_id={t_id}&transaction_status=Successful&amount=0&recipient_id=uid2000&currency=USD"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), f"New user {u_id} added successfully. Transaction {t_id} added successfully")
        self.assertEqual(
            get_transaction(t_id, coll1),
            TransactionDetails(
                transaction_id=t_id,
                transaction_status=Status.Successful,
                amount=0,
                recipient_id="uid2000",
                currency=ClCurrency.USD,
            ),
        )
