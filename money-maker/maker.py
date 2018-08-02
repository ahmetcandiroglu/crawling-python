from bot import Bot
import logger
import schedule
import time


def make_decision(bot):
    bot.make_decision(5)


def log_account(bot):
    bot.log_account()


logger.reset_and_log('Moneymaker is in business (5 min interval)\n')

genius_bot = Bot(1000, 'enpara')

schedule.every(5).minutes.do(make_decision, genius_bot)
schedule.every().hour.do(log_account, genius_bot)

while True:
    schedule.run_pending()
    time.sleep(1)


