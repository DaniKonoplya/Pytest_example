from datetime import timezone, datetime
import pytz
import sys


class Account(object):

    _monthly_interest = 0.5
    _transaction_count = 0
    _account_numbers = set()

    _transaction_types = {
        'withdraw': 'W',
        'deposit': 'D',
        'monthly_interset': 'I',
    }

    def __init__(self, account_number, first_name, last_name, time_zone):
        self.account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        self.time_zone = time_zone
        self._balance = 0.0

    @classmethod
    def get_interest_rate(cls):
        return cls._monthly_interest

    @classmethod
    def set_interest_rate(cls, rate):
        try:
            cls._monthly_interest = float(abs(rate))
        except TypeError:
            raise TypeError(f'Value: {rate} for interest rate is incorrect')

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, account_number):
        try:
            self._account_number
            raise ValueError(
                'This account is already set you can not manually replace !')
        except AttributeError:
            pass
        if isinstance(account_number, int):
            if account_number not in Account._account_numbers:
                self._account_number = account_number
                Account._account_numbers.add(account_number)
            else:
                raise ValueError('This account number already exists.')
        else:
            raise ValueError('Value must be an integer')

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = self.validate_name(first_name, 'first_name')

    @staticmethod
    def validate_name(value, value_type):
        if isinstance(value, str) and len(value.strip()) > 0:
            return value.strip()
        raise ValueError(f'Value for {value_type} must be a valid string')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = Account.validate_name(last_name, 'last name')

    @property
    def transaction_time(self):
        return (datetime.utcnow().astimezone(
            pytz.timezone(self._time_zone)).strftime("%Y-%m-%dT%H:%M:%S"))

    @property
    def time_zone(self):
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone='UTC'):
        if isinstance(time_zone, str) and time_zone in pytz.all_timezones:
            self._time_zone = time_zone
        else:
            raise ValueError('Time zone value is incorrect.')

    @property
    def balance(self):
        return self._balance

    def withdraw(self, val):
        try:
            if float(val) <= self.balance:
                confirm_code =  self._generate_trans_code(Account._transaction_types[sys._getframe().f_code.co_name])
                self._balance -= abs(val)
                return confirm_code
            else:
                message = 'Requilred sum is greater than available.'
                raise ValueError
        except ValueError:
            try:
                raise ValueError(f'{message}')
            except NameError:
                raise ValueError(f'Wrong value for withdrawal is provided.')

    def _generate_trans_code(self, tr_type):
        Account._transaction_count += 1
        return f'{tr_type}-{self.account_number}-{self.transaction_time.replace("-","").replace(":","").replace("T","")}-{Account._transaction_count}'

    def deposit(self, val):
        try:
            val = float(abs(val))
            if val > 0:
                self._balance += val
                return self._generate_trans_code(Account._transaction_types[sys._getframe().f_code.co_name])
            raise ValueError('Should be a positive value for deposit.')
        except TypeError:
            raise TypeError('Wrong value is provided for deposit.')

    @property
    def monthly_interset(self):
        interest = (Account._monthly_interest + 100.0) * self.balance / 100.0
        conf_code =  self._generate_trans_code(Account._transaction_types[sys._getframe().f_code.co_name])
        self._balance = interest
        return conf_code

    @classmethod
    def transaction_data(cls, confirmation_number):
        if isinstance(confirmation_number,str):
            data = confirmation_number.split('-')
            if len(data) != 4:
                raise ValueError('Invalid confirmation code.')
            DataClass = type('DataClass', (), dict())
            DataClass.account_number = data[1]
            DataClass.transaction_code = data[0]
            date_time = data[2]
            DataClass.date_time = date_time[:4] + '-' + date_time[4:6] + '-' + date_time[6:8] + \
                'T' + date_time[8:10] + ":" + \
                date_time[10:12] + ":" + date_time[12:]
            DataClass.transaction_id = data[-1]
            return DataClass
        else:
            raise TypeError('Invalid confirmation code.')


if __name__ == '__main__':

    ac1 = Account(123, 'Denis', 'Konoplya', 'Israel')
    ac = Account(124, 'Denis', 'Konoplya', 'Israel')

    properties = [(k, v)
                  for k, v in Account.__dict__.items() if isinstance(v, property)]

    for k, v in properties:
        print(k)
        print(v.__get__(ac, Account))

    print(ac.balance)
    print(ac.deposit(100.0))
    print(ac.withdraw(10.0))
    c_num = (ac.monthly_interset)
    dat_object = Account.transaction_data(c_num)

    print(dat_object.account_number)
    print(dat_object.transaction_code)
    print(dat_object.date_time)
    print(dat_object.transaction_id)
