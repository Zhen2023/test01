import json
import os
import argparse as argp
import csv
import pandas as pd
import datetime as dt

class Contact:
    @staticmethod
    def is_valid_phone_format(phone):
        phone_str = phone.strip()
        if not phone_str:
            # print("输入手机号为空")
            return True
        elif not phone_str.isdigit():
            # print(f"输入手机号‘{phone_str}’包含非数字字符，不是有效手机号。")
            return False
        elif len(phone_str) != 11:
            # print(f"输入手机号‘{phone_str}’长度不为11，不是有效手机号。")
            return False
        else:
            return True

    @staticmethod
    def is_valid_email_format(email):
        email_str = email.strip()
        if not email_str:
            # print("输入邮箱为空")
            return True
        elif email_str.count('@') == 1:
            parts = email_str.split('@',1)
            if parts[0] and parts[1] and '.' in parts[1] and  not parts[1].startswith('.') and not parts[1].endswith('.'):
                if len(parts[1].split('.')[-1]) >= 2:#顶级域名长度至少为2
                    return True
                    
        else:
            return False

        
    def __init__(
        self, 
        name : str, 
        phone : str = "", 
        email : str = "", 
        notes : str = "", 
        ):
        if not name.strip():
            raise ValueError("联系人姓名不能为空")
        self.name = str(name).strip()

        self.phone = ""
        phone_str = str(phone).strip()
        if phone_str:
            if Contact.is_valid_phone_format(phone_str):
                self.phone = phone_str
            else:
                print(f"输入手机号{phone_str}无效，手机号默认为空")


        self.email = ""
        email_str = str(email).strip()
        if email_str:
            if Contact.is_valid_email_format(email_str):
                self.email = email_str
            else:
                print(f"输入邮箱{email_str}无效，邮箱默认为空")

        self.notes = str(notes).strip()

        
    def __str__(self):
        return f"姓名：{self.name}\n手机号：{self.phone if self.phone else "无"}\n邮箱：{self.email if self.email else "无" }\n备注：{self.notes if self.notes else "无"}"

    def edit(self,name=None,phone=None,email=None,notes=None):
        
        if name is not None:
            name = str(name).strip()
            if self.name.strip() == name or not name:
                print("新名字为空或未变，本次未做修改")
            else:
                self.name = name
                print(f"姓名更新为{self.name}")
        
        if phone is not None:
            phone = str(phone).strip()
            if self.phone.strip() == phone:
                print("新手机号未变，本次未做修改")
            elif phone == "":
                self.phone = ""
                print("手机号已清空")
            elif Contact.is_valid_phone_format(phone):
                self.phone = phone
                print(f"手机号更新为{self.phone}")
            else:
                print(f"{phone}不是有效手机号，手机号不做修改")
        if email is not None:
            email = str(email).strip()
            if self.email == email:
                print("新邮箱未变，本次未做修改")
            elif email == "":
                self.email = ""
                print("邮箱已清空")
            elif Contact.is_valid_email_format(email):
                self.email = email
                print(f"邮箱更新为{self.email}")
            else:
                print(f"{email}不是有效邮箱，邮箱不做修改")
        if notes is not None:
            notes = str(notes).strip()
            if self.notes.strip() == notes:
                print("新备注未变，本次未做修改")
            elif notes == "":
                self.notes = ""
                print("备注已清空")
            else :
                self.notes = notes
                print(f"备注已更新")

    def to_dict(self):
        return{
            "name":self.name,
            "phone":self.phone,
            "email":self.email,
            "notes":self.notes
        }

    @staticmethod
    def from_dict(contact_dict):
        name_to_check = contact_dict.get("name")
        if not name_to_check or not name_to_check.strip():
            raise ValueError("联系人姓名不能为空")
        else:
            name = name_to_check.strip()
        phone = contact_dict.get("phone","")
        email = contact_dict.get("email","")
        notes = contact_dict.get("notes","")
        return Contact(
            name,
            phone,
            email,
            notes
            )

address_book = []

def add_contact(name,phone="",email="",notes=""):
    if not name.strip():
        print("联系人姓名不能为空")
        return False

    
    try:
        contact = Contact(name,phone,email,notes)   
        address_book.append(contact)
        return True
    except ValueError as e:
        print(f"添加联系人失败，原因：{e}")
        return False

def list_contact():
    if not address_book:
        print("通讯录为空")
        return
    print("-----联系人列表-----")
    for i,contact in enumerate(address_book,1):
        print(f"{i}号联系人------：\n{contact}")
    print("---------列表加载完毕---------")

def save_address_book(file_name="address_book.json"):
    if not address_book:
        print("通讯录为空，无需保存")
        return False

    address_book_dict = [contact.to_dict() for contact in address_book]
    try:
        with open(file_name,"w",encoding="utf-8") as f:
            json.dump(address_book_dict,f,indent=4,ensure_ascii=False)
            
            return True
    except IOError:
        print("出现IO异常，通讯录保存失败")
        return False
    except Exception as e:
        print(f"出现未知异常：{e}，通讯录保存失败")
        return False

