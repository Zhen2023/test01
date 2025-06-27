import os

def print_directory_tree(root_dir, exclude_dirs=None):
    """
    一个打印目录树的函数。

    :param root_dir: 要遍历的根目录路径。
    :param exclude_dirs: 要排除的文件夹名称列表（或集合）。
    """
    if exclude_dirs is None:
        # 使用集合(set)进行查找，效率更高
        exclude_dirs = set()
    else:
        exclude_dirs = set(exclude_dirs)

    print(f"目录树: {os.path.abspath(root_dir)}")

    for root, dirs, files in os.walk(root_dir, topdown=True):
        # --- 核心排除逻辑 ---
        # os.walk(topdown=True) 允许我们在这里修改 dirs 列表，
        # 从而阻止 os.walk 继续深入到被排除的目录中。
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # 计算当前目录的深度，用于生成缩进
        level = root.replace(root_dir, '').count(os.sep)
        indent = '│   ' * (level -1) + '├── ' if level > 0 else ''

        # 打印当前目录名
        # os.path.basename(root) 获取路径的最后一部分 (即当前目录名)
        if level > 0:
            print(f"{indent}{os.path.basename(root)}/")

        # 打印当前目录下的所有文件
        sub_indent = '│   ' * level + '├── '
        for i, f in enumerate(files):
            # 如果是最后一个文件，使用不同的连接符
            if i == len(files) - 1 and len(dirs) == 0:
                 sub_indent = '│   ' * level + '└── '
            print(f"{sub_indent}{f}")


# --- 主程序部分 ---
if __name__ == "__main__":
    # 1. 设置你的目标文件夹路径
    # 使用 r"..." (原始字符串) 来避免 Windows 路径中反斜杠 \ 的转义问题
    target_path = r"D:\Trae_work\my-flask-blog-fina" #我在这里新增了内容，你能识别到么

    # 2. 设置要排除的文件夹名称
    folders_to_exclude = ["venv", "__pycache__", "migrations",".trae","test",".git"] # 我也帮你把 migrations 加进去了，因为它通常也和核心逻辑无关

    # 3. 调用函数
    if os.path.isdir(target_path):
        print_directory_tree(target_path, exclude_dirs=folders_to_exclude)
    else:
        print(f"错误：路径 '{target_path}' 不是一个有效的目录。")