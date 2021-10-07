import datetime as dt

FORMAT = '%d.%m.%Y'


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week = self.today - dt.timedelta(days=7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        list_sum = []
        for record in self.records:
            if record.date == self.today:
                list_sum.append(record.amount)
        return sum(list_sum)

    def get_week_stats(self):
        sum_week = 0
        for record in self.records:
            if self.week < record.date <= self.today:
                sum_week += record.amount
        return sum_week

    def get_money_remained(self):
        return self.limit - self.get_today_stats()


class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, FORMAT).date()


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        money_dict = {'rub': (CashCalculator.RUB_RATE, 'руб'),
        'eur': (CashCalculator.EURO_RATE, 'Euro'),
        'usd': (CashCalculator.USD_RATE, 'USD')
        }
        money_remained = self.get_money_remained()
        rate, name = money_dict[currency]
        if money_remained == 0:
            return 'Денег нет, держись'
        if money_remained > 0:
            return f'На сегодня осталось {(money_remained / rate):.2f} {name}'
        elif money_remained < 0:
            debt = self.get_today_stats() - self.limit
            return ('Денег нет, держись: твой долг -'
            f' {(debt / rate):.2f} {name}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        if self.limit > self.get_today_stats():
            calories = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
            f' калорийностью не более {calories} кКал')
        else:
            return 'Хватит есть!'


cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
print(cash_calculator.get_today_cash_remained('rub'))
