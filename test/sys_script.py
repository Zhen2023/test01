import sys

def get_args():
    
    if len(sys.argv) < 2 :
        print(f"缺少命令参数，请至少需要输入一个参数，第一个参数必须是'greet <名字>' 或'info'")
        sys.exit(1)
    elif sys.argv[1] == 'info':
        print(f"当前操作系统信息{sys.platform},Python版本信息{sys.version}")
        sys.exit(0)
    elif sys.argv[1] == 'greet' :
        if len(sys.argv) >= 3:
            print(f"Hello,{sys.argv[2]}")
            sys.exit(0)
        else:
            print(f"'greet'且后面带有 <名字> ")
            sys.exit(1)
    else:
        print(f"第一个参数必须是'greet'且后面带有 <名字> 或'info' ")
        sys.exit(1)

get_args()
