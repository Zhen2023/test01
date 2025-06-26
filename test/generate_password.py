import random as re 
import string as st

charset = st.ascii_letters + st.digits + st.punctuation

def generate_password(length):
    password_list = re.choices(charset, k=length)
    password = "".join(password_list)
    return password

while True:
    try:
        length=int(input(f"请输入随机密码长度（最少6位）：").strip())
        if length<6:
            print("密码长度不能小于6位")
            continue
        else:
            while True:
                password = generate_password(length) 
                
                try:
                    p=input(f"您本次生成的随机密码是：{password}，您是否满意？（y/n）").strip().lower()
                    if p == "y":
                        print("密码生成成功,请妥善保管")
                        break
                    elif p == "n":
                        continue
                    else:
                        print("输入有误，请输入y或n")
                        continue
                except ValueError:
                    print("输入有误，请输入y或n")
                    continue
            break
    except ValueError:
        print("输入有误，请输入一个整数")


