import json
import os
import datetime as dt
import typing as typ

VALID_STATUS = {"待办","已完成"} #集合查询更快
VALID_PRIORITY = {"高","中","低",None}#优先级指定值


class Task:
    def __init__(self, description : str, status :str ="待办",priority: typ.Optional[str]=None,end_date: typ.Optional[str]=None):

        if not description.strip():
            raise ValueError("任务描述不能为空")
        else:
            self.description = description.strip()
  
        if status not in VALID_STATUS:
            print(f"无效的状态{status}，已设置为默认值“待办”")
            self.status = "待办"
        else:
            self.status = status

        if priority not in VALID_PRIORITY:
            print(f"无效的优先级{priority}，已清空")
            self.priority = None
        else:
            self.priority = priority
        
        self.end_date:typ.Optional[dt.date] = None

        if isinstance(end_date,str) and end_date:
            try:
                self.end_date = dt.date.fromisoformat(end_date)
            except ValueError:
                print(f"无效的日期格式{end_date}，请按“年-月-日“格式输入日期，如2025-05-23")
        elif isinstance(end_date,dt.date):
            self.end_date = end_date
       

    def mark_done(self):
        self.status = "已完成"
        
    def mark_undone(self):
        self.status = "待办"
    
    def set_priority(self,new_priority):
        if new_priority not in VALID_PRIORITY :
            return False
        self.priority = new_priority
        return True
    
    def set_end_date(self,new_end_date):
        if new_end_date is None:
            self.end_date = None
            return True
        elif isinstance(new_end_date,str) and new_end_date:
            try:
                self.end_date = dt.date.fromisoformat(new_end_date)
                return True
            except ValueError:
                print(f"无效的日期格式{new_end_date}，请按“年-月-日“格式输入日期，如2025-05-23")
                return False

        elif isinstance(new_end_date,dt.date):
            self.end_date = new_end_date
            return True
        else:
            return False

    
    def edit_description(self, new_description):
        if not new_description.strip():
            return False
        self.description = new_description
        return True

    def __str__(self):
        return f"({self.status}){self.description} - 优先级：{self.priority if self.priority else "无" } ； 截止日期：{self.end_date if self.end_date else "无"}"
    
    def to_dict(self):
       
        return {
            "description":self.description,
            "status":self.status,
            "priority":self.priority,
            "end_date":self.end_date.isoformat() if self.end_date else None
        }

    @staticmethod
    def from_dict(task_dict):
        if 'description' not in task_dict:
            raise ValueError("任务字典缺少‘description’键")

        description = task_dict['description']
        status = task_dict.get('status',"待办")
        priority = task_dict.get('priority',None)

        end_date_str = task_dict.get('end_date',None)
        final_end_date:typ.Optional[dt.date] = None
        if isinstance(end_date_str,str) and end_date_str:
            try:
                final_end_date = dt.date.fromisoformat(end_date_str.strip())
            except ValueError:
                print(f"{description}的截止日期{end_date_str}无效，将清空该值") 

        return Task(description,status,priority,final_end_date)

todo_list = []

def add_task(description):
    # global todo_list # 在函数内部修改全局列表时，严格来说不需要 global (因为修改的是列表内容，不是重新赋值列表变量本身)
                    # 但如果函数内部有 todo_list = ... 这样的重新赋值操作，就需要 global
    if not description: # 简单的非空校验
        print("任务描述不能为空！")
        return 
    task = Task(description)
    todo_list.append(task)
    print(f"任务‘{description}’已添加")

def del_task(index_int):
    if 0 <= index_int < len(todo_list):
        try:
            poped_task = todo_list.pop(index_int)
            return poped_task
        except IndexError:
            print(f"内部错误，尝试删除{index_int+1}号任务时失败")
            return None
    else:
        print(f"内部错误，传递给‘del_task’的参数‘{index_int}’无效")
        return None

