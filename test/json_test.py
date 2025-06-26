import json
dict1 ={"theme": "dark", "font_size": 12, "show_sidebar": True}

def save_config(dict_data,file_name="config.json"):
    with open(file_name,"w",encoding="utf-8") as f:
        json.dump(dict_data,f,indent=4,ensure_ascii=False)


save_config(dict1)

def load_config(file_name="config.json"):
    with open(file_name,"r",encoding="utf-8") as f:
        load_data = json.load(f)
        print(f"已成功解析json文件，内容如下:")
        print(json.dumps(load_data,indent=4,ensure_ascii=False))
    while True:
        if input("是否要查询某项配置？(y/n)").strip().lower() == "y":
            key = input("请输入要查询的配置项：").strip()
            try:
                print(f"{key}的配置项为：{load_data[key]}")
            except KeyError:
                print(f"{key}不存在，请重新输入")
        else:
            break

load_config()
