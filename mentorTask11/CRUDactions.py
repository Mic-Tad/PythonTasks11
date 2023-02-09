from fastapi import FastAPI
import mongo_actions
from cl_currency import ClCurrency
from transaction_details import TransactionDetails
from user import User
from statuses import Status

app = FastAPI()

@app.get('/get')
def get_trans(t_id:str):
    return mongo_actions.get_transaction(t_id)

@app.delete('/delete')
def delete_trans(t_id:str):
    mongo_actions.delete_transaction(t_id)
    return f'Deleted {t_id} successfully'

@app.post('/post/user/{u_id}/transaction')
def add_trans(u_id,transaction_id='tid2000',
            transaction_status='Successful',
            amount=0,
            recipient_id='uid2000',
            currency='USD'):
    mongo_actions.add_transaction(user_id=u_id,details=TransactionDetails(
            transaction_id=transaction_id,
            transaction_status=Status[transaction_status],
            amount=amount,
            recipient_id=recipient_id,
            currency=ClCurrency[currency]
    ))
    return 'Done'

@app.put('/put/transaction')
def update_trans(transaction_id='tid2000',
            transaction_status='Successful',
            amount=0,
            recipient_id='uid2000',
            currency='USD'):
    print(amount)
    mongo_actions.update_transaction(TransactionDetails(transaction_id=transaction_id,
            transaction_status=Status[transaction_status],
            amount=amount,
            recipient_id=recipient_id,
            currency=ClCurrency[currency]))
    return amount

