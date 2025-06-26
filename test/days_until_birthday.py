import datetime as dt

def next_birth_date(month, day):
    """判断日期是否正确"""
    td_year = dt.date.today().year
    while True:
        try:
            birth_date = dt.date(td_year,month,day)
            return birth_date
        except ValueError:
            td_year += 1
            continue

def days_until_birthday():
    """运行天数计算逻辑"""
    td = dt.date.today()
    while True:
        try:
            month_str = input("请输入您的生日月份：").strip()
            birth_month = int(month_str)
            if birth_month < 1 or birth_month > 12:
                print("输入有误，请输入一个1-12之间的整数")
                continue
            else:
                break
        except ValueError:
            print("输入有误，请输入一个1-12之间的整数")

    while True:
        try:
            day_str = input("请输入您生日的日期：").strip()
            birth_day = int(day_str)
            if birth_month == 2 and (birth_day < 1 or birth_day > 29):
                print(f"输入有误，{birth_month}月份最多只有29天，请输入一个1-29之间的整数")
                continue
            elif birth_month in [4, 6, 9, 11] and (birth_day < 1 or birth_day > 30):
                print(f"输入有误，{birth_month}月份最多只有30天，请输入一个1-30之间的整数")
                continue
            elif birth_day < 1 or birth_day > 31:
                print(f"输入有误，{birth_month}月份最多只有31天，请输入一个1-31之间的整数")
                continue
            else:
                break
        except ValueError:
            print("输入有误，请输入一个整数")
    
    print(f"收到您输入的生日是{month_str}月{day_str}日，现在计算离下一个生日还有多少天")

    if birth_month == 2 and birth_day == 29:
        birth_date  = next_birth_date(birth_month, birth_day)
        difference = birth_date -td
        print(f"您的生日距离{birth_date}还有{difference.days}天")
    else:
        birth_date = dt.date(td.year, birth_month, birth_day)
        if (birth_date - td).days < 0:
            birth_date = dt.date(td.year+1, birth_month, birth_day)
            difference = birth_date - td
            print(f"距离您最近一个生日{birth_date}，还有{difference.days}天")
        elif (birth_date - td).days > 0:
            difference = birth_date - td
            print(f"距离您最近一个生日{birth_date}还有{difference.days}天")
        else:
            print(f"今天是您的生日，祝您生日快乐")

days_until_birthday()
