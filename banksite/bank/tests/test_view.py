from django.test import TestCase
from ..views import bank_auth, bank_reg


class Register_Tests(TestCase):
    def test_bank_auth(self):
        somerequest = self.client.post()
        bank_reg(request=somerequest)

