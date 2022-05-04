import datetime

def get_now_datetime(forNaming=False):
    if forNaming:
        return datetime.datetime.now().strftime("%y%m%d%H%M%S")
    else:
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def get_today_date():
    return datetime.date.today().strftime("%Y-%m-%d")

def date_from_str(str):
    return datetime.datetime.strptime(str, '%Y-%m-%d').date()



if __name__ == "__main__":
    print(get_now_datetime())
    print(get_today_date())
    print(type(get_now_datetime()))
    print(type(get_today_date()))
    print(date_from_str(get_today_date()))
    print(type(date_from_str(get_today_date())))