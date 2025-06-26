import pandas as pd
import os
# from pathlib import Path # 移除未使用的导入
import argparse # 导入 argparse 模块

def split_dataframe_by_column_and_save(df, column_a, column_b, output_dir='output'): # 修改默认输出目录为相对路径
    """
    根据DataFrame的指定列拆分数据并保存到对应的文件夹

    参数:
    df (pd.DataFrame): 要拆分的DataFrame
    column_a (str): 用于拆分数据的列名（A列）
    column_b (str): 用于创建文件夹的列名（B列）
    output_dir (str): 输出目录的根路径，默认为'output'
    """
    try:
        # 创建根输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 按B列的值分组
        for b_value, group_b in df.groupby(column_b):
            # 创建以B列值命名的文件夹
            folder_path = os.path.join(output_dir, str(b_value))
            os.makedirs(folder_path, exist_ok=True)

            # 按A列的值进一步分组
            for a_value, group_a in group_b.groupby(column_a):
                # 构建输出文件路径
                # 确保文件名是字符串且有效
                valid_a_value = str(a_value).replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                file_name = f"{valid_a_value}.xlsx"
                file_path = os.path.join(folder_path, file_name)

                # 保存数据到Excel文件
                try:
                    group_a.to_excel(file_path, index=False)
                    print(f"已保存文件: {file_path}")
                except Exception as e:
                    print(f"保存文件 {file_path} 时发生错误: {e}")

    except KeyError as e:
        print(f"指定的列名不存在: {e}")
    except Exception as e:
        print(f"处理数据时发生未知错误: {e}")


# 示例使用
if __name__ == "__main__":
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='根据DataFrame的指定列拆分数据并保存到对应的文件夹。')

    # 添加命令行参数
    parser.add_argument('input_file', type=str, help='要读取的Excel文件路径')
    parser.add_argument('column_a', type=str, help='用于拆分数据的列名（A列）')
    parser.add_argument('column_b', type=str, help='用于创建文件夹的列名（B列）')
    parser.add_argument('-o', '--output_dir', type=str, default='output_data', help='输出目录的根路径，默认为 output_data')

    # 解析命令行参数
    args = parser.parse_args()

    try:
        # 读取Excel文件
        df = pd.read_excel(args.input_file)
        print(f"成功读取文件: {args.input_file}")

        # 调用函数拆分并保存数据
        split_dataframe_by_column_and_save(df, args.column_a, args.column_b, args.output_dir)

    except FileNotFoundError:
        print(f"错误：找不到文件 {args.input_file}")
    except pd.errors.EmptyDataError:
        print(f"错误：文件 {args.input_file} 是空的")
    except Exception as e:
        print(f"读取文件 {args.input_file} 时发生错误: {e}")