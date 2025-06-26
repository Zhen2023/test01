numbers = [1, 2, 3, 4, 5]
number_ssquares = [num ** 2 for num in numbers ]

even_numbers = [num for num in range(1,11) if num%2 == 0]

uppercase_long_words = [word.upper() for word in words if len(word)>3]

num_squares = {num : num**2 for num in numbers }

len_words ={word:len(word) for word in words }

even_numbers ={num : num**2 for num in range(1,11) if num%2 ==0}

change_dict ={value:key for key,value in original_dict.items()}

def reverse(string):
    return string.reverse()

def reverse2(string):
    return string[::-1]

def reverse3(string):
    return ''.join(reversed(string))

def reverse_up(string):
    string1 =string[::-1].lower()
    return string1[0].upper() + string1[1:]

def reverse_up2(string):
    for i in range(len(string)):
        if i == 0:
            string[i].upper()
        else: 
            string[i].lower()
    return string

def reverse_up3(string):
    return string[::-1].title()


def write_file(name,content):
    contents=content + "\n" + name
    f = open("my_first_file.txt","w")
    f.write(contents)
    f.close()

def write_file2(name,content):
    contents=content + "\n" + name
    with open("my_first_file.txt","w") as f:
        f.write(contents)

def red_file(name):
    with open("my_first_file.txt","r") as f:
        line_list = f.readlines()
        for line in line_list:
            print(line)

def red_file2(name):
    with open("my_first_file.txt","r",encoding="utf-8") as f:
        line_list = f.readlines()
        for i in range(len(line_list)):
            print(i+1,end="")
            print(": "+line_list[i].rstrip())

def red_file3(name):
    with open(name,"r",encoding="utf-8") as f:
        n = 1
        for line in f:
            print(n,end="")
            print(": "+line.strip())
            n+=1
            
def red_file4(name):
    with open(name,"r",encoding="utf-8") as f:
        n = 1
        if f.readline():
            for line in f:
                print(n,end="")
                print(": "+line.rstrip())
                n+=1

def red_file5(name):
    with open(name,"r",encoding="utf-8") as f:
        n = 1
        while f.readline():
            print(n,end="")
            print(": " + f.readline().rstrip())
            n+=1


def red_file7(name):
    with open(name,"r",encoding="utf-8") as f:
        for i,line in enumerate(f,start=1):
            print(i,end="")
            print(": " + line.rstrip())


