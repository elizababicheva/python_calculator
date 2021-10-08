"""These are two trackers: for counting money and calories.
Trackers can count calories / money spent today as well as for the whole week.
"""
import datetime as dt

FORMAT = '%d.%m.%Y'


class Calculator:
    """Parent class with general functionality for money and calorie tracker.
    """

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week = self.today - dt.timedelta(days=7)

    def add_record(self, record):
        """This function adds a new record to the list.
        """

        self.records.append(record)

    def get_today_stats(self):
        """This function returns the number of calories
        or money spent today.
        """

        return sum(record.amount for record in self.records
                   if record.date == self.today)

    def get_week_stats(self):
        """This function returns the number of
        calories or money spent this week.
        """

        return sum(record.amount for record in self.records
                   if self.week < record.date <= self.today)

    def get_money_or_calor_remained(self):
        """This function returns the balance of money or calories
        that can be spent today, based on the limit set by the user.
        """

        return self.limit - self.get_today_stats()


class Record:
    """Parent class with general functionality for money and calorie tracker.
    """

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, FORMAT).date()


class CashCalculator(Calculator):
    """Child class that contains one function.
    """

    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        """This function returns the amount of money left in rubles, euros or dollars.
        In case there is no money, if the currency is not supported by the
        tracker or there is a debt - returns the corresponding message.
        """

        money_dict = {'rub': (CashCalculator.RUB_RATE, 'руб'),
                      'eur': (CashCalculator.EURO_RATE, 'Euro'),
                      'usd': (CashCalculator.USD_RATE, 'USD')}
        money_remained = self.get_money_or_calor_remained()
        rate, name = money_dict[currency]
        if not money_remained:
            return 'Денег нет, держись'
        if currency not in money_dict:
            return "Такой валюты нет!"
        if money_remained > 0:
            return f'На сегодня осталось {(money_remained / rate):.2f} {name}'
        else:
            debt = self.get_today_stats() - self.limit
            return ('Денег нет, держись: твой долг -'
                    f' {(debt / rate):.2f} {name}')


class CaloriesCalculator(Calculator):
    """Child class that contains one function.
    """

    def get_calories_remained(self):
        """This function returns function returns the number of calories
        the user eat today.
        In case the user has reached or exceeded the calorie limit for today,
        will be returned the corresponding message.
        """

        calor_remained = self.get_money_or_calor_remained()
        if calor_remained > 0:
            calories = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {calories} кКал')
        return 'Хватит есть!'


if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