def load_address_book(file_name="address_book.json"):
    global address_book
    if not os.path.exists(file_name):
        print("通讯录文件不存在")
        address_book = []
        return
    try:
        with open(file_name,"r",encoding="utf-8") as f:
            address_book_dict = json.load(f)
            address_book_temp = []
            error_count = 0

            for contact_dict in address_book_dict:
                try:
                    contact = Contact.from_dict(contact_dict)
                    address_book_temp.append(contact)
                    
                except Exception as e:
                    error_count += 1
                    print(f"加载联系人{contact.name}时出现异常，跳过：{e}")
            if address_book_temp:
                address_book = address_book_temp
                print(f"共加载{len(address_book)}个联系人，其中{error_count}个联系人加载失败")
            else:
                print("通讯录加载失败")
                address_book = []
    except IOError:
        print("出现IO异常，通讯录加载失败")
        address_book = []
    except json.JSONDecodeError:
        print("出现JSON解码异常，通讯录加载失败")
        address_book = []
    except Exception as e:
        print(f"出现未知异常：{e}，通讯录加载失败")
        address_book = []

def find_contact():
    if not address_book:
        print("通讯录为空")
        return []
    name = input("请输入要查询的联系人姓名：").strip()
    if not name:
        print("查询人姓名不能为空")
        return []
    find_list = []
    
    for contact in address_book:#如果用enumerate()函数，会返回一个元组，元组的第一个元素是索引，第二个元素是列表中的元素，需要解包，即前面需要有两个变量    
        if name.lower() in contact.name.lower():
            find_list.append(contact)
    
    return find_list    
    

def del_contact(index_int):
    
    try:
        if 0 <= index_int < len(address_book):
            poped_contact = address_book.pop(index_int)
            return poped_contact
        else:
            print("内部错误，接收到的编号不存在")
            return False
    except IndexError:
        print("输入的联系人编号不存在")
        return False

def get_user_choice():
    if not address_book:
        print("通讯录为空")
        return None,None

    choice_str = input(f"请输入你要操作的联系人编号：1-{len(address_book)}")
    
    if not choice_str:
        print("输入为空，操作取消")
        return None,None
    elif not choice_str.isdigit():
        print(f"输入非数字，输入错误，请输入联系人编号：1-{len(address_book)}")
        return None,None
    elif 1 <= int(choice_str) <= len(address_book):
        return int(choice_str),address_book[int(choice_str)-1]
    else:
        print(f"输入数字超出范围，输入错误，请输入联系人编号：1-{len(address_book)}")
        return None,None

def export_csv(output_filename = "output_contacts.csv"):
    if not address_book:
        print("通讯录为空，无法导出")
        return
    if os.path.exists(output_filename):
        choice_str = input(f"文件{output_filename}已存在，是否覆盖？（y/n）:").strip().lower()
        if choice_str != "y":
            print("导出取消")
            return
    export_dict = [contact.to_dict() for contact in address_book]
    fieldnames = ["name","phone","email","notes"] #导出的表头
    try:
        with open(output_filename,"w",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames=fieldnames,extrasaction="ignore",restval="N/A")
            writer.writeheader()
            writer.writerows(export_dict)
            print(f"通讯录已导出至{output_filename}")
            return True

    except IOError:
        print("出现IO异常，通讯录导出失败")
        return False
    except Exception as e:
        print(f"出现未知异常：{e}，通讯录导出失败")
        return False

def import_csv(input_filename = "input_contacts.csv"):
    if not os.path.exists(input_filename):
        print("导入文件不存在")
        return
    try:
        # 尝试使用 UTF-8 编码读取
        with open(input_filename,"r",newline="",encoding="utf-8") as f:
            reader_dict = csv.DictReader(f)
            import_list = []
            error_count = 0
            for row_dict in reader_dict:
                try:
                    contact = Contact.from_dict(row_dict)
                    import_list.append(contact)
                except Exception as e:
                    error_count +=1
                    # 尝试从 row_dict 获取 name，如果失败则打印原始字典
                    contact_name = row_dict.get("name", str(row_dict))
                    print(f"导入联系人{contact_name}时出现异常，跳过：{e}")

            if import_list:
                address_book.extend(import_list)
                print(f"共导入{len(import_list)}个联系人，其中{error_count}个联系人导入失败")
            else:
                print("通讯录导入失败")

    except UnicodeDecodeError:
        # 如果 UTF-8 解码失败，尝试使用 GBK 编码
        print(f"使用 UTF-8 编码读取文件 {input_filename} 失败，尝试使用 GBK 编码...")
        try:
            with open(input_filename,"r",newline="",encoding="gbk") as f:
                reader_dict = csv.DictReader(f)
                import_list = []
                error_count = 0
                for row_dict in reader_dict:
                    try:
                        contact = Contact.from_dict(row_dict)
                        import_list.append(contact)
                    except Exception as e:
                        error_count +=1
                        # 尝试从 row_dict 获取 name，如果失败则打印原始字典
                        contact_name = row_dict.get("name", str(row_dict))
                        print(f"导入联系人{contact_name}时出现异常，跳过：{e}")

                if import_list:
                    address_book.extend(import_list)
                    print(f"共导入{len(import_list)}个联系人，其中{error_count}个联系人导入失败")
                else:
                    print("通讯录导入失败")
        except Exception as e:
            # GBK 也失败或出现其他异常
            print(f"使用 GBK 编码读取文件 {input_filename} 也失败：{e}")
            print("通讯录导入失败")

    except IOError:
        print("出现IO异常，通讯录导入失败")
        return False
    except Exception as e:
        print(f"出现未知异常：{e}，通讯录导入失败")
        return False

