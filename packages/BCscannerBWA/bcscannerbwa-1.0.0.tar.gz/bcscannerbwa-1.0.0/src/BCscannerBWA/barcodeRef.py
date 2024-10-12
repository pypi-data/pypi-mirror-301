#########################################################
# title:barcode index
# author:dawang
# date:20230915
#########################################################

import argparse
import subprocess


def format_input(input_str):
    lines = input_str.strip().split('\n')
    output = []
    for i, line in enumerate(lines):
        output.append(f'>b{i+1}')
        output.append(line)
    return '\n'.join(output)

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='Input formatting script')
parser.add_argument('-i', '--input', type=str, help='Path to the input txt file')
parser.add_argument('-o', '--output', type=str, help='Path to the output file')

# 解析命令行参数
args = parser.parse_args()

# 检查是否提供输入文件路径
if not args.input:
    print("请提供输入文件路径")
    exit(1)

# 检查是否提供输出文件路径
if not args.output:
    print("请提供输出文件路径")
    exit(1)

# 读取输入文件内容
try:
    with open(args.input, 'r') as file:
        input_str = file.read()
except FileNotFoundError:
    print("找不到指定的输入文件")
    exit(1)

# 格式化输入
formatted_input = format_input(input_str)

# 写入结果到输出文件
with open(args.output, 'w') as output_file:
    output_file.write(formatted_input)

print(f"结果已保存到文件: {args.output}")

# 创建bwa索引
index_command = ['bwa', 'index', args.output]
try:
    subprocess.run(index_command, check=True)
    print(f"已成功创建bwa索引: {args.output}")
except subprocess.CalledProcessError:
    print("创建bwa索引时出现错误")