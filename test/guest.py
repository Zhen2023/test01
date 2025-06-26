import random as re

def guest_game():
    """运行猜数字游戏逻辑"""
    print("来玩猜数游戏吧，请随机输入两个正整数作为范围的上下限，我会在这个范围内随机生成一个整数，你猜猜看它是多少。")
    while True:
       try:
           num1 = int(input(f"输入第一个数字").strip())
           num2 = int(input(f"输入第二个数字").strip()) 
        
           if num1 != num2:
                guest_num = re.randint(min(num1,num2),max(num1,num2))
                break
           else :
                print("两个数字不能相同，请重新输入")
                continue
       except ValueError:
            print("输入错误，请输入一个整数")
        

    amount = 1
    
    while True:
        try:
            guess_num = int(input(f"第{amount}次，请输入你猜测的数字").strip())
            if guess_num < guest_num:
                print("猜小了")
            elif guess_num > guest_num:
                print("猜大了")
            else:
                print(f"恭喜你猜对了，你只用了{amount}次就猜对了")
                break
            amount += 1
        except ValueError:
            print("输入错误，请输入一个整数")
            
guest_game()

# print("来玩一个猜数游戏吧")
# begin = int(input("请输入第1个正整数："))
# end = int(input("请输入第2个正整数："))
# guest_num = re.randint(min(begin,end),max(begin,end))