def load_data_by_pd(file_name):
    if not os.path.exists(file_name):
        print("文件不存在")
        return
    try:
        _,file_extension = os.path.splitext(file_name)
        file_extension = file_extension.lower()

        df = None
        if file_extension == ".csv":
            print("正在使用pandas读取csv文件")
            df = pd.read_csv(file_name,keep_default_na=False,na_filter=False)
        elif file_extension in [".xls",".xlsx"]:
            print("正在使用pandas读取Excel文件")
            try:
                df = pd.read_excel(file_name,sheet_name=0,header=0,keep_default_na=False,na_filter=False)
            except Exception as e_excel:
                print(f"使用默认引擎加载Excel文件失败，{e_excel}")
                if file_extension == ".xls":#旧版Excel文件
                    print("尝试 'xlrd' 引擎加载Excel文件")
                    try:
                        df = pd.read_excel(file_name,sheet_name=0,header=0,keep_default_na=False,na_filter=False,engine="xlrd")
                    except Exception as e_xlrd:
                        print(f"使用xlrd引擎加载Excel文件失败，{e_xlrd}")
                        return None
                else:
                    return None
        else:
            print("不支持的文件类型")
            return None
        print(f"加载数据成功")
        return df
    except FileNotFoundError:
        print("文件不存在")
        return None
    
    except pd.errors.EmptyDataError:
        print("Excel文件为空")
        return None
    except pd.errors.ParserError:
        print("解析Excel文件时出现错误")
        return None
    except IOError:
        print("出现IO异常，数据加载失败")
        return None
    except Exception as e:
        print(f"出现未知异常：{e}，数据加载失败")
        return None

def export_by_pd():
    if not address_book:
        print("通讯录为空，无法导出")
        return False
    df = pd.DataFrame([contact.to_dict() for contact in address_book])
    if df.empty:
        print("数据为空，无法导出")
        return False
    
    try:
        time_str = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"联系人信息_{time_str}.xlsx"
        df.to_excel(file_name,index=False)
        print(f"通讯录已导出至{file_name}")
        return True

    except UnicodeEncodeError:
        print("出现Unicode编码异常，通讯录导出失败")
        return False
    except IOError:
        print("出现IO异常，通讯录导出失败")
        return False
    except Exception as e:
        print(f"出现未知异常：{e}，通讯录导出失败")
        return False





if __name__ == "__main__":
    print("欢迎使用通讯录管理系统")
    load_address_book()
    parser = argp.ArgumentParser(description="通讯录管理系统")
    subparser = parser.add_subparsers(dest="command",help="可执行命令",required=True)
    #子命令，添加联系人
    parser_add = subparser.add_parser("add",help="添加联系人")
    parser_add.add_argument("--name",help="联系人姓名",required=True)
    parser_add.add_argument("--phone",help="联系人手机号（可选）")
    parser_add.add_argument("--email",help="联系人邮箱（可选）")
    parser_add.add_argument("--notes",help="联系人备注（可选）")

    #子命令，编辑联系人
    parser_edit = subparser.add_parser("edit",help="编辑联系人")
    parser_edit.add_argument("uid",type=int,help="联系人编号")
    parser_edit.add_argument("--name",help="新联系人姓名")
    parser_edit.add_argument("--phone",help="新联系人手机号")
    parser_edit.add_argument("--email",help="新联系人邮箱")
    parser_edit.add_argument("--notes",help="新联系人备注")

    #子命令，列出联系人
    parser_list = subparser.add_parser("list",help="列出联系人")

    #子命令，查找联系人
    parser_find = subparser.add_parser("find",help="查找联系人")
    parser_find.add_argument("search",help="要查找的联系人姓名")

    #子命令，删除联系人
    parser_del = subparser.add_parser("del",help="删除联系人")
    parser_del.add_argument("uid",type=int,help="联系人编号")

    #子命令，导出联系人
    parser_export = subparser.add_parser("export",help="导出联系人")
    parser_export.add_argument("--filename",help="导出文件名")

    #子命令，导入联系人
    parser_import = subparser.add_parser("import",help="导入联系人")
    parser_import.add_argument("filename",help="导入文件名")

    args = parser.parse_args()

    if args.command == "add":
        name = args.name
        phone = args.phone
        email = args.email
        notes = args.notes

        if add_contact(name,phone,email,notes):
            print("联系人添加成功")