import pymongo
from camel_to_snake_converter import change_case
from cl_currency import ClCurrency
from transaction_details import TransactionDetails
from user import User
from statuses import Status

client = pymongo.MongoClient("localhost:27017")
db = client.Market
coll1 = db.Transactions
coll2 = db.Users


def add_user(user: User, coll2=coll2):
    coll2.insert_one({"UserId": user.user_id, "Transactions": user.transactions})


def update_user(user: User, coll2=coll2):
    if len(coll2.find_one({"UserId": user.user_id})) < 1:
        add_user(user=user)
    else:
        filter = {"UserId": user.user_id}
        new_values = {"$set": {"Transactions": user.transactions}}
        coll2.update_one(filter, new_values)


def add_transaction(user_id: str, details: TransactionDetails, coll1=coll1, coll2=coll2):
    if len(coll2.find_one({"UserId": user_id})) < 1:
        add_user(User(user_id=user_id, transactions=[details.transaction_id]))
    else:
        l = list(coll2.find_one({"UserId": user_id})["Transactions"])
        h = [i for i in l]
        h.append(details.transaction_id)
        update_user(User(user_id=user_id, transactions=h))
    coll1.insert_one(
        {
            "TransactionId": details.transaction_id,
            "Amount": details.amount,
            "Currency": details.currency.name,
            "TransactionStatus": details.transaction_status.name,
            "RecepientId": details.recipient_id,
        }
    )


def get_transaction(transaction_id: str, coll1=coll1):
    t = TransactionDetails()
    for i in coll1.find({"TransactionId": transaction_id}):
        for k, v in i.items():
            t.__setattr__(k, v)
    return t


def update_transaction(details: TransactionDetails, coll1=coll1):
    flag = False
    for new_data in coll1.find({"TransactionId": details.transaction_id}):
        for k, v in new_data.items():
            k = change_case(k)
            if k != "_id" and details.__dict__[k] != v:
                flag = True
                break
    if flag:
        filter = {"TransactionId": details.transaction_id}
        new_values = {
            "$set": {
                "TransactionId": details.transaction_id,
                "Amount": details.amount,
                "Currency": details.currency.name,
                "TransactionStatus": details.transaction_status.name,
                "RecepientId": details.recipient_id,
            }
        }
        coll1.update_one(filter, new_values)


def create_index(field, unique=False, coll1=coll1):
    coll1.create_index(field, unique=unique)


def delete_transaction(transaction_id: str, coll1=coll1):
    coll1.delete_one({"TransactionId": transaction_id})


def clear_db(coll=coll1):
    coll.delete_many({})

def create_transactions(user:User,n:int):
    for i in range(n):
        add_transaction(user_id=user.user_id,details=TransactionDetails(
            transaction_id=f'tid200{i}',
            transaction_status=Status.Successful,
            amount=i*i+200%(i+1),
            recipient_id=f'uid234{i*2}',
            currency=ClCurrency.EUR
        ))

if __name__ == "__main__":
    clear_db()
    clear_db(coll2)
    us1 = User("3214", [])
    n=20
    trad = TransactionDetails(transaction_id='tid200')
    add_user(us1)
    add_transaction(us1.user_id, trad)
    create_transactions(us1,n)
    update_transaction(TransactionDetails(amount=2))

    print("ok")