def save_tasks(file_name="tasks.json"):
    tasks_dict = [task.to_dict() for task in todo_list]
    try:
        with open(file_name,"w",encoding="utf-8") as f:
            json.dump(tasks_dict,f,indent=4,ensure_ascii=False)
        print(f"当前任务已保存到‘{file_name}’")
    except IOError as e:
        print(f"保存'{file_name}'时IO异常,error:{e}")

    except Exception as e:
        print(f"保存'{file_name}'发生未知错误,error:{e}")

def load_todo_list(file_name="tasks.json"):
    global todo_list
    todo_list_temp = []
    try:
        if os.path.exists(file_name):#变量地址，增加了文件是否存在的判断
            with open(file_name,"r",encoding="utf-8") as f :
                tasks_dict = json.load(f)
                error_count = 0
                for task in tasks_dict:
                    try:
                        todo_list_temp.append(Task.from_dict(task))
                    except ValueError as ve:
                        error_count += 1
                        print(f"加载任务{task}失败 ：{ve}")

                #todo_list_temp = [Task.from_dict(task) for task in tasks_dict]
            todo_list = todo_list_temp
            print(f"任务已从{file_name}加载,成功：{len(todo_list)}个，失败：{error_count}个")
            
        else:
            print(f"文件'{file_name}'不存在")
    except IOError as e:
        print(f"加载{file_name}失败，error:{e}")
    except json.JSONDecodeError:
        print(f"错误：文件 '{file_name}' 格式不正确。将使用空列表。")
        todo_list = []
    except Exception as e:
        print(f"发生未知错误，加载'{file_name}'失败，error:{e}")
        todo_list = []

def list_tasks():
    print("\n--- 当前任务列表 ---")
    if not todo_list:
        print("任务列表为空")
        return

    for i,task in enumerate(todo_list,1):
        print(f"{i}.{task}")
    print("---------------")

def get_task_from_user_input():
    if not todo_list:
        print("任务列表为空，无法操作任务")
        return None,None
    try:
        index_str = input(f"请输入您要操作的任务编号：").strip()
        index_int = int(index_str) - 1
        if 0 <= index_int < len(todo_list):
            return todo_list[index_int],index_int
        else:
            print(f"无效的任务编号，请输入1-{len(todo_list)}内的整数")
            return None,None
    except ValueError:
        print("无效的任务编号，请输入一个整数")
        return None,None
    except Exception as e:
        print(f"获取任务失败，error:{e}")
        return None,None

def clear_done_tasks():
    """清除状态为“已完成”的任务"""
    global todo_list
    if not todo_list:
        return 0
    todo_list_temp =[task for task in todo_list if task.status != "已完成"]
    clear_count = len(todo_list) - len(todo_list_temp)
    todo_list = todo_list_temp
    return clear_count
    

