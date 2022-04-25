from kavenegar import KavenegarAPI

from main_app import settings
from main_app.celery import app


@app.task()
def send_otp_message(phone,code):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_KEY)
        params = {
            'receptor': phone,
            'token': code,
            'template': settings.TOKEN_TEMPLATE
        }
        api.verify_lookup(params=params)

    except Exception as error:
        print("Error : {}".format(error))
