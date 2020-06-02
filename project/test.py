import pytest

from sol import Account


class Test:
    @pytest.fixture
    def create_object(self):
        return{
            'account_number': 123,
            'first_name': 'Denis',
            'last_name': 'Konoplya',
            'time_zone': 'Israel'
        }

    @pytest.fixture
    def obj(self, create_object):
        Account._account_numbers.clear()
        return Account(**create_object)

    def test_initialization(self, create_object, obj):
        for attr_name in create_object:
            assert getattr(obj, attr_name) == create_object.get(attr_name)

    @pytest.mark.parametrize('account_number,first_name,last_name,time_zone', [(130, '', 'Konoplya', 'Israel'), (124, 'Denis', '', 'Israel'), ('xx', 'Denis', 'Konoplya', 'Israel'), (124, 'Denis', 'Konoplya', ''), (125, 'Denis', 'Konoplya', '   '), (126, 'Denis', 123, 'Israel'), (127, 'Denis', None, 'Israel'), (None, 'Vasya', 'Konoplya', 'Israel'), (128, object, 'Konoplya', 'Israel')])
    def test_wrong_initialization(self, account_number, first_name, last_name, time_zone):
        with pytest.raises(ValueError):
            Account(account_number, first_name, last_name, time_zone)

    @pytest.mark.parametrize('sum_deposit', [100.0, 200.0, 3.0, 3.25, 12])
    def test_interest_rate(self, sum_deposit, create_object, obj):
        interest_rate = Account._monthly_interest
        obj.deposit(sum_deposit)
        new_balance = sum_deposit * (100 + interest_rate) / 100
        obj.monthly_interset
        assert obj.balance == new_balance
    
    def test_same_account(self,create_object,obj):
        with pytest.raises(ValueError):
            Account(**create_object)