# --- 主程序入口 ---
if __name__ == "__main__":
    prompt_options = ", ".join(f"'{opt}'" if opt is not None else "'无'" for opt in VALID_PRIORITY)

    print("欢迎使用任务管理系统")
    load_todo_list()
    
    while True:
        list_tasks()
        input_str = input("请输入命令(n:新建任务，m：修改任务状态，q：退出，d：删除，e：编辑，cd:清除已完成任务，p：设置优先级，sd:设置完成日期)，不区分大小写:").strip().lower()
        #新建任务
        if input_str == "n":
            description = input("请输入任务描述：").strip()
            add_task(description)
        #修改任务状态
        elif input_str == "m":
            task,index_m_int = get_task_from_user_input()
            if not task:
                continue

            current_status = task.status
            action_description = "'完成'" if current_status == "待办" else "'待办'"
            
            m_choice = input(f"当任务{index_m_int+1}: {task}，是否要将状态标记为{action_description}：（y/n）").strip().lower()
            if  m_choice == "y":
                if current_status == "待办":
                    task.mark_done()
                else: # current_status == "已完成"
                    task.mark_undone()
                print(f"任务修改完成：{index_m_int+1}: {task.description}状态更新为{task.status}")   
                    
            elif m_choice == "n": 
                print("已取消修改任务状态")
            else:
                print("无效的输入，操作已取消")

        #删除任务
        elif input_str == "d":
            task,index_d_int = get_task_from_user_input()
            if not task:
                continue
            
            try:
                d_choice = input(f"确认删除任务{task}?(y/n)").strip().lower()
                if d_choice == "y":
                    poped_task = del_task(index_d_int)
                    print(f"已删除任务{poped_task}")
                elif d_choice == "n":
                    print("删除操作已取消")
                else:
                    print("无效的输入，操作已取消")
                        
            except Exception as e:
                print(f"删除任务失败，error:{e}")
        
        #编辑任务
        elif input_str == "e":
            task, index_e_int = get_task_from_user_input()
            
            if not task:
                continue
            old_description = task.description
            new_description = input(f"将修改{index_e_int+1}:{old_description},请输入新的任务描述：(回车表示“退出，不修改”)").strip()
            if not new_description:
                print("输入的任务描述为空,操作已取消")
                continue
            if task.edit_description(new_description):
                print(f"任务{index_e_int+1}: {task}已更新")
            else:
                print("任务描述不能为空，操作已取消")

        #清除已完成任务
        elif input_str == "cd":
            
            if todo_list:
                has_done_tasks = any(task.status == "已完成" for task in todo_list)
                if not has_done_tasks:
                    print("任务列表中没有已完成的任务")
                    continue
                cd_choice = input("确认要清除‘已完成’状态的任务吗？（y/n）:").strip().lower()
                if cd_choice == "y":
                    clear_count = clear_done_tasks()
                    if clear_count > 0:
                        print(f"已清除{clear_count}个已完成任务")
                else:
                    print("已取消清除已完成任务")
                   
            else:
                print("任务列表为空，无法操作任务")

        elif input_str == "p":
            task, index_p_int = get_task_from_user_input()
            if not task:
                continue
            old_priority = task.priority
            new_priority = input(f"将修改{index_p_int+1}:{task.description}的优先级，当前优先级为{old_priority},请输入新的优先级（{prompt_options}），“回车”表示退出，不修改：").strip() 
            if new_priority == "":
                print("输入为空，操作已取消")
               
            if new_priority == "无":
                new_priority = None
            if new_priority in VALID_PRIORITY:
                if task.set_priority(new_priority):
                    print(f"任务{index_p_int+1}: {task.description}的“优先级”已由’{old_priority}‘已更新为‘{task.priority}’")
                else:
                    print(f"无效的优先级，请输入:{prompt_options}")

        elif input_str == "sd":
            task, index_sd_int =get_task_from_user_input()
            if not task:
                continue
            old_end_date = task.end_date if task.end_date else "无"
            date_str = input(f"将为任务{index_sd_int+1}:{task.description}设置截止日期，当前截止日期为‘{old_end_date}’,请按“年-月-日，如2025-05-23”格式输入新的截止日期：(输入“无”，将清空当前截止日期，输入回车表示“退出，不修改”)\n").strip()
            if date_str =="":
                print("输入为空，操作已取消")
                continue
            elif date_str == "无":
                if task.set_end_date(None):
                    print(f"任务{index_sd_int+1}: {task.description}的截止日期已清空")
            else:
                try:
                    new_end_date = dt.date.fromisoformat(date_str)
                except ValueError:
                    print("无效的日期格式，请按“年-月-日“格式输入日期，如2025-05-23")
                    continue
                if task.set_end_date(new_end_date):
                    print(f"任务{index_sd_int + 1}： {task.description}的截止日期已由‘{old_end_date}’,修改为‘{new_end_date}’")
                else:
                    print("设置截止日期失败")



        #退出
        elif input_str == "q":
            save_tasks()
            print("感谢使用任务管理系统，再见！")
            break
        else:
            print("无效的命令，请输入n、m、d或q")
            continue
        



