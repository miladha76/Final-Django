from kavenegar import *
from .models import Account

def send_opt(code:str):
    try:
        api = KavenegarAPI('6756796A38344F6C6C5A4B2F6F5266556C47532F4274326A5337674162344C4A6A424F2F706A6C6C2B6B4D3D')
        params = { 'sender' : '1000596446', 'receptor': 'Account.phone_number', 'message' :f'{code}.وب سرویس پیام کوتاه کاوه نگار' }
        response = api.sms_send( params)
        print(response)
    except (APIException, HTTPException) as e:
        print(e)