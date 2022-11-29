from django.conf import settings
import os
from twilio.rest import Client
import random

class MessageHandler:
    phone_number = None
    # otp = None
    def __init__(self,phone_number)->None:
        self.phone_number = phone_number
        # self.otp = otp

    def sent_otp_on_phone(self):

        client=Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)

        verification = client.verify \
                     .v2 \
                     .services('VA216d7193034e240fc19d15444114683f') \
                     .verifications \
                     .create(to=self.phone_number, channel='sms')

                     
    def validate(self,otp1):
        client=Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)

        verification_check = client.verify \
                           .v2 \
                           .services('VA216d7193034e240fc19d15444114683f') \
                           .verification_checks \
                           .create(to=self.phone_number,code=otp1)
        validation=verification_check.status
        print(  validation)
        return validation



        