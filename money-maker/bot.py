import crawler
import logger


class Bot:

    def __init__(self, s_usd, bank_id):
        logger.log(f'Starting with {s_usd}$ in {bank_id} bank\n')

        self.s_usd = s_usd
        self.s_tl = 0.0
        self.usd = s_usd
        self.tl = 0.0

        self.last_rate = 0.0
        self.sensitivity = 0.05
        self.bank_id = bank_id

        self.init_accounts()

    def init_accounts(self):
        rate = crawler.get_bank_dollar_price(self.bank_id)
        self.s_tl = self.s_usd * rate['sell']
        self.last_rate = rate['sell']

    def sell_usd(self, amount, rate):
        if self.usd < amount:
            return

        self.usd -= amount
        self.tl += amount * rate
        self.last_rate = rate
        logger.log(f'Sell {amount}$ = {amount*rate}₺\n')

    def buy_usd(self, amount, rate):
        if self.tl < amount * rate:
            return

        self.usd += amount
        self.tl -= amount * rate
        self.last_rate = rate
        logger.log(f'Buy {amount}$ = {amount*rate}₺')

    def decide(self, command, buy_rate, sell_rate):
        logger.log(f'You should do: {command} / 1$ = {buy_rate}₺\n')

        if command == 'Güçlü Al':
            if self.usd <= 0:
                return

            self.buy_usd(self.usd, buy_rate)

        elif command == 'Al':
            if self.usd <= 0 | self.last_rate + self.sensitivity < buy_rate:
                return

            self.buy_usd(self.usd, buy_rate)

        elif command == 'Sat':
            if self.usd <= 0 | self.last_rate - self.sensitivity > sell_rate:
                return

            self.sell_usd(self.usd, sell_rate)

        elif command == 'Güçlü Sat':
            if self.usd <= 0:
                return

            self.sell_usd(self.usd, sell_rate)

        else:
            logger.log(f'Doing nothing zZz..\n')

    def compare_all_time(self, buy_rate, sell_rate):
        c_usd = self.usd + self.tl / buy_rate
        c_tl = self.tl + self.usd * sell_rate

        p_usd = (c_usd - self.s_usd) / self.s_usd * 100
        p_tl = (c_tl - self.s_tl) / self.s_tl * 100

        logger.log(f'Start: {self.s_usd}$ = {self.s_tl}₺')
        logger.log(f'Current: {c_usd}$ = {c_tl}₺')
        logger.log(f'Profit: {p_usd}% ($) = {p_tl}% (₺)')

    def make_decision(self, interval):
        command = crawler.get_dollar_advice()[interval]
        rate = crawler.get_bank_dollar_price(self.bank_id)

        self.decide(command, rate['buy'], rate['sell'])

    def log_account(self):
        rate = crawler.get_bank_dollar_price(self.bank_id)
        self.compare_all_time(rate['buy'], rate['sell'])
