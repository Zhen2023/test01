import os

def get_dir():
    while True:
        dir_path = input("请输入要查看的目录：").strip()
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"您需要查看的目录是'{dir_path}',结构如下：")
            contents = os.listdir(dir_path)
            if not contents:
                print("该目录为空")
            else:
                for content_name in contents:
                    content = os.path.join(dir_path, content_name)
                    if os.path.isdir(content):
                        print(f"【目录】{content_name}")
                    elif os.path.isfile(content):
                        print(f"【文件】{content_name}")
                    else:
                        print(f"【其他】{content_name}")
            break
        else:
            print("您输入的目录不存在，请重新输入")
            continue
        

get_dir()