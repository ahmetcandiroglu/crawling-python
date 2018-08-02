import time


def log(str_to_print):
    c_time = time.strftime("%d-%m-%Y %H:%M", time.gmtime())
    with open("money.log", "a") as money_log:
        print(str_to_print + c_time, file=money_log)
        print('-' * len(str_to_print), file=money_log)


def reset_and_log(str_to_print):
    c_time = time.strftime("%d-%m-%Y %H:%M", time.gmtime())
    with open("money.log", "w") as money_log:
        print(str_to_print + c_time, file=money_log)
        print('-' * len(str_to_print), file=money_log)
