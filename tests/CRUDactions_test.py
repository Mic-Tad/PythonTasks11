from unittest import TestCase

from fastapi.testclient import TestClient

import CRUDactions
import pymongo
from cl_currency import ClCurrency
from mongo_actions import add_transaction, clear_db, get_transaction, update_user
from statuses import Status
from transaction_details import TransactionDetails
from user import User
from fast_api_client.fast_api_client.api.default.add_trans_post_user_u_id_transaction_post import \
    sync as transaction_post
from fast_api_client.fast_api_client.client import Client
from fast_api_client.fast_api_client.api.default.delete_trans_delete_delete import sync as transaction_delete
from fast_api_client.fast_api_client.api.default.get_trans_get_get import sync as transaction_get
from fast_api_client.fast_api_client.api.default.update_trans_put_transaction_put import sync as transaction_put


client1 = pymongo.MongoClient("localhost:27017")
db = client1.Market
coll1 = db.Transactions
coll2 = db.Users

clear_db(coll2)
clear_db(coll1)
URL = 'http://127.0.0.1:8000'
client = TestClient(CRUDactions.app, base_url=URL)


class CRUDactionsTest(TestCase):
    def test_get_trans_value_check(self):
        us1 = User("3214", [])
        update_user(us1, coll2=coll2)
        t_id="tid200342"
        add_transaction(
            user_id=us1.user_id,
            details=TransactionDetails(
                transaction_id=t_id,
                transaction_status=Status.Successful,
                amount=33,
                recipient_id="uid2345",
                currency=ClCurrency.EUR,
            ),
            coll2=coll2,
            coll1=coll1,
        )
        response=transaction_get(client=Client(URL),t_id=t_id)
        #response = client.get("/get?t_id=tid200342")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.parsed,
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
        response=transaction_put(client=Client(URL),transaction_id=t_id,transaction_status='Successful',amount=43,recipient_id='uid2345',currency='USD')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.parsed, f"Transaction {t_id} updated successfully")
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
        response = transaction_delete(client=Client(URL), t_id=t_id)
        # response = client.delete(f"/delete?t_id={t_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.parsed, f"Transaction {t_id} deleted successfully")
        self.assertEqual(get_transaction(t_id, coll1), "We cannot get nonexistent transaction")

    def test_add_trans_execution_check(self):
        t_id = "tid200342"
        u_id = "uid3290"
        response = transaction_post(u_id=u_id, client=Client(URL), transaction_id=t_id, transaction_status='Successful',
                                    amount=0, recipient_id='uid2000', currency='USD')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.parsed, f"New user {u_id} added successfully. Transaction {t_id} added successfully")
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