def multiply_all_simplified(*numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def concatenate_strings(separator, *strings):
    if len(strings) == 0:
        return ""
    elif len(strings) == 1:
        return strings[0]
    else:
        result = strings[0]
        for i in range(1, len(strings)):
            result += separator + strings[i]
        return result
    

def concatenate_strings2(separator, *strings):
    return separator.join(strings)

def concatenate_strings3(separator, *strings):
    if not strings :
        return ""
    else:
        result = strings[0]
        for i in range(1, len(strings)):
            result += separator + strings[i]
        return result

def print_arguments(prefix, *args):
    for arg in args:
       print(f"{prefix}: {arg}")    

def print_kwargs(**options):
    for key, value in options.items():
        print(f"{key}: {value}")

def create_config(config_name, **settings):
     config = {'name':config_name, **settings}
     return config

def format_attributes(**attributes):
    if not attributes:
        return ""
    else:
        result = []
        for key,value in attributes.items():
            result.append(f"{key}={value}")
        return ", ".join(result)

def format_attributes(**attributes):
    if not attributes:
        return ""
    else:
       return ", ".join( [f"{key}={value}" for key,value in attributes.items()])

def format_attributes_no_if(**attributes): #对空列表调用join会返回空字符串
    return ", ".join([f"{key}={value}" for key, value in attributes.items()])

class Car:
    def __init__(self,make,model,year):
        self.make = make
        self.model=model
        self.year=year
        print(f"{self.year}年，一辆由{self.make}制造的{self.model}汽车诞生了！")

    def display_info(self):
        print(f"这是一辆由{self.make}制造的{self.model}汽车，制造年份是{self.year}")

class BankAccount:
    def __init__(self,owner,initial_balance=0.00):
        self.owner = owner
        if initial_balance <0:
            self.balance = 0.00
            print("初始余额不能为负数，已自动设置为0")
        else:
            self.balance = float(initial_balance)
        print(f"{self.owner}的账户创建成功，初始余额为{self.balance:.2f}")

    def deposit(self,amount):
        if amount<=0:
            print("存款金额必须大于0")
        else:
            self.balance += float(amount)
            print(f"已存入{amount:.2f}元，当前余额为{self.balance:.2f}")

    def withdraw(self,amount):
        if amount<=0:
            print("取款金额必须大于0")
        elif amount > self.balance:
            print("余额不足")
        else:
            self.balance -= float(amount)
            print(f"已取出{amount:.2f}元，当前余额为{self.balance:.2f}")
    
    def get_balance(self):
        print(f"{self.owner}的账户余额为{self.balance:.2f}")

class BankAccount2:
    def __init__(self,owner,initial_balance=0.00):
        self.owner = owner
        self._balance=max(initial_balance,0.00)
        print(f"{self.owner}的账户创建成功，初始余额为{self._balance:.2f}")

    def deposit(self,amount):
        if amount<=0:
            print("存款金额必须大于0")
        else:
            self._balance += float(amount)
            print(f"已存入{amount:.2f}元，当前余额为{self._balance:.2f}")

    def withdraw(self,amount):
        if amount<=0:
            print("取款金额必须大于0")
        elif amount > self._balance:
            print("余额不足")
        else:
            self._balance -= float(amount)
            print(f"已取出{amount:.2f}元，当前余额为{self._balance:.2f}")
    
    def get_balance(self):
        print(f"{self.owner}的账户余额为{self._balance:.2f}")

class BankAccount3:
    num_accounts = 0
    def __init__(self,owner,initial_balance=0.00):
        self.owner = owner
        self._balance=max(initial_balance,0.00)
        BankAccount3.num_accounts += 1
        print(f"{self.owner}的账户创建成功，初始余额为{self._balance:.2f}")

    def deposit(self,amount):
        if amount<=0:
            print("存款金额必须大于0")
        else:
            self._balance += float(amount)
            print(f"已存入{amount:.2f}元，当前余额为{self._balance:.2f}")

    def withdraw(self,amount):
        if amount<=0:
            print("取款金额必须大于0")
        elif amount > self._balance:
            print("余额不足")
        else:
            self._balance -= float(amount)
            print(f"已取出{amount:.2f}元，当前余额为{self._balance:.2f}")
    
    def get_balance(self):
        print(f"{self.owner}的账户余额为{self._balance:.2f}")

    @classmethod 
    def get_total_accounts(cls):
        print(f"当前共有{cls.num_accounts}")


class Employee:
    def __init__(self,name,salary=0.00):
        self.name = name
        self._salary = max(float(salary),0.00)

    def  display_info(self):
        print(f"姓名：{self.name}，工资：{self._salary:.2f}元")

class Manager(Employee):
    def __init__(self,name,department,salary=0.00):
        super().__init__(name,salary)
        self.department = department

    def display_info(self):
        super().display_info()
        print(f"部门：{self.department}")


import datetime as dt
now = dt.datetime.now()
print(now)
print(now.strftime("%Y-%m-%d"))
print(now.strftime("%H:%M:%S"))
print(strftime("%Y-%m-%d",now)) #这是错误的写法，strftime是对象的方法，不是函数


import datetime as dt


while True:
    try:
        birth_month = int(input("请输入您生日的月份：").strip())
        if birth_month < 1 or birth_month > 12:
            print("输入有误，请输入一个1-12之间的整数")
            continue
        else:
            break
    except ValueError:
        print("输入有误，请输入一个整数")
        

while True:
    try:
        birth_day = int(input("请输入您生日的日期 ：").strip())
        if birth_day < 1 or birth_day > 31:
            print("输入有误，请输入一个1-31之间的整数")
            continue
        else:
            break
    except ValueError:
        print("输入有误，请输入一个整数")
        continue



def days_until_birthday(birth_month, birth_day):
    td = dt.date.today()
    if td.month<=birth_month:
        birthday = dt.date(td.year,birth_month,birth_day)
        difference = birthday - td
        return difference.days
    else:
        birthday = dt.date(td.year+1,birth_month,birth_day)
        difference = birthday - td
        return difference.days
        

days_until_birthday(birth_month, birth_day)